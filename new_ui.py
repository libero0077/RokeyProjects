import sys
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2  # OpenCV 라이브러리

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QDesktopWidget, QMessageBox, QDialog
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets


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



class Ui_Dialog(object):
    def setupUi(self, Dialog):
        # 메인 페이지
        self.Dialog = Dialog
        Dialog.setObjectName("Dialog")
        Dialog.resize(774, 729)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)

        # JOB 작업 그룹
            # JOB 선택 박스
        self.job_comboBox = QtWidgets.QComboBox(Dialog)
        self.job_comboBox.setGeometry(QtCore.QRect(450, 480, 291, 25))
        self.job_comboBox.setObjectName("job_comboBox")
        self.job_comboBox.addItem("")
        self.job_comboBox.addItem("")
        self.job_comboBox.addItem("")

            # JOB 시작 버튼
        self.job_start_button = QtWidgets.QPushButton(Dialog)
        self.job_start_button.setGeometry(QtCore.QRect(450, 510, 89, 31))
        self.job_start_button.setObjectName("job_start_button")

            # JOB 정지 버튼
        # self.job_stop_button = QtWidgets.QPushButton(Dialog)
        # self.job_stop_button.setGeometry(QtCore.QRect(450, 554, 141, 41))
        # self.job_stop_button.setCheckable(False)
        # self.job_stop_button.setObjectName("job_stop_button")

            # JOB 일시정지 버튼
        self.job_pause_button = QtWidgets.QPushButton(Dialog)
        self.job_pause_button.setGeometry(QtCore.QRect(550, 510, 89, 31))
        self.job_pause_button.setCheckable(False)
        self.job_pause_button.setObjectName("job_pause_button")

            # JOB 동작 재개 버튼
        self.job_resume_button = QtWidgets.QPushButton(Dialog)
        self.job_resume_button.setGeometry(QtCore.QRect(650, 510, 89, 31))
        self.job_resume_button.setCheckable(False)
        self.job_resume_button.setObjectName("job_resume_button")

            # JOB 초기화 버튼
        self.job_reset_button = QtWidgets.QPushButton(Dialog)
        #self.job_reset_button.setGeometry(QtCore.QRect(600, 554, 141, 41)) #나중에 STOP 추가시 크기 조절
        self.job_reset_button.setGeometry(QtCore.QRect(450, 550, 291, 41))
        self.job_reset_button.setCheckable(False)
        self.job_reset_button.setObjectName("job_reset_button")

        # 비상정지 버튼
        self.emergencystop_button = QtWidgets.QPushButton(Dialog)
        self.emergencystop_button.setGeometry(QtCore.QRect(40, 604, 701, 81))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.emergencystop_button.setFont(font)
        self.emergencystop_button.setAutoFillBackground(False)
        self.emergencystop_button.setObjectName("emergencystop_button")

        # 로봇 상태 라벨
        self.robot_status_label = QtWidgets.QLabel(Dialog)
        self.robot_status_label.setGeometry(QtCore.QRect(40, 10, 701, 61))
        font = QtGui.QFont()
        font.setPointSize(32)
        self.robot_status_label.setFont(font)
        self.robot_status_label.setFrameShape(QtWidgets.QFrame.Box)
        self.robot_status_label.setAlignment(QtCore.Qt.AlignCenter)
        self.robot_status_label.setObjectName("robot_status_label")

        # 작업 소요 시간 라벨
        self.processing_time_label = QtWidgets.QLabel(Dialog)
        self.processing_time_label.setGeometry(QtCore.QRect(450, 450, 291, 17))
        self.processing_time_label.setObjectName("processing_time_label")

        # 영상 출력 하는 라벨
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

        # 학습 데이터 수집 버튼
        self.collect_data_button = QtWidgets.QPushButton(Dialog)
        self.collect_data_button.setGeometry(QtCore.QRect(310, 450, 131, 141))
        self.collect_data_button.setObjectName("collect_data_button")

        # 이메일 그룹
            # 이메일 입력 텍스트 박스
        self.email_textbox = QtWidgets.QTextEdit(Dialog)
        self.email_textbox.setGeometry(QtCore.QRect(400, 690, 241, 31))
        self.email_textbox.setObjectName("email_textbox")

            # 이메일 저장 버튼
        self.email_save_button = QtWidgets.QPushButton(Dialog)
        self.email_save_button.setGeometry(QtCore.QRect(650, 690, 89, 31))
        self.email_save_button.setObjectName("email_save_button")

            # "관리자 이메일"을 나타내는 라벨 수정 불필요
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(300, 690, 91, 31))
        self.label_3.setObjectName("label_3")

        # 컨베이어 수동 조작 그룹
            # 컨베이어 속도 조절 슬라이드
        self.conveyor_control_slider = QtWidgets.QSlider(Dialog)
        self.conveyor_control_slider.setEnabled(True)
        self.conveyor_control_slider.setGeometry(QtCore.QRect(40, 500, 261, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.conveyor_control_slider.setFont(font)
        self.conveyor_control_slider.setMinimum(0)
        self.conveyor_control_slider.setMaximum(99)
        self.conveyor_control_slider.setOrientation(QtCore.Qt.Horizontal)
        self.conveyor_control_slider.setObjectName("conveyor_control_slider")

            # 컨베이어 수동 조작 체크 버튼
        self.conveyor_control_radio = QtWidgets.QRadioButton(Dialog)
        self.conveyor_control_radio.setGeometry(QtCore.QRect(40, 450, 141, 23))
        self.conveyor_control_radio.setObjectName("conveyor_control_radio")

            # 컨베이어 방향 전환 버튼들
        self.conveyor_move_right = QtWidgets.QPushButton(Dialog)
        self.conveyor_move_right.setGeometry(QtCore.QRect(180, 520, 121, 31))
        self.conveyor_move_right.setObjectName("conveyor_move_right")
        self.conveyor_move_left = QtWidgets.QPushButton(Dialog)
        self.conveyor_move_left.setGeometry(QtCore.QRect(40, 520, 121, 31))
        self.conveyor_move_left.setObjectName("conveyor_move_left")

            # 컨베이어 작동 정지 버튼
        self.conveyor_move_stop = QtWidgets.QPushButton(Dialog)
        self.conveyor_move_stop.setGeometry(QtCore.QRect(40, 560, 261, 31))
        self.conveyor_move_stop.setObjectName("conveyor_move_stop")

            # 컨베이어 라벨 관련
        self.label_1 = QtWidgets.QLabel(Dialog)
        self.label_1.setGeometry(QtCore.QRect(40, 480, 261, 17))
        self.label_1.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.label_1.setObjectName("label_1")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(40, 480, 261, 20))
        self.label_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate

        # 화면에 출력될 텍스트
        Dialog.setWindowTitle(_translate("Dialog", "Team 5"))

        # 영상 출력할 라벨
        self.media_label.setText(_translate("Dialog", "Media"))

        # 로봇 상태 라벨
        self.robot_status_label.setText(_translate("Dialog", "robot status"))

        # 비상 정지 버튼
        self.emergencystop_button.setText(_translate("Dialog", "EmergencyStop"))

        # JOB 관련
            # JOB 작업 소요 시간 라벨
        self.processing_time_label.setText(_translate("Dialog", "작업 소요 시간"))

            # JOB 버튼들
        self.job_start_button.setText(_translate("Dialog", "START"))
        self.job_pause_button.setText(_translate("Dialog", "PAUSE"))
        self.job_resume_button.setText(_translate("Dialog", "RESUME"))
        self.job_reset_button.setText(_translate("Dialog", "RESET"))

            # JOB 선택 콤보 박스 (밑에 추가하면 JOB 추가 가능)
        self.job_comboBox.setItemText(0, _translate("Dialog", "Job1"))
        self.job_comboBox.setItemText(1, _translate("Dialog", "Job2"))
        self.job_comboBox.setItemText(2, _translate("Dialog", "Job3"))

        # 관리자 이메일 관련
        self.email_save_button.setText(_translate("Dialog", "저장"))
        self.label_3.setText(_translate("Dialog", "관리자 이메일 "))

        # 학습 데이터 수집
        self.collect_data_button.setText(_translate("Dialog", "학습 데이터 수집"))
        
        # 컨베이어 수동 조작
        self.conveyor_control_radio.setText(_translate("Dialog", "컨베이어 수동 조작"))
        self.label_1.setText(_translate("Dialog", "0                                                                 100"))
        self.label_2.setText(_translate("Dialog", "컨베이어 속도"))
        
            # 컨베이어 수동 조작 버튼
        self.conveyor_move_right.setText(_translate("Dialog", "오른쪽으로"))
        self.conveyor_move_left.setText(_translate("Dialog", "왼쪽으로"))
        self.conveyor_move_stop.setText(_translate("Dialog", "컨베이어 정지"))



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
        self.webcam_node = WebcamViewerNode(self.ui.media_label)

        # 버튼 클릭 이벤트 연결
        self.ui.emergencystop_button.clicked.connect(self.handle_emergencystop_button)
        self.ui.job_start_button.clicked.connect(self.handle_job_start_button)
        self.ui.job_pause_button.clicked.connect(self.handle_job_pause_button)
        self.ui.job_resume_button.clicked.connect(self.handle_job_resume_button)
        self.ui.job_reset_button.clicked.connect(self.handle_job_reset_button)
        self.ui.email_save_button.clicked.connect(self.handle_email_save_button)
        self.ui.collect_data_button.clicked.connect(self.handle_collect_data_button)
        self.ui.conveyor_move_right.clicked.connect(self.handle_conveyor_move_right)
        self.ui.conveyor_move_left.clicked.connect(self.handle_conveyor_move_left)
        self.ui.conveyor_move_stop.clicked.connect(self.handle_conveyor_move_stop)
        
        # 라디오 버튼 클릭 이벤트 연결
        self.ui.conveyor_control_radio.clicked.connect(self.handle_conveyor_control_radio)


        # ROS2 스핀을 위한 타이머 설정
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.spin_ros2)
        self.timer.start(10)  # 10ms 간격으로 ROS2 spin 실행

    def spin_ros2(self):
        rclpy.spin_once(self.webcam_node, timeout_sec=0)

    def closeEvent(self, event):
        self.webcam_node.destroy_node()
        rclpy.shutdown()
        super().closeEvent(event)


    # 이벤트 핸들러
    def handle_emergencystop_button(self):
        print("비상 정지 버튼 클릭")

    def handle_job_start_button(self):
        print("JOB 시작 버튼 클릭")

    def handle_job_pause_button(self):
        print("JOB 일시 정지 버튼 클릭")

    def handle_job_resume_button(self):
        print("JOB 작업 재개 버튼 클릭")

    def handle_job_reset_button(self):
        print("JOB 리셋 버튼 클릭")

    def handle_email_save_button(self):
        print("이메일 저장 버튼 클릭")

    def handle_collect_data_button(self):
        print("학습 데이터 수집 버튼 클릭")

    def handle_conveyor_move_right(self):
        print("컨베이어 오른쪽 이동 버튼 클릭")

    def handle_conveyor_move_left(self):
        print("컨베이어 왼쪽 이동 버튼 클릭")

    def handle_conveyor_move_stop(self):
        print("컨베이어 정지 버튼 클릭")

    # 컨베이어 라디오 버튼 클릭 이벤트
    def handle_conveyor_control_radio(self):
        print("컨베이어 수동 조작 라디오 버튼 클릭")

    
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 로그인창 생성
    login_window = Login()
    login_window.show()

    # 매인 앱 실행
    #main_window = MainApp()
    #main_window.show()

    sys.exit(app.exec_())