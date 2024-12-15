# ROS2와 Qt 관련 라이브러리 임포트
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image  # ROS2 이미지 메시지 타입
from cv_bridge import CvBridge  # ROS 이미지를 OpenCV 이미지로 변환
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QVBoxLayout, QHBoxLayout, QSizePolicy
from PyQt5.QtGui import QImage, QPixmap
from rclpy.executors import SingleThreadedExecutor
from PyQt5.QtCore import Qt, pyqtSignal, QThread
import sys

### YOLO 기능 사용 ########
from ultralytics import YOLO
import cv2
import time
from collections import deque
from std_msgs.msg import Bool

################# minimap#####################
import yaml
from PIL import Image as PILImage, ImageDraw
from geometry_msgs.msg import PoseWithCovarianceStamped

###########################################################
# MapNode 및 MapThread 정의
###########################################################
class MapNode(Node):
    def __init__(self):
        super().__init__('map_node')
        self.amcl_pose_x = 0.0
        self.amcl_pose_y = 0.0
        self.sub_cmd_vel = self.create_subscription(
            PoseWithCovarianceStamped,
            'tb1/amcl_pose',
            self.subscription_callback,
            10
        )

        # 여기 추가 (tb2/amcl_pose 구독)
        self.amcl_pose_x2 = 0.0
        self.amcl_pose_y2 = 0.0
        self.sub_cmd_vel2 = self.create_subscription(
            PoseWithCovarianceStamped,
            'tb2/amcl_pose',
            self.subscription_callback2,
            10
        )

    def subscription_callback(self, msg):
        self.amcl_pose_x = msg.pose.pose.position.x
        self.amcl_pose_y = msg.pose.pose.position.y

    # 여기 추가 (두 번째 로봇 콜백)
    def subscription_callback2(self, msg):
        self.amcl_pose_x2 = msg.pose.pose.position.x
        self.amcl_pose_y2 = msg.pose.pose.position.y

class MapThread(QThread):
    signal = pyqtSignal(float, float)  # 기존 첫 번째 로봇용
    # 여기 추가 (두 번째 로봇용 시그널)
    signal2 = pyqtSignal(float, float)

    def __init__(self, executor, camera_node, map_node):
        super().__init__()
        self.executor = executor
        self.camera_node = camera_node
        self.map_node = map_node
        self.running = True

    def run(self):
        while rclpy.ok() and self.running:
            self.executor.spin_once(timeout_sec=0.1)
            # 첫 번째 로봇 좌표 전달
            self.signal.emit(self.map_node.amcl_pose_x, self.map_node.amcl_pose_y)
            # 두 번째 로봇 좌표 전달 추가
            self.signal2.emit(self.map_node.amcl_pose_x2, self.map_node.amcl_pose_y2)

    def stop(self):
        self.running = False

