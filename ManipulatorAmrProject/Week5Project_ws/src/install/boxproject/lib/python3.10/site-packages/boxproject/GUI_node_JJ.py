import sys
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from PyQt5 import QtCore, QtGui, QtWidgets
import cv2  # OpenCV 라이브러리
## 로그인 함수 ##
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QDesktopWidget, QMessageBox, QDialog
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets
## 액션 관련 ##
from rclpy.action import ActionClient
from boxproject_interfaces.action import TaskAction  # TaskAction은 사용자 정의 액션 인터페이스


############################## 로그인 관련 #################################
class Login(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('시스템 로그인')
        self.resize(450, 350)  # 초기 창 크기
        self.setMinimumSize(300, 250)  # 최소 창 크기 설정
        self.setStyleSheet("background-color: #F5F6F7;")
        
        # 창을 화면에 배치
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        layout.addStretch(1)  # 상단 여백

        # 로그인 제목
        title_label = QLabel('로그인')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont('Arial', 24, QFont.Bold))
        layout.addWidget(title_label)

        layout.addStretch(1)  # 제목과 입력 필드 사이 여백

        # 아이디 입력
        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("아이디")
        self.id_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #DADADA;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
                background-color: white;
            }
        """)
        layout.addWidget(self.id_input)

        # 비밀번호 입력
        self.pw_input = QLineEdit()
        self.pw_input.setPlaceholderText("비밀번호")
        self.pw_input.setEchoMode(QLineEdit.Password)
        self.pw_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #DADADA;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
                background-color: white;
            }
        """)
        layout.addWidget(self.pw_input)

        layout.addStretch(1)  # 입력 필드와 버튼 사이 여백

        # 로그인 버튼
        login_button = QPushButton("로그인")
        login_button.setStyleSheet("""
            QPushButton {
                background-color: #1E90FF;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 15px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5ACCFF;
            }
        """)
        login_button.clicked.connect(self.login)
        layout.addWidget(login_button)

        layout.addStretch(1)  # 하단 여백

        self.setLayout(layout)

    def login(self):
        # 로그인 로직은 그대로 유지
        login_id = "b5"
        login_pw = "rokey"
    
        user_id = self.id_input.text()
        user_pw = self.pw_input.text()

        if user_id == login_id and user_pw == login_pw:
            QMessageBox.information(self, "로그인 성공", "시스템 접속")
            self.open_main_window()
        else:
            QMessageBox.warning(self, "로그인 실패", "아이디 또는 비밀번호가 올바르지 않습니다.")

    def open_main_window(self):
        self.main_window = MainApp()  # MainApp을 직접 호출
        self.main_window.show()
        self.close()
