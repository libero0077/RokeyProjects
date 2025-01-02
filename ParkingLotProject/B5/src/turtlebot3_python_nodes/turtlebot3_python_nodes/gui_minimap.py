import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QLabel, 
                             QVBoxLayout, QHBoxLayout, QSizePolicy)
from PyQt5.QtGui import QImage, QPixmap
from rclpy.executors import SingleThreadedExecutor
from PyQt5.QtCore import Qt, pyqtSignal, QThread, QObject
import sys
from std_msgs.msg import String, Bool
import json
from PyQt5.QtGui import QFont
from ultralytics import YOLO
import cv2
import time
from collections import deque
import yaml
from PIL import Image as PILImage, ImageDraw
from geometry_msgs.msg import PoseWithCovarianceStamped
from turtlebot3_interfaces.srv import GetSystemState

import random

# 튜플 리스트 (샘플: 실제로는 질문에 주어진 전체 튜플을 여기에 정의)
SLOT_TUPLES = [
    (1, 1), (1, 2), (1, 3), (1, 6), (1, 7), (1, 11), (1, 14), (1, 15), (1, 16),
    (3, 2), (3, 3), (3, 5), (3, 7), (3, 8), (3, 10), (3, 13), (3, 15),
    (4, 3), (4, 8), (4, 9), (4, 10), (4, 14), (4, 15),
    (6, 2), (6, 4), (6, 5), (6, 7), (6, 9), (6, 10), (6, 12), (6, 14), (6, 15),
    (7, 2), (7, 3), (7, 7), (7, 10), (7, 12), (7, 13), (7, 14), (7, 15),
    (9, 3), (9, 5), (9, 6), (9, 7), (9, 9), (9, 10), (9, 11), (9, 14), (9, 15), (9, 16)
]

class MapNode(Node):
    def __init__(self):
        super().__init__('map_node')
        self.amcl_pose_x = 0.0
        self.amcl_pose_y = 0.0
        self.amcl_pose_x2 = 0.0
        self.amcl_pose_y2 = 0.0
        
        self.create_subscription(
            PoseWithCovarianceStamped,
            'tb1/amcl_pose',
            self.subscription_callback,
            10
        )

        self.create_subscription(
            PoseWithCovarianceStamped,
            'tb2/amcl_pose',
            self.subscription_callback2,
            10
        )

    def subscription_callback(self, msg):
        self.amcl_pose_x = msg.pose.pose.position.x
        self.amcl_pose_y = msg.pose.pose.position.y

    def subscription_callback2(self, msg):
        self.amcl_pose_x2 = msg.pose.pose.position.x
        self.amcl_pose_y2 = msg.pose.pose.position.y

class MapThread(QThread):
    signal = pyqtSignal(float, float)    # 첫 번째 로봇 좌표 시그널
    signal2 = pyqtSignal(float, float)   # 두 번째 로봇 좌표 시그널
    parking_status_signal = pyqtSignal(str)

    def __init__(self, executor, camera_node, map_node):
        super().__init__()
        self.executor = executor
        self.camera_node = camera_node
        self.map_node = map_node
        self.running = True

    def run(self):
        while rclpy.ok() and self.running:
            self.executor.spin_once(timeout_sec=0.1)
            self.signal.emit(self.map_node.amcl_pose_x, self.map_node.amcl_pose_y)
            self.signal2.emit(self.map_node.amcl_pose_x2, self.map_node.amcl_pose_y2)

            # 예제 주차장 상태 데이터 emit (실제 로직에 맞게 변경 가능)
            parking_status_data = json.dumps({'slot_name': 'A-11', 'task_type': '주차'})
            self.parking_status_signal.emit(parking_status_data)

    def stop(self):
        self.running = False

