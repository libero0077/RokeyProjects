# ROS2와 Qt 관련 라이브러리 임포트
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image  # ROS2 이미지 메시지 타입
from cv_bridge import CvBridge  # ROS 이미지를 OpenCV 이미지로 변환
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QSizePolicy, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QDateTime
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy, QoSDurabilityPolicy
import sys
from std_msgs.msg import String
from geometry_msgs.msg import Point
import json

class CameraViewer(Node):
    def __init__(self, app):
        super().__init__('camera_viewer')
        self.app = app
        self.bridge = CvBridge()
        
        # QoS 설정
        self.qos = rclpy.qos.QoSProfile(
            reliability=rclpy.qos.QoSReliabilityPolicy.BEST_EFFORT,
            durability=rclpy.qos.QoSDurabilityPolicy.VOLATILE,
            history=rclpy.qos.QoSHistoryPolicy.KEEP_LAST,
            depth=1
        )

        # 카메라 토픽 수정 (8개로 제한)
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

        # 구독자 생성
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
            
        # 주차장 상태 구독자 추가
        self.parking_status_subscriber = self.create_subscription(
            String,
            '/parking_status',
            self.parking_status_callback,
            10
        )    

        # 로그 구독자 추가
        self.log_subscriber = self.create_subscription(
            String,
            '/log',
            self.log_callback,
            10
        )

        # 로봇 상태 구독자 추가
        self.robot_state_subscriber = self.create_subscription(
            String,
            '/robot_state',
            self.robot_state_callback,
            10
        )

        # UI 설정
        self.window = QWidget()
        self.main_layout = QHBoxLayout()
        self.window.setLayout(self.main_layout)

        # 좌측 레이아웃 (카메라 화면) 설정
        self.left_layout = QVBoxLayout()
        self.camera_layout = QGridLayout()
        self.camera_layout.setSpacing(2)
        self.camera_layout.setContentsMargins(5, 5, 5, 5)
        self.left_layout.addLayout(self.camera_layout)

        # 우측 레이아웃 설정
        self.right_layout = QVBoxLayout()

        # 메인 레이아웃에 좌우 레이아웃 추가 (2:3 비율)
        self.main_layout.addLayout(self.left_layout, 2)
        self.main_layout.addLayout(self.right_layout, 3)

        # 카메라 이미지를 표시할 라벨 생성 (8개로 제한)
        self.image_labels = []
        for i in range(8):
            label = QLabel()
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("border: 1px solid black; background-color: black;")
            label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            label.setMinimumSize(240, 180)  # 크기 조정
            label.setScaledContents(True)
            label.mousePressEvent = lambda event, index=i: self.show_enlarged(index)
            self.image_labels.append(label)
            self.camera_layout.addWidget(label, i // 2, i % 2)

        # 맵 표시 영역 추가 (크기 확대)
        self.map_label = QLabel("맵")
        self.map_label.setStyleSheet("border: 1px solid black;")
        self.map_label.setAlignment(Qt.AlignCenter)
        self.map_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.right_layout.addWidget(self.map_label, 70)  # 50% 비율 할당

        # 주차장 상태 표시 영역
        self.parking_status_label = QLabel("주차장 상태")
        self.parking_status_label.setStyleSheet("border: 1px solid black;")
        self.parking_status_label.setAlignment(Qt.AlignCenter)
        self.right_layout.addWidget(self.parking_status_label, 15)  # 15% 비율 할당

        # 로그 표시 영역 (QTableWidget으로 변경)
        self.log_table = QTableWidget()
        self.right_layout.addWidget(self.log_table, 10)
        self.log_table.setColumnCount(3)
        self.log_table.setHorizontalHeaderLabels(['시간', '레벨', '메시지'])
        self.log_table.horizontalHeader().setStretchLastSection(True)
        self.log_table.setColumnWidth(0, 150)  # 시간 열의 너비
        self.log_table.setColumnWidth(1, 50)   # 레벨 열의 너비
        self.log_table.verticalHeader().setVisible(False)  # 수직 헤더(인덱스) 숨기기

        # 로봇 상태 표시 영역
        self.robot_status_label = QLabel("로봇 상태")
        self.robot_status_label.setStyleSheet("border: 1px solid black;")
        self.robot_status_label.setAlignment(Qt.AlignCenter)
        self.right_layout.addWidget(self.robot_status_label, 5)  # 20% 비율 할당

        # 윈도우 설정
        screen = self.app.primaryScreen().geometry()
        window_width = screen.width()
        window_height = screen.height()
        self.window.setGeometry(0, 0, window_width, window_height)
        self.window.setWindowTitle('Camera Viewer')
        self.window.show()

    def image_callback(self, msg):
        """ROS 이미지 메시지를 받아서 Qt 라벨에 표시하는 콜백 함수"""
        try:
            topic = msg.header.frame_id.split('_frame')[0] + '/image_raw'
            if topic in self.camera_topics:
                index = self.camera_topics[topic]
                # ROS 이미지를 OpenCV 이미지로 변환
                cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
                h, w, ch = cv_image.shape
                bytes_per_line = ch * w
                # OpenCV 이미지를 Qt 이미지로 변환
                qt_image = QImage(cv_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(qt_image)
                self.image_labels[index].setPixmap(pixmap)
        except Exception as e:
            self.get_logger().error(f'Error processing image: {str(e)}')

    def show_enlarged(self, index):
        """선택한 카메라 화면을 확대하는 함수"""
        if hasattr(self, 'current_enlarged') and self.current_enlarged == index:
            self.restore_original_layout()
            return

        self.current_enlarged = index
        enlarged_label = self.image_labels[index]
        
        # 선택한 화면 외 다른 화면 숨기기
        for i, label in enumerate(self.image_labels):
            if i != index:
                label.hide()
        
        # 선택한 화면을 전체 영역으로 확대
        self.camera_layout.removeWidget(enlarged_label)
        self.camera_layout.addWidget(enlarged_label, 0, 0, 4, 3)
        enlarged_label.setScaledContents(True)

    def restore_original_layout(self):
        """확대된 화면을 원래 레이아웃으로 복원하는 함수"""
        for i, label in enumerate(self.image_labels):
            label.setScaledContents(True)
            self.camera_layout.removeWidget(label)
            label.show()
            self.camera_layout.addWidget(label, i // 2, i % 2)  # 2x4 그리드로 변경
        delattr(self, 'current_enlarged')
        
    
    def parking_status_callback(self, msg):
        """주차장 상태 메시지 수신 시 호출되는 콜백 함수"""
        try:
            parking_status = json.loads(msg.data)
            status_text = f"빈 자리 수: {parking_status['available_spots']}\n"
            status_text += f"만차 여부: {'예' if parking_status['is_full'] else '아니오'}\n"
            status_text += f"대기 차량 수: {parking_status['waiting_vehicles']}"
            self.parking_status_label.setText(status_text)    
            
            self.get_logger().info(f"Parking status updated: {parking_status}")
        except json.JSONDecodeError as e:
            self.get_logger().error(f'Error decoding parking status JSON: {str(e)}')

    def log_callback(self, msg):
        """로그 메시지 수신 시 호출되는 콜백 함수"""
        try:
            log_data = json.loads(msg.data)
            row_position = self.log_table.rowCount()
            self.log_table.insertRow(row_position)
            
            time_item = QTableWidgetItem(QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss"))
            level_item = QTableWidgetItem(log_data['level'])
            message = f"Test log message:[{log_data['level']}]"
            message_item = QTableWidgetItem(message)
            
            self.log_table.setItem(row_position, 0, time_item)
            self.log_table.setItem(row_position, 1, level_item)
            self.log_table.setItem(row_position, 2, message_item)
            
            self.log_table.scrollToBottom()
            
            # 로그 메시지 수신 로깅 추가
            self.get_logger().info(f"Received log message: [{log_data['level']}]")
            
        except json.JSONDecodeError as e:
            self.get_logger().error(f'Error decoding JSON: {str(e)}')

    def robot_state_callback(self, msg):
        """로봇 상태 메시지 수신 시 호출되는 콜백 함수"""
        try:
            robot_state = json.loads(msg.data)
            state_text = f"상태: {robot_state['current_state']}\n"
            state_text += f"위치: X={robot_state['current_position'][0]:.2f}, Y={robot_state['current_position'][1]:.2f}"
            self.robot_status_label.setText(state_text)
            
            # 로봇 상태 메시지 수신 로깅 추가
            self.get_logger().info(f"Received robot state: {robot_state['current_state']}, Position: ({robot_state['current_position'][0]:.2f}, {robot_state['current_position'][1]:.2f})")
        except json.JSONDecodeError as e:
            self.get_logger().error(f'Error decoding JSON: {str(e)}')

    def run(self):
        """ROS2 노드와 Qt 이벤트 루프를 실행하는 함수"""
        while rclpy.ok():
            rclpy.spin_once(self)  # ROS2 콜백 처리
            self.app.processEvents()  # Qt 이벤트 처리

def main(args=None):
    """메인 함수"""
    rclpy.init(args=args)  # ROS2 초기화
    app = QApplication(sys.argv)  # Qt 애플리케이션 생성
    viewer = CameraViewer(app)  # 카메라 뷰어 인스턴스 생성
    viewer.run()  # 실행    
    viewer.destroy_node()  # 노드 종료
    rclpy.shutdown()  # ROS2 종료

if __name__ == '__main__':
    main()