###################################로그인 관련 ###############################################################

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        self.Dialog = Dialog
        Dialog.setObjectName("Dialog")
        Dialog.resize(774, 756)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.job_start_button = QtWidgets.QPushButton(Dialog)
        self.job_start_button.setGeometry(QtCore.QRect(450, 510, 89, 41))
        self.job_start_button.setObjectName("job_start_button")
        self.job_stop_button = QtWidgets.QPushButton(Dialog)
        self.job_stop_button.setGeometry(QtCore.QRect(450, 554, 141, 41))
        self.job_stop_button.setObjectName("job_stop_button")
        self.job_pause_button = QtWidgets.QPushButton(Dialog)
        self.job_pause_button.setGeometry(QtCore.QRect(550, 510, 89, 41))
        self.job_pause_button.setObjectName("job_pause_button")
        self.emergencystop_button = QtWidgets.QPushButton(Dialog)
        self.emergencystop_button.setGeometry(QtCore.QRect(40, 604, 701, 81))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.emergencystop_button.setFont(font)
        self.emergencystop_button.setAutoFillBackground(False)
        self.emergencystop_button.setObjectName("emergencystop_button")
        self.robot_status_label = QtWidgets.QLabel(Dialog)
        self.robot_status_label.setGeometry(QtCore.QRect(40, 10, 701, 61))
        font = QtGui.QFont()
        font.setPointSize(32)
        self.robot_status_label.setFont(font)
        self.robot_status_label.setFrameShape(QtWidgets.QFrame.Box)
        self.robot_status_label.setAlignment(QtCore.Qt.AlignCenter)
        self.robot_status_label.setObjectName("robot_status_label")
        self.processing_time_label = QtWidgets.QLabel(Dialog)
        self.processing_time_label.setGeometry(QtCore.QRect(450, 450, 291, 17))
        self.processing_time_label.setObjectName("processing_time_label")
        self.move_forward_button = QtWidgets.QPushButton(Dialog)
        self.move_forward_button.setGeometry(QtCore.QRect(130, 454, 89, 36))
        self.move_forward_button.setTabletTracking(False)
        self.move_forward_button.setObjectName("move_forward_button")
        self.move_backward_button = QtWidgets.QPushButton(Dialog)
        self.move_backward_button.setGeometry(QtCore.QRect(130, 560, 89, 36))
        self.move_backward_button.setObjectName("move_backward_button")
        self.move_turnright_button = QtWidgets.QPushButton(Dialog)
        self.move_turnright_button.setGeometry(QtCore.QRect(228, 500, 81, 51))
        self.move_turnright_button.setObjectName("move_turnright_button")
        self.move_turnleft_button = QtWidgets.QPushButton(Dialog)
        self.move_turnleft_button.setGeometry(QtCore.QRect(40, 500, 81, 51))
        self.move_turnleft_button.setObjectName("move_turnleft_button")
        self.job_comboBox = QtWidgets.QComboBox(Dialog)
        self.job_comboBox.setGeometry(QtCore.QRect(450, 480, 291, 25))
        self.job_comboBox.setObjectName("job_comboBox")
        self.job_comboBox.addItem("")
        self.job_comboBox.addItem("")
        self.job_comboBox.addItem("")
        self.media_label = QtWidgets.QLabel(Dialog)
        self.media_label.setGeometry(QtCore.QRect(40, 80, 701, 361))
        font = QtGui.QFont()
        font.setPointSize(30)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.media_label.setFont(font)
        self.media_label.setAutoFillBackground(False)
        self.media_label.setFrameShape(QtWidgets.QFrame.Panel)
        self.media_label.setFrameShadow(QtWidgets.QFrame.Plain)
        self.media_label.setAlignment(QtCore.Qt.AlignCenter)
        self.media_label.setObjectName("media_label")
        self.move_10cm_button = QtWidgets.QPushButton(Dialog)
        self.move_10cm_button.setGeometry(QtCore.QRect(320, 450, 89, 25))
        self.move_10cm_button.setObjectName("move_10cm_button")
        self.move_1cm_button = QtWidgets.QPushButton(Dialog)
        self.move_1cm_button.setGeometry(QtCore.QRect(320, 510, 89, 25))
        self.move_1cm_button.setObjectName("move_1cm_button")
        self.move_1mm_button = QtWidgets.QPushButton(Dialog)
        self.move_1mm_button.setGeometry(QtCore.QRect(320, 540, 89, 25))
        self.move_1mm_button.setObjectName("move_1mm_button")
        self.collect_data_button = QtWidgets.QPushButton(Dialog)
        self.collect_data_button.setGeometry(QtCore.QRect(40, 690, 701, 25))
        self.collect_data_button.setObjectName("collect_data_button")
        self.email_textbox = QtWidgets.QTextEdit(Dialog)
        self.email_textbox.setGeometry(QtCore.QRect(400, 720, 241, 31))
        self.email_textbox.setObjectName("email_textbox")
        self.email_save_button = QtWidgets.QPushButton(Dialog)
        self.email_save_button.setGeometry(QtCore.QRect(650, 720, 89, 31))
        self.email_save_button.setObjectName("email_save_button")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(300, 720, 91, 31))
        self.label_4.setObjectName("label_4")
        self.move_stop_button = QtWidgets.QPushButton(Dialog)
        self.move_stop_button.setGeometry(QtCore.QRect(130, 500, 89, 51))
        self.move_stop_button.setObjectName("move_stop_button")
        self.move_5cm_button = QtWidgets.QPushButton(Dialog)
        self.move_5cm_button.setGeometry(QtCore.QRect(320, 480, 89, 25))
        self.move_5cm_button.setObjectName("move_5cm_button")
        self.job_pause_button_2 = QtWidgets.QPushButton(Dialog)
        self.job_pause_button_2.setGeometry(QtCore.QRect(650, 510, 89, 41))
        self.job_pause_button_2.setObjectName("job_pause_button_2")
        self.job_stop_button_2 = QtWidgets.QPushButton(Dialog)
        self.job_stop_button_2.setGeometry(QtCore.QRect(600, 554, 141, 41))
        self.job_stop_button_2.setObjectName("job_stop_button_2")
        self.move_1mm_button_2 = QtWidgets.QPushButton(Dialog)
        self.move_1mm_button_2.setGeometry(QtCore.QRect(320, 570, 89, 25))
        self.move_1mm_button_2.setObjectName("move_1mm_button_2")
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Team 5"))
        self.job_start_button.setText(_translate("Dialog", "START"))
        self.job_stop_button.setText(_translate("Dialog", "STOP"))
        self.job_pause_button.setText(_translate("Dialog", "PAUSE"))
        self.emergencystop_button.setText(_translate("Dialog", "EmergencyStop"))
        self.robot_status_label.setText(_translate("Dialog", "robot status"))
        self.processing_time_label.setText(_translate("Dialog", "작업 소요 시간"))
        self.move_forward_button.setText(_translate("Dialog", "▲"))
        self.move_backward_button.setText(_translate("Dialog", "▼"))
        self.move_turnright_button.setText(_translate("Dialog", ":앞쪽_화살표:"))
        self.move_turnleft_button.setText(_translate("Dialog", ":뒤쪽_화살표:"))
        self.job_comboBox.setItemText(0, _translate("Dialog", "Job1"))
        self.job_comboBox.setItemText(1, _translate("Dialog", "Job2"))
        self.job_comboBox.setItemText(2, _translate("Dialog", "Job3"))
        self.media_label.setText(_translate("Dialog", "Media"))
        self.move_10cm_button.setText(_translate("Dialog", "10cm"))
        self.move_1cm_button.setText(_translate("Dialog", "1cm"))
        self.move_1mm_button.setText(_translate("Dialog", "1mm"))
        self.collect_data_button.setText(_translate("Dialog", "학습 데이터 수집"))
        self.email_save_button.setText(_translate("Dialog", "저장"))
        self.label_4.setText(_translate("Dialog", "관리자 이메일 "))
        self.move_stop_button.setText(_translate("Dialog", "■"))
        self.move_5cm_button.setText(_translate("Dialog", "5cm"))
        self.job_pause_button_2.setText(_translate("Dialog", "RESUME"))
        self.job_stop_button_2.setText(_translate("Dialog", "RESET"))
        self.move_1mm_button_2.setText(_translate("Dialog", "1mm"))