###########################################################
# CameraViewer 정의 (첫 번째 코드)
###########################################################
class CameraViewer(Node):
    def __init__(self, app):
        super().__init__('camera_viewer')
        self.app = app
        self.bridge = CvBridge()

        ######################## yolov8 모델 로드 ####################
        self.yolo_model = YOLO('yolov8m.pt')  
        self.vehicle_pub = self.create_publisher(Bool, '/vehicle_detected', 10)
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
                self.create_subscription(
                    Image,
                    topic,
                    self.image_callback,
                    self.qos
                )
            )

        # UI 설정
        self.window = QWidget()
        self.main_layout = QHBoxLayout()
        self.window.setLayout(self.main_layout)

        self.left_layout = QVBoxLayout()
        self.camera_layout = QGridLayout()
        self.camera_layout.setSpacing(2)
        self.camera_layout.setContentsMargins(5, 5, 5, 5)
        self.left_layout.addLayout(self.camera_layout)

        self.right_layout = QVBoxLayout()

        # 메인 레이아웃에 좌우 레이아웃 추가
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

        # 여기서부터 Map 기능 추가
        self.dot_size = 2
        image = PILImage.open('/home/rokey/Documents/RokeyProjects/multitb_ws/src/turtlebot3_multi_robot/map/map.pgm')
        self.width, self.height = image.size
        self.image_rgb = image.convert('RGB')
        with open('/home/rokey/Documents/RokeyProjects/multitb_ws/src/turtlebot3_multi_robot/map/map.yaml', 'r') as file:
            data = yaml.safe_load(file)
        self.resolution = data['resolution']
        self.map_x = -data['origin'][0]
        self.map_y = data['origin'][1] + self.height * self.resolution
        self.resize_factor = 0.5
        self.scaled_width = int(self.width * self.resize_factor)
        self.scaled_height = int(self.height * self.resize_factor)

        # 여기 추가 (두 로봇 위치 저장)
        self.robot1_x = None
        self.robot1_y = None
        self.robot2_x = None
        self.robot2_y = None

        self.parking_status_label = QLabel("주차장 상태")
        self.parking_status_label.setStyleSheet("border: 1px solid black;")
        self.parking_status_label.setAlignment(Qt.AlignCenter)
        self.right_layout.addWidget(self.parking_status_label, 15)

        self.log_label = QLabel("로그")
        self.log_label.setStyleSheet("border: 1px solid black;")
        self.log_label.setAlignment(Qt.AlignCenter)
        self.right_layout.addWidget(self.log_label, 10)

        self.robot_status_label = QLabel("로봇 상태")
        self.robot_status_label.setStyleSheet("border: 1px solid black;")
        self.robot_status_label.setAlignment(Qt.AlignCenter)
        self.right_layout.addWidget(self.robot_status_label, 5)

        # 윈도우 설정
        screen = self.app.primaryScreen().geometry()
        window_width = screen.width()
        window_height = screen.height()
        self.window.setGeometry(0, 0, window_width, window_height)
        self.window.setWindowTitle('Camera Viewer')
        self.window.show()

    def update_map(self, x, y):
        self.robot1_x = x
        self.robot1_y = y
        self.redraw_map()  # 맵 재갱신

    # 여기 추가 (두 번째 로봇용 함수)
    def update_map2(self, x, y):
        self.robot2_x = x
        self.robot2_y = y
        self.redraw_map()

    # 여기 추가 (두 로봇 모두 그리는 함수)
    def redraw_map(self):
        image_copy = self.image_rgb.copy()
        draw = ImageDraw.Draw(image_copy)

        # 첫 번째 로봇
        if self.robot1_x is not None and self.robot1_y is not None:
            pos_x = self.map_x + self.robot1_x
            pos_y = self.map_y - self.robot1_y
            draw.ellipse((
                pos_x / self.resolution - self.dot_size,
                pos_y / self.resolution - self.dot_size,
                pos_x / self.resolution + self.dot_size,
                pos_y / self.resolution + self.dot_size),
                fill='red'
            )

        # 두 번째 로봇
        if self.robot2_x is not None and self.robot2_y is not None:
            pos_x2 = self.map_x + self.robot2_x
            pos_y2 = self.map_y - self.robot2_y
            draw.ellipse((
                pos_x2 / self.resolution - self.dot_size,
                pos_y2 / self.resolution - self.dot_size,
                pos_x2 / self.resolution + self.dot_size,
                pos_y2 / self.resolution + self.dot_size),
                fill='blue'
            )

        image_resized = image_copy.resize((self.scaled_width, self.scaled_height))
        pil_image = image_resized.convert('RGBA')
        data = pil_image.tobytes("raw", "RGBA")
        qimage = QImage(data, self.scaled_width, self.scaled_height, QImage.Format_RGBA8888)
        pixmap = QPixmap.fromImage(qimage)
        self.map_label.setPixmap(pixmap)
        self.map_label.repaint()

    def image_callback(self, msg):
        try:
            topic = msg.header.frame_id.split('_frame')[0] + '/image_raw'
            if topic in self.camera_topics:
                index = self.camera_topics[topic]
                cv_image = self.bridge.imgmsg_to_cv2(msg, "rgb8")

                # YOLO 적용 (3번 카메라에만)
                if index == 2:  
                    cv_image = self.detect_vehicle(cv_image)

                h, w, ch = cv_image.shape
                bytes_per_line = ch * w
                qt_image = QImage(cv_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(qt_image)
                self.image_labels[index].setPixmap(pixmap)
        except Exception as e:
            self.get_logger().error(f'Error processing image: {str(e)}')

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
                msg = Bool()
                msg.data = True
                self.vehicle_pub.publish(msg)
                self.get_logger().info('대기 지역에 차량이 진입하였습니다')
                self.detection_times.clear()

        return frame

    def show_enlarged(self, index):
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
        for i, label in enumerate(self.image_labels):
            label.setScaledContents(True)
            self.camera_layout.removeWidget(label)
            label.show()
            self.camera_layout.addWidget(label, i // 2, i % 2)
        delattr(self, 'current_enlarged')

    def run(self):
        # 여기서는 ROS spin을 하지 않고, 단지 Qt 이벤트만 처리
        while self.app:
            self.app.processEvents()


def main(args=None):
    rclpy.init(args=args)
    app = QApplication(sys.argv)

    # 노드 생성
    viewer = CameraViewer(app)
    map_node = MapNode()

    # Executor 생성 후 노드를 추가
    executor = SingleThreadedExecutor()
    executor.add_node(viewer)
    executor.add_node(map_node)

    # MapThread에서 spin 처리
    map_thread = MapThread(executor, viewer, map_node)
    map_thread.signal.connect(viewer.update_map)
    # 여기 추가 (두 번째 로봇 시그널 연결)
    map_thread.signal2.connect(viewer.update_map2)
    map_thread.start()

    viewer.run()  # UI 이벤트 처리

    # 종료 처리
    map_thread.stop()
    map_thread.wait()
    viewer.destroy_node()
    map_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