class CameraViewer(Node, QObject):
    logs_signal = pyqtSignal(str)
    robot_status_signal = pyqtSignal(str)
    parking_status_update_signal = pyqtSignal(dict)
    update_image_signal = pyqtSignal(int, object)  # object로 cv_image(numpy array) 전달

    def __init__(self, app):
        Node.__init__(self, 'camera_viewer')
        QObject.__init__(self)

        self.app = app
        self.bridge = CvBridge()

        # 주차장 상태 초기화
        self.parking_status_info = {}
        for (r, c) in SLOT_TUPLES:
            slot_name = f"A-{r}{c}"
            self.parking_status_info[slot_name] = '빈 슬롯'

        # 토픽 구독
        self.create_subscription(String, '/parking_status', self.parking_status_callback, 10)
        self.create_subscription(String, '/central_control/logs', self.logs_callback, 10)
        self.create_subscription(String, '/central_control/robot_status', self.robot_status_callback, 10)

        # YOLO 로드 (모델 경로 실제 환경에 맞게 변경)
        self.yolo_model = YOLO('yolov8m.pt')  
        self.vehicle_pub = self.create_publisher(String, '/vehicle_detected', 10)
        self.vehicle_classes = ['car', 'truck', 'bus', 'motorcycle', 'person']
        self.detection_times = deque()
        self.roi = (450, 530, 640, 640)

        # QoS 설정
        self.qos = rclpy.qos.QoSProfile(
            reliability=rclpy.qos.QoSReliabilityPolicy.BEST_EFFORT,
            durability=rclpy.qos.QoSDurabilityPolicy.VOLATILE,
            history=rclpy.qos.QoSHistoryPolicy.KEEP_LAST,
            depth=1
        )

        self.camera_topics = {
            'camera_wall_1/image_raw': 0,
            'camera_wall_2/image_raw': 1,
            'camera_wall_3/image_raw': 2,
            'camera_wall_4/image_raw': 3,
            'camera_wall_5/image_raw': 4,
            'camera_wall_6/image_raw': 5,
            'camera_wall_7/image_raw': 6,
            'camera_wall_8/image_raw': 7
        }

        self.subscribers = []
        for topic in self.camera_topics.keys():
            self.subscribers.append(
                self.create_subscription(Image, topic, self.image_callback, self.qos)
            )

        # UI 설정
        self.window = QWidget()
        self.main_layout = QHBoxLayout(self.window)

        self.left_layout = QVBoxLayout()
        self.camera_layout = QGridLayout()
        self.camera_layout.setSpacing(2)
        self.camera_layout.setContentsMargins(5, 5, 5, 5)
        self.left_layout.addLayout(self.camera_layout)

        self.right_layout = QVBoxLayout()
        self.main_layout.addLayout(self.left_layout, 2)
        self.main_layout.addLayout(self.right_layout, 3)

        self.image_labels = []
        for i in range(8):
            label = QLabel()
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("border: 1px solid black; background-color: black;")
            label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            label.setMinimumSize(240, 180)
            label.setScaledContents(True)
            label.mousePressEvent = lambda event, index=i: self.show_enlarged(index)
            self.image_labels.append(label)
            self.camera_layout.addWidget(label, i // 2, i % 2)

        self.map_label = QLabel("맵")
        self.map_label.setStyleSheet("border: 1px solid black;")
        self.map_label.setAlignment(Qt.AlignCenter)
        self.map_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.right_layout.addWidget(self.map_label, 70)

        # 맵 로딩
        try:
            image_path = '/home/juwon/git/RokeyProjects/ParkingLotProject/B5/src/turtlebot3_python_nodes/map/map.pgm'
            yaml_path = '/home/juwon/git/RokeyProjects/ParkingLotProject/B5/src/turtlebot3_python_nodes/map/map.yaml'
            image = PILImage.open(image_path)
            self.width, self.height = image.size
            self.image_rgb = image.convert('RGB')
            with open(yaml_path, 'r') as file:
                data = yaml.safe_load(file)
            self.resolution = data['resolution']
            self.map_x = -data['origin'][0]
            self.map_y = data['origin'][1] + self.height * self.resolution
            self.resize_factor = 0.5
            self.scaled_width = int(self.width * self.resize_factor)
            self.scaled_height = int(self.height * self.resize_factor)

            self.dot_size = 2
            self.robot1_x = None
            self.robot1_y = None
            self.robot2_x = None
            self.robot2_y = None

            self.get_logger().info(f"Map image loaded successfully from {image_path}")
        except Exception as e:
            self.get_logger().error(f"Failed to load map image: {str(e)}")


        self.parking_status_label = QLabel("주차장 상태")
        self.parking_status_label.setStyleSheet("""
            border: 1px solid black;
            font-size: 18px;
            font-weight: bold;
            background-color: #f0f0f0;
            padding: 10px;
        """)
        self.parking_status_label.setAlignment(Qt.AlignCenter)
        self.parking_status_label.setWordWrap(True)
        self.right_layout.addWidget(self.parking_status_label, 15)

        self.log_label = QLabel("로그")
        self.log_label.setStyleSheet("border: 1px solid black;")
        self.log_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)  # 좌측 상단 정렬로 변경
        self.right_layout.addWidget(self.log_label, 10)

        self.robot_status_label = QLabel("로봇 상태")
        self.robot_status_label.setStyleSheet("border: 1px solid black;")
        self.robot_status_label.setAlignment(Qt.AlignCenter)
        self.right_layout.addWidget(self.robot_status_label, 5)

        screen = self.app.primaryScreen().geometry()
        window_width = screen.width()
        window_height = screen.height()
        self.window.setGeometry(0, 0, window_width, window_height)
        self.window.setWindowTitle('Camera Viewer')
        self.window.show()

        # 로그를 저장할 deque (최대 1000줄 유지)
        self.log_messages = deque(maxlen=50)
        # 로봇 상태도 비슷하게 deque로 관리
        self.robot_status_messages = deque(maxlen=10)

        # 로깅용 라벨 다중 줄 표시를 위해 setWordWrap(True) 또는 RichText사용
        self.log_label.setWordWrap(True)
        # setTextFormat을 RichText로 설정 (필요시)

        self.robot_status_label.setWordWrap(True)
        # self.robot_status_label.setTextFormat(Qt.RichText)

        # get_system_state 서비스 클라이언트 생성 및 호출
        self.get_system_state_client = self.create_client(GetSystemState, 'get_system_state')
        while not self.get_system_state_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for get_system_state service...')
        self.call_get_system_state_service()

        # 시그널-슬롯 연결
        self.logs_signal.connect(self.add_log_message)
        self.robot_status_signal.connect(self.robot_status_callback)
        self.parking_status_update_signal.connect(self.handle_parking_status_update)
        self.update_image_signal.connect(self.set_image_label)

        # 초기화 과정 종료 전에 redraw_map 호출
        self.get_logger().info("Calling redraw_map() for initial display...")
        self.redraw_map()

    def connect_signals(self, map_thread):
        map_thread.signal.connect(self.handle_robot1_update)
        map_thread.signal2.connect(self.handle_robot2_update)
        map_thread.parking_status_signal.connect(self.update_parking_status_from_thread)

    def call_get_system_state_service(self):
        req = GetSystemState.Request()
        future = self.get_system_state_client.call_async(req)
        future.add_done_callback(self.handle_get_system_state_response)

    def handle_get_system_state_response(self, future):
        try:
            response = future.result()
            robot_status_list = json.loads(response.robot_status_json)
            slot_status_list = json.loads(response.slot_status_json)

        # 로봇 상태를 emit할 때 str(robot_status_list)가 아닌 json.dumps(robot_status_list)를 사용
            if robot_status_list:
                self.robot_status_signal.emit(json.dumps(robot_status_list))
            else:
                self.robot_status_signal.emit(json.dumps([]))  # 빈 리스트라도 JSON으로

            self.parking_status_info.clear()
            for slot_info in slot_status_list:
                slot_name = slot_info.get('slot_name', 'Unknown')
                task_type = slot_info.get('task_type', '빈 슬롯')
                self.parking_status_info[slot_name] = task_type
            self.update_parking_status_ui()

        except Exception as e:
            self.get_logger().error(f"Error getting system state: {e}")

    def logs_callback(self, msg):
        # msg.data 예: {"timestamp":"2023-12-10T15:23:45","origin":"central_control_node","message":"Vehicle detected"}
        try:
            log_data = json.loads(msg.data)
            timestamp = log_data.get('timestamp', '')
            origin = log_data.get('origin', '')
            message = log_data.get('message', '')

            # 보기 좋은 형식으로 변환
            # [HH:MM:SS] (origin): message
            # timestamp에서 시간 파싱 (예: ISO8601 -> HH:MM:SS 부분만)
            # 간단히 전체 timestamp 출력하거나 슬라이스로 원하는 부분 사용 가능
            # 예: "2023-12-10T15:23:45" -> "15:23:45"
            time_str = timestamp.split('T')[-1] if 'T' in timestamp else timestamp
            formatted_msg = f"[{time_str}] ({origin}): {message}"

            # 시그널 emit
            self.logs_signal.emit(formatted_msg)

        except json.JSONDecodeError as e:
            self.get_logger().error(f"Log parsing error: {str(e)}")

    def add_log_message(self, formatted_msg):
        # formatted_msg를 deque에 추가
        self.log_messages.append(formatted_msg)
        # 전체 로그를 HTML 형식으로 합쳐서 표시
        # 줄바꿈은 <br>로 처리
        html_logs = "<br>".join(self.log_messages)
        self.log_label.setText(html_logs)

    def robot_status_callback(self, msg):
        # msg는 이제 ROS 메시지가 아닌 str 타입
        try:
            status_list = json.loads(msg)  # msg.data 대신 msg 사용
            if not status_list:
                self.robot_status_label.setText("로봇 상태 정보 없음")
                return

            lines = []
            for st in status_list:
                rid = st.get('robot_id', '?')
                state = st.get('state', '?')
                last_task = st.get('last_task', 'None')
                lines.append(f"Robot {rid}: {state} (last task: {last_task})")

            formatted_status = " | ".join(lines)
            self.robot_status_label.setText(formatted_status)

        except json.JSONDecodeError as e:
            self.get_logger().error(f"Robot status parsing error: {str(e)}")

    def add_robot_status_message(self, formatted_status):
        # 로봇 상태 메시지 업데이트
        # 상태는 매번 전체 리스트를 받는다고 가정하면 단순히 최근 상태만 표시
        # 여러 개 상태를 누적할 필요 없으면 그냥 setText
        # 혹은 상태 변화 이력을 쌓고 싶다면 deque 사용
        self.robot_status_messages.append(formatted_status)
        # 최근 상태 1개만 보여준다거나, N개만 보여주고 싶다면 join해서 표시
        # 여기서는 최근 10개 상태만 표시 (deque maxlen=100이므로 항상 유지)
        recent_statuses = list(self.robot_status_messages)[-10:]
        html_status = "<br>".join(recent_statuses)
        self.robot_status_label.setText(html_status)

    # parking_status_update_signal, update_image_signal, 등 나머지 함수는 기존과 동일
    # ...

    def parking_status_callback(self, msg):
        try:
            parking_status = json.loads(msg.data)
            self.parking_status_update_signal.emit(parking_status)
        except json.JSONDecodeError as e:
            self.get_logger().error(f"주차장 상태 파싱 오류: {str(e)}")

    def handle_parking_status_update(self, parking_status):
        slot_name = parking_status.get('slot_name', '알 수 없음')
        task_type = parking_status.get('task_type', '알 수 없음')

        if slot_name in self.parking_status_info:
            self.parking_status_info[slot_name] = task_type
            self.update_parking_status_ui()
            self.get_logger().info(f"주차장 상태 업데이트: {slot_name}, {task_type}")
        else:
            self.get_logger().error(f"알 수 없는 슬롯: {slot_name}")

    def update_parking_status_from_thread(self, parking_status_data):
        try:
            parking_status = json.loads(parking_status_data)
            self.parking_status_update_signal.emit(parking_status)
        except json.JSONDecodeError as e:
            self.get_logger().error(f"주차장 상태 파싱 오류: {str(e)}")

    def update_parking_status_ui(self):
        if not self.parking_status_info:
            self.parking_status_label.setText("현재 주차장 상태 정보가 없습니다.")
            return

        status_summary = ""
        count = 0
        for slot, task in self.parking_status_info.items():
            color = self.get_status_color(task)
            status_summary += f"<span style='color: {color}; font-size: 17px; font-weight: bold;'>{slot}: {task}</span> "
            count += 1
            if count % 10 == 0:
                status_summary += "<br>"

        self.parking_status_label.setText(f"<html>{status_summary}</html>")

    def get_status_color(self, task_type):
        color_map = {
            '주차': '#FF6347',
            '출차 중': '#FFA500',
            '주차 중': '#1E90FF',
            '빈 슬롯': '#32CD32',
            'None1': '#FF6347',
            'None2': '#32CD32'
        }
        return color_map.get(task_type, '#000000')

    def handle_robot1_update(self, x, y):
        self.robot1_x = x
        self.robot1_y = y
        self.redraw_map()

    def handle_robot2_update(self, x, y):
        self.robot2_x = x
        self.robot2_y = y
        self.redraw_map()

    def redraw_map(self):
        image_copy = self.image_rgb.copy()
        draw = ImageDraw.Draw(image_copy)

        if self.robot1_x is not None and self.robot1_y is not None:
            pos_x = self.map_x + self.robot1_x
            pos_y = self.map_y - self.robot1_y
            draw.ellipse((pos_x / self.resolution - self.dot_size,
                          pos_y / self.resolution - self.dot_size,
                          pos_x / self.resolution + self.dot_size,
                          pos_y / self.resolution + self.dot_size),
                         fill='red')

        if self.robot2_x is not None and self.robot2_y is not None:
            pos_x2 = self.map_x + self.robot2_x
            pos_y2 = self.map_y - self.robot2_y
            draw.ellipse((pos_x2 / self.resolution - self.dot_size,
                          pos_y2 / self.resolution - self.dot_size,
                          pos_x2 / self.resolution + self.dot_size,
                          pos_y2 / self.resolution + self.dot_size),
                         fill='blue')

        image_resized = image_copy.resize((self.scaled_width, self.scaled_height))
        pil_image = image_resized.convert('RGBA')
        data = pil_image.tobytes("raw", "RGBA")
        qimage = QImage(data, self.scaled_width, self.scaled_height, QImage.Format_RGBA8888)
        pixmap = QPixmap.fromImage(qimage)
        self.map_label.setPixmap(pixmap)
        self.map_label.repaint()

    def image_callback(self, msg):
        # 콜백 스레드에서 GUI 객체 생성 X
        try:
            topic = msg.header.frame_id.split('_frame')[0] + '/image_raw'
            if topic in self.camera_topics:
                index = self.camera_topics[topic]
                cv_image = self.bridge.imgmsg_to_cv2(msg, "rgb8")

                # YOLO 처리
                if index == 2:
                    cv_image = self.detect_vehicle(cv_image)

                # GUI 객체 생성하지 않고 raw cv_image만 메인 스레드로 전달
                self.update_image_signal.emit(index, cv_image)

        except Exception as e:
            self.get_logger().error(f'Error processing image: {str(e)}')

    def set_image_label(self, index, cv_image):
        # 메인 스레드 슬롯: 여기서 QImage/QPixmap 생성
        h, w, ch = cv_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(cv_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image)
        self.image_labels[index].setPixmap(pixmap)

    def detect_vehicle(self, frame):
        results = self.yolo_model(frame)
        detected = False

        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                cls = int(box.cls)
                label = self.yolo_model.names[cls]

                if label in self.vehicle_classes:
                    if (self.roi[0] <= x1 <= self.roi[2]) and (self.roi[1] <= y1 <= self.roi[3]):
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(frame, label, (x1, y1 - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                        detected = True

        current_time = time.time()
        if detected:
            self.detection_times.append(current_time)
        else:
            self.detection_times.clear()

        if len(self.detection_times) > 0:
            time_diff = current_time - self.detection_times[0]
            if time_diff >= 5:
                vehicle_id = random.randint(1000, 9999)
                message_str = f"{vehicle_id}, 대기 지역에 차량이 진입하였습니다."
                msg = String()
                msg.data = message_str
                self.vehicle_pub.publish(msg)
                self.get_logger().info(f"대기 지역에 차량 {vehicle_id}번 진입")
                self.detection_times.clear()

        return frame

    def show_enlarged(self, index):
        # 메인 스레드에서 실행
        if hasattr(self, 'current_enlarged') and self.current_enlarged == index:
            self.restore_original_layout()
            return

        self.current_enlarged = index
        enlarged_label = self.image_labels[index]

        for i, label in enumerate(self.image_labels):
            if i != index:
                label.hide()

        self.camera_layout.removeWidget(enlarged_label)
        self.camera_layout.addWidget(enlarged_label, 0, 0, 4, 3)
        enlarged_label.setScaledContents(True)

    def restore_original_layout(self):
        # 메인 스레드에서 실행
        for i, label in enumerate(self.image_labels):
            label.setScaledContents(True)
            self.camera_layout.removeWidget(label)
            label.show()
            self.camera_layout.addWidget(label, i // 2, i % 2)
        delattr(self, 'current_enlarged')

    def run(self):
        while self.app:
            self.app.processEvents()

def main(args=None):
    rclpy.init(args=args)
    app = QApplication(sys.argv)

    viewer = CameraViewer(app)
    map_node = MapNode()

    executor = SingleThreadedExecutor()
    executor.add_node(viewer)
    executor.add_node(map_node)

    # 메인 스레드에서 ROS와 Qt 이벤트를 함께 처리
    while rclpy.ok():
        executor.spin_once(timeout_sec=0.01)
        app.processEvents()

    viewer.destroy_node()
    map_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