################################ GUI "media_label" 부분에 실시간 웹캠 카메라 스트리밍 ##############################
class WebcamViewerNode(Node):
    def __init__(self, media_label):
        super().__init__('webcam_viewer')  # 노드 이름 설정

        # 웹캠으로부터 실시간 영상을 서브스크라이브 하는 부분
        self.subscription = self.create_subscription(Image, 'webcam/image_raw', self.image_callback, 10)
        self.bridge = CvBridge()  # OpenCV와 ROS 메시지 변환을 위한 브리지 객체
        self.media_label = media_label 

    # 웹캠으로부터 실시간 영상을 서브스크라이브하는 콜백함수
    def image_callback(self, msg):
        try:
            frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
            pixmap = QtGui.QPixmap.fromImage(qt_image)

            self.media_label.setPixmap(pixmap) # QLabel에 Pixmap 설정 (GUI 업데이트)
        except Exception as e:
            self.get_logger().error(f"Failed to process image: {e}")

class MainApp(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        rclpy.init()
        
        # ROS 2 초기화 및 노드 생성
        self.ros_node = rclpy.create_node('gui_node')
        self.action_client = ActionClient(self.ros_node, TaskAction, '/robot_arm_task')


        self.webcam_node = WebcamViewerNode(self.ui.media_label)

        # ROS2 스핀을 위한 타이머 설정
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.spin_ros2)
        self.timer.start(10)  # 10ms 간격으로 ROS2 spin 실행

        # 버튼 클릭 이벤트 연결
        self.ui.job_start_button.clicked.connect(self.start_task)
        self.ui.job_stop_button.clicked.connect(self.stop_task)
        self.ui.job_pause_button.clicked.connect(self.pause_task)
        self.ui.job_pause_button_2.clicked.connect(self.resume_task)
        self.ui.job_stop_button_2.clicked.connect(self.reset_task)
        self.ui.emergencystop_button.clicked.connect(self.emergency_stop)

    def spin_ros2(self):
        """ROS2 노드 스핀"""
        rclpy.spin_once(self.ros_node, timeout_sec=0)
        rclpy.spin_once(self.webcam_node, timeout_sec=0)

    def closeEvent(self, event):
        """GUI 종료 시 ROS2 노드 종료"""
        self.ros_node.destroy_node()
        self.webcam_node.destroy_node()
        rclpy.shutdown()
        super().closeEvent(event)

