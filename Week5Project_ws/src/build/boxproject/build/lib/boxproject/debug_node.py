import sys
import json
import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, QThread
from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QPushButton, QRadioButton, QTextEdit, QLabel, QApplication
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge
import smtplib
from email.mime.text import MIMEText


class TestNode(Node):
    def __init__(self):
        super().__init__('test_node')

        self.textbox = None  # 초기값은 None으로 설정

        # ROS2 퍼블리셔
        self.robot_status_publisher = self.create_publisher(String, 'robot_status', 10)
        self.webcam_publisher = self.create_publisher(Image, 'webcam/image_raw', 10)

        # ROS2 서브스크라이버
        self.create_subscription(String, 'conveyor_state', self.conveyor_callback, 10)
        self.create_subscription(String, 'emergency_stop', self.emergency_callback, 10)  # 비상정지 메시지 구독

        # OpenCV - ROS 메시지 변환 브리지
        self.bridge = CvBridge()

        # 카메라 초기화
        self.camera_index = self.detect_camera_index()
        self.camera = cv2.VideoCapture(self.camera_index) if self.camera_index is not None else None

        # 자동 상태 전송 관련 설정
        self.automatic_mode = False
        self.status_list = ["대기중", "작동중", "일시정지"]
        self.current_status_index = 0

        # GUI에서 업데이트를 위한 콜백
        self.update_camera_display = None
        self.update_emergency_textbox = None  # 비상정지 텍스트 박스 업데이트 콜백

    def conveyor_callback(self, msg):
        """conveyor_state 메시지 수신 콜백"""
        text = msg.data
        self.get_logger().info(f"Received conveyor state: {text}")
        self.update_textbox(text)

    def emergency_callback(self, msg):
        """emergency_stop 메시지 수신 콜백"""
        text = msg.data
        self.get_logger().info(f"Received emergency stop: {text}")
        if self.update_emergency_textbox:
            self.update_emergency_textbox(text)

    def update_textbox(self, text):
        """GUI 텍스트 박스 업데이트"""
        if hasattr(self, 'textbox'):
            self.textbox.append(text)

    def publish_robot_status(self, status):
        """robot_status 메시지 퍼블리시"""
        msg = String()
        msg.data = status
        self.robot_status_publisher.publish(msg)
        self.get_logger().info(f"Published robot status: {status}")

    def automatic_status_update(self):
        """자동 상태 전송"""
        if self.automatic_mode:
            self.publish_robot_status(self.status_list[self.current_status_index])
            self.current_status_index = (self.current_status_index + 1) % len(self.status_list)

    def detect_camera_index(self):
        """사용 가능한 카메라 인덱스를 자동으로 탐지"""
        for index in range(10):  # 최대 10개 카메라 인덱스 시도
            cap = cv2.VideoCapture(index)
            if cap.isOpened():
                cap.release()
                return index
        return None

    def publish_webcam(self):
        """웹캠 영상을 퍼블리시하고 GUI에 표시"""
        if self.camera and self.camera.isOpened():
            ret, frame = self.camera.read()
            if ret:
                # ROS 메시지로 퍼블리시
                msg = self.bridge.cv2_to_imgmsg(frame, encoding='bgr8')
                self.webcam_publisher.publish(msg)
                self.get_logger().info("Published webcam frame")

                # GUI 디스플레이 업데이트
                if self.update_camera_display:
                    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    h, w, ch = rgb_image.shape
                    bytes_per_line = ch * w
                    qt_image = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
                    pixmap = QtGui.QPixmap.fromImage(qt_image)
                    self.update_camera_display(pixmap)


class TestApp(QtWidgets.QWidget):
    def __init__(self, node):
        super().__init__()
        self.node = node
        
        # UI 초기화
        self.node.textbox, self.camera_label, self.emergency_textbox = self.init_ui()

        # ROS2 타이머
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.spin_ros2)
        self.timer.start(10)

        # 자동 상태 전송 타이머
        self.auto_timer = QTimer(self)
        self.auto_timer.timeout.connect(self.node.automatic_status_update)

        # 웹캠 퍼블리시 타이머
        self.webcam_timer = QTimer(self)
        self.webcam_timer.timeout.connect(self.node.publish_webcam)
        self.webcam_timer.start(50)

        # GUI에서 카메라 디스플레이 업데이트 함수 연결
        self.node.update_camera_display = self.update_camera_display

        self.node.update_emergency_textbox = self.update_emergency_textbox  # 비상정지 메시지 업데이트 연결

    def init_ui(self):
        """UI 초기화"""
        layout = QVBoxLayout()

        # 텍스트 박스 (conveyor_state 메시지 출력)
        textbox = QTextEdit(self)
        textbox.setReadOnly(True)
        layout.addWidget(QLabel("Conveyor State:"))
        layout.addWidget(textbox)

        # 텍스트 박스 (emergency_stop 메시지 출력)
        emergency_textbox = QTextEdit(self)
        emergency_textbox.setReadOnly(True)
        layout.addWidget(QLabel("Emergency Stop Messages:"))
        layout.addWidget(emergency_textbox)

        # 상태 전송 버튼
        btn_idle = QPushButton("대기중", self)
        btn_idle.clicked.connect(lambda: self.node.publish_robot_status("대기중"))
        layout.addWidget(btn_idle)

        btn_running = QPushButton("작동중", self)
        btn_running.clicked.connect(lambda: self.node.publish_robot_status("작동중"))
        layout.addWidget(btn_running)

        btn_paused = QPushButton("일시정지", self)
        btn_paused.clicked.connect(lambda: self.node.publish_robot_status("일시정지"))
        layout.addWidget(btn_paused)

        # 자동 상태 전송 라디오 버튼
        auto_radio = QRadioButton("자동 상태 전송", self)
        auto_radio.toggled.connect(self.toggle_auto_mode)
        layout.addWidget(auto_radio)

        # 이메일 전송 GUI
        layout.addWidget(QLabel("이메일 전송"))
        self.email_to = QLineEdit(self)
        self.email_to.setPlaceholderText("받는 사람 이메일")
        layout.addWidget(self.email_to)

        self.email_subject = QLineEdit(self)
        self.email_subject.setPlaceholderText("이메일 제목")
        layout.addWidget(self.email_subject)

        self.email_body = QTextEdit(self)
        self.email_body.setPlaceholderText("이메일 내용")
        layout.addWidget(self.email_body)

        send_email_button = QPushButton("이메일 전송", self)
        send_email_button.clicked.connect(self.send_email)
        layout.addWidget(send_email_button)

        # 웹캠 디스플레이
        camera_label = QLabel(self)
        camera_label.setFixedSize(640, 480)
        layout.addWidget(QLabel("Camera View:"))
        layout.addWidget(camera_label)

        # 레이아웃 설정
        self.setLayout(layout)
        self.setWindowTitle("Test Node")
        self.resize(800, 600)

        return textbox, camera_label, emergency_textbox

    def toggle_auto_mode(self, checked):
        """자동 상태 전송 모드 토글"""
        self.node.automatic_mode = checked
        if checked:
            self.auto_timer.start(2000)  # 2초마다 상태 변경
        else:
            self.auto_timer.stop()

    def send_email(self):
        recipient = self.email_to.text()
        subject = self.email_subject.text()
        content = self.email_body.toPlainText()

        self.email_thread = EmailSenderThread(recipient, subject, content)
        self.email_thread.start()

    def spin_ros2(self):
        """ROS2 스핀"""
        rclpy.spin_once(self.node, timeout_sec=0)

    def update_camera_display(self, pixmap):
        """카메라 화면을 QLabel에 업데이트"""
        self.camera_label.setPixmap(pixmap)

    def update_emergency_textbox(self, text):
        """Emergency Stop 텍스트 박스 업데이트"""
        self.emergency_textbox.append(text)


class EmailSenderThread(QThread):
    def __init__(self, recipient, subject, content, parent=None):
        super().__init__(parent)
        self.recipient = recipient
        self.subject = subject
        self.content = content

    def run(self):
        try:
            # SMTP 설정
            smtp_server = "smtp.gmail.com"
            smtp_port = 587
            sender_email = "doosan.rokey.b5@gmail.com"  # 비밀번호 : rokey1234
            sender_password = "tcbd gasi edjk sazv"

            # SMTP 서버 연결
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, sender_password)

            # 이메일 생성
            msg = MIMEText(self.content)
            msg["Subject"] = self.subject
            msg["From"] = sender_email
            msg["To"] = self.recipient

            # 이메일 전송
            server.sendmail(sender_email, self.recipient, msg.as_string())
            server.quit()

            print("이메일 전송 성공!")
        except Exception as e:
            print(f"이메일 전송 실패: {e}")

def main(args=None):
    rclpy.init(args=args)
    test_node = TestNode()

    app = QApplication(sys.argv)
    test_app = TestApp(test_node)
    test_app.show()

    sys.exit(app.exec_())
    test_node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