################################ GUI "media_label" 부분에 실시간 웹캠 카메라 스트리밍 ##############################

    def send_goal(self, task_name):
        """로봇팔 액션 서버에 작업 요청"""
        if not self.action_client.wait_for_server(timeout_sec=5.0):
            QMessageBox.critical(self, "오류", "로봇팔 서버와 연결할 수 없습니다.")
            return None

        goal_msg = TaskAction.Goal()
        goal_msg.task = task_name
        self.ros_node.get_logger().info(f"Sending goal: {task_name}")

        # Goal 요청
        future = self.action_client.send_goal_async(goal_msg, feedback_callback=self.feedback_callback)
        future.add_done_callback(self.goal_response_callback)
        return future

    def goal_response_callback(self, future):
        """Goal 응답 콜백"""
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.ros_node.get_logger().info("Goal rejected")
            QMessageBox.warning(self, "오류", "작업 요청이 거부되었습니다.")
            return
        self.ros_node.get_logger().info("Goal accepted")
        self.result_future = goal_handle.get_result_async()
        self.result_future.add_done_callback(self.result_callback)

    def feedback_callback(self, feedback_msg):
        """피드백 콜백"""
        feedback = feedback_msg.feedback
        self.ui.robot_status_label.setText(f"상태: {feedback.status}")  # status 필드 수정

    def result_callback(self, future):
        """결과 콜백"""
        result = future.result().result
        self.ui.robot_status_label.setText(f"완료: {result.result}")  # result 필드 수정
        QMessageBox.information(self, "완료", result.result)
        
    # 버튼 이벤트 핸들러
    def start_task(self):
        task_name = self.ui.job_comboBox.currentText()
        if task_name:
            self.send_goal(task_name)

    def stop_task(self):
        QMessageBox.information(self, "알림", "Stop은 현재 작업을 취소합니다.")
        self.action_client.cancel_all_goals()

    def pause_task(self):
        QMessageBox.information(self, "알림", "Pause 기능은 별도의 상태 처리를 통해 구현됩니다.")
        # Pause는 현재는 직접적으로 액션 인터페이스에 포함되지 않았습니다.

    def resume_task(self):
        QMessageBox.information(self, "알림", "Resume 기능은 별도의 상태 처리를 통해 구현됩니다.")
        # Resume은 현재는 직접적으로 액션 인터페이스에 포함되지 않았습니다.

    def reset_task(self):
        QMessageBox.information(self, "알림", "Reset 명령은 새로운 Goal로 동작합니다.")
        self.send_goal("reset")

    def emergency_stop(self):
        QMessageBox.critical(self, "경고", "Emergency Stop 명령 실행")
        self.action_client.cancel_all_goals()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = Login()
    login_window.show()
    sys.exit(app.exec_())

# ros2 run으로 실행시키려면 다음 코드를 활성화
'''def main(args=None):
    app = QtWidgets.QApplication(sys.argv)  # PyQt 애플리케이션 생성
    main_app = MainApp()  # PyQt GUI와 ROS2 통합
    main_app.show()  # GUI 표시
    sys.exit(app.exec_())  # 이벤트 루프 실행 및 종료'''