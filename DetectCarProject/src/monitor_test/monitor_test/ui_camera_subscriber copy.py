#객체 탐지 없지만 작동하는 코드

# PyQt5 모듈 임포트 (GUI 생성에 사용)
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QTimer, QMetaObject, Q_ARG
from PyQt5.QtWidgets import QMessageBox, QApplication

# ROS 2 관련 모듈 임포트 (노드 통신 및 메시지 처리)
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from std_msgs.msg import String  # 로그 메시지 전송용
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge

# 기타 라이브러리 임포트
import cv2
import sys
import numpy as np
import threading
from ultralytics import YOLO  # YOLO 객체 탐지 라이브러리
import time
import math

# 시스템 상태를 나타내는 변수 (1: 준비 상태, 2: 단속 중, 3: 경고 상태)
status = 1

class Ui_Form(object):
    """GUI 초기 설정을 담당하는 클래스"""
    def setupUi(self, Form):
        # 메인 폼 설정
        Form.setObjectName("Form")
        Form.resize(1363, 618)

        # 왼쪽 카메라 레이블 생성 (사용자 클릭 가능)
        self.L_camera_label = ClickableLabel(Form)
        self.L_camera_label.setGeometry(QtCore.QRect(30, 110, 640, 480))
        self.L_camera_label.setFrameShape(QtWidgets.QFrame.Panel)
        self.L_camera_label.setLineWidth(2)
        self.L_camera_label.setAlignment(QtCore.Qt.AlignCenter)

        # 오른쪽 카메라 레이블 생성
        self.R_camera_label = QtWidgets.QLabel(Form)
        self.R_camera_label.setGeometry(QtCore.QRect(690, 110, 640, 480))
        self.R_camera_label.setFrameShape(QtWidgets.QFrame.Panel)
        self.R_camera_label.setLineWidth(2)
        self.R_camera_label.setAlignment(QtCore.Qt.AlignCenter)

        # 상태 레이블 생성
        self.state_label = QtWidgets.QLabel(Form)
        self.state_label.setGeometry(QtCore.QRect(30, 20, 451, 70))
        font = QtGui.QFont()
        font.setPointSize(32)
        font.setBold(True)
        self.state_label.setFont(font)
        self.state_label.setFrameShape(QtWidgets.QFrame.Box)
        self.state_label.setLineWidth(3)
        self.state_label.setAlignment(QtCore.Qt.AlignCenter)
        self.state_label.setStyleSheet("background-color: yellow;")  # 배경색 설정

        # 시간 레이블 그룹 생성
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(510, 20, 400, 70))

        # 경과 시간 레이블 생성
        self.down_time_label = QtWidgets.QLabel(self.groupBox)
        self.down_time_label.setGeometry(QtCore.QRect(10, 40, 350, 25))
        font.setPointSize(16)
        self.down_time_label.setFont(font)

        # 시작 시간 레이블 생성
        self.up_time_label = QtWidgets.QLabel(self.groupBox)
        self.up_time_label.setGeometry(QtCore.QRect(10, 10, 350, 25))
        self.up_time_label.setFont(font)

        # 종료 버튼 생성
        self.pushbutton_1 = QtWidgets.QPushButton(Form)
        self.pushbutton_1.setGeometry(QtCore.QRect(1150, 30, 181, 61))
        font.setPointSize(18)
        self.pushbutton_1.setFont(font)
        self.pushbutton_1.clicked.connect(self.pushbutton1_push)

        # 추적 중단 버튼 생성
        self.pushbutton_2 = QtWidgets.QPushButton(Form)
        self.pushbutton_2.setGeometry(QtCore.QRect(940, 30, 181, 61))
        self.pushbutton_2.setFont(font)
        self.pushbutton_2.setEnabled(False)
        self.pushbutton_2.clicked.connect(self.pushbutton2_push)

        # UI 텍스트 설정
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)


    def retranslateUi(self, Form):
        """UI에 표시될 텍스트를 설정"""
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "음주 운전 도주 차량 검거 시스템"))
        self.L_camera_label.setText(_translate("Form", "Camera 1"))
        self.R_camera_label.setText(_translate("Form", "Camera 2"))
        self.state_label.setText(_translate("Form", "단속 준비 중"))
        self.down_time_label.setText(_translate("Form", "단속 경과 시간 : 00:00:00"))
        self.up_time_label.setText(_translate("Form", "단속 시작 시간 : 2024/11/11/24:00:00"))
        self.pushbutton_1.setText(_translate("Form", "프로그램 종료"))
        self.pushbutton_2.setText(_translate("Form", "차량 추적 중단"))

    def reset_ui(self):
        """UI를 초기화하여 단속 준비 상태로 변경"""
        self.state_label.setText("단속 준비 중")
        self.state_label.setStyleSheet("background-color: yellow;")

    def pushbutton1_push(self):
        """프로그램 종료 또는 단속 중단 버튼"""
        global status

        print("프로그램 종료/단속 중단 버튼 클릭됨")
        if status == 1:
            reply = QMessageBox.question(
                None,
                'Confirm',
                '정말 프로그램을 종료하시겠습니까?',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes
            )
            if reply == QMessageBox.Yes:
                QApplication.instance().quit()
        elif status == 2:
            reply = QMessageBox.question(
                None,
                'Confirm',
                '정말 단속을 중단하시겠습니까?',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes
            )
            if reply == QMessageBox.Yes:
                self.node.set_status(1)
                #status = 1

    def pushbutton2_push(self):
        """추적 중단 버튼"""
        print("추적 중단 버튼 클릭됨")
        reply = QMessageBox.question(
            None,
            'Confirm',
            '정말 차량 추적을 중단하시겠습니까?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes
        )
        if reply == QMessageBox.Yes:
            self.node.set_status(2)
            print("차량 추적 중단 확인됨")


class ClickableLabel(QtWidgets.QLabel):
    """클릭 가능한 QLabel을 위한 클래스"""
    clicked = QtCore.pyqtSignal(int, int)

    def mousePressEvent(self, event):
        """마우스 클릭 이벤트 처리, 클릭 좌표 전달"""
        self.clicked.emit(event.x(), event.y())
        super().mousePressEvent(event)



class CameraNode(Node):
    """ROS 2 카메라 노드 클래스"""
    def __init__(self, ui):
        global status

        super().__init__('camera_subscriber_node')
        self.ui = ui
        print("CameraNode initialized")  # 디버깅용 로그
        self.bridge = CvBridge()
        self.click_points = []  # 클릭된 좌표 저장
        self.yolo_model = YOLO("/home/lsw/ros2_rokey/src/monitor_test/monitor_test/models/best.pt")  # YOLOv8 모델 로드
        status = 1
        self.current_color_index = 0

        # QLabel 클릭 이벤트와 함수 연결
        self.ui.L_camera_label.clicked.connect(self.handle_label_click)

        # QTimer 설정 (상태 색상 변경)
        self.color_timer = QTimer()
        self.color_timer.timeout.connect(self.toggle_label_color)
        self.color_timer.start(1000)  # 1초 간격으로 색상 변경

        # 카메라 데이터 구독 설정
        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=3
        )
        self.subscription_left = self.create_subscription(
            CompressedImage, '/camera/image1/compressed', self.callback_left_camera, qos_profile
        )
        self.subscription_right = self.create_subscription(
            CompressedImage, '/camera/image2/compressed', self.callback_right_camera, qos_profile
        )

        # 디버그 로그 발행자 설정
        self.debug_publisher = self.create_publisher(String, 'debug_logs', 10)


    """@@@@@@@@@@@@@@@@@@@@@@@@@@@@@이미지 처리@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"""

    def display_image(self, cv_image, label):
        """OpenCV 이미지를 QLabel에 표시"""
        rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        q_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
    
        label.setPixmap(QPixmap.fromImage(q_image))

    def callback_right_camera(self, msg):
        """오른쪽 카메라 콜백 처리"""
        np_arr = np.frombuffer(msg.data, np.uint8)
        cv_image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        self.display_image(cv_image, self.ui.R_camera_label)


    def callback_left_camera(self, msg):
        """왼쪽 카메라 콜백 처리, YOLO 탐지 수행"""
        np_arr = np.frombuffer(msg.data, np.uint8)
        self.current_image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        results = self.yolo_model.track(source=self.current_image, conf=0.75, persist=True)
        self.process_detections(results)    # 탐지된 객체 이미지에 표시
        self.update_image_with_diamond()    # 마름모 표시 추가


    def process_detections(self, results):
        """탐지된 객체의 경계 상자 및 클래스 정보를 이미지에 작성"""
        if results[0].boxes is not None:    # 입력 소스가 있을때 동작
            for box in results[0].boxes:    # 박스의 좌표와 클래스 정보를 추출
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = box.conf.item()  # 신뢰도
                cls = int(box.cls.item()) if hasattr(box.cls, 'item') else int(box.cls) # 클래스
                label = f"{results[0].names[cls]} {conf:.2f}"
                cv2.rectangle(self.current_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(self.current_image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


    def update_image_with_diamond(self):
        #생성된 마름모를 현재 이미지에 업데이트
        #클릭된 좌표들을 이용해 마름모를 그리고, 투명도를 적용하여 이미지를 겹쳐서 표시합니다.
        if self.current_image is None:
            return
        
        # 마름모 좌표 순서 정렬
        self.sorted_points = self.sort_diamond_points(self.click_points) 

        # 이미지 복사본 생성
        overlay = self.current_image.copy()

        # 클릭된 각 좌표에 점을 그림
        for point in self.sorted_points:
            cv2.circle(overlay, point, radius=5, color=(0, 0, 255), thickness=-1)

        # 마름모 모양으로 연결하여 채움
        if len(self.sorted_points) == 4:
            pts = np.array(self.sorted_points, np.int32).reshape((-1, 1, 2))
            fill_color = (0, 255, 0)    # 채우기 색상
            alpha = 0.5 # 채우기 투명도

            # 채워진 다각형을 그리고 원본 이미지와 블렌딩
            filled_overlay = overlay.copy()
            cv2.fillPoly(filled_overlay, [pts], fill_color)
            overlay = cv2.addWeighted(filled_overlay, alpha, overlay, 1 - alpha, 0)

            # 마름모의 경계선을 그림
            cv2.polylines(overlay, [pts], isClosed=True, color=(0, 0, 255), thickness=2)

        # 결과 이미지를 QLabel에 표시
        self.display_image(overlay, self.ui.L_camera_label)


    """@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@클릭 좌표 인식 및 마름모 생성@@@@@@@@@@@@@@@@@@@@@@@@@@@"""

    def handle_label_click(self, x, y):
        """라벨 클릭 시 좌표 저장 및 마름모 업데이트"""
        global status

        if status == 1 and len(self.click_points) < 4:
            self.click_points.append((x, y))
            self.log_debug(self.click_points)
            if len(self.click_points) == 4:
                self.click_points = self.sort_diamond_points(self.click_points)
                self.set_status(2)
                self.update_image_with_diamond()


    def sort_diamond_points(self, points):
        """마름모 좌표를 시계 방향으로 정렬"""
        cx = sum(p[0] for p in points) / 4
        cy = sum(p[1] for p in points) / 4
        return sorted(points, key=lambda p: math.atan2(p[1] - cy, p[0] - cx))


    """@@@@@@@@@@@@@@@@@@@@@@@@@@@@상태 관리@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"""

    def set_status(self, new_status):
        """상태를 변경하고 UI를 업데이트"""
        global status

        QMessageBox.information(None, "정보", "set_status 작동함")
        status = new_status
        self.update_ui()


    def update_ui(self):
        """현재 상태에 따라 UI를 업데이트"""
        global status

        QMessageBox.information(None, "정보", "update_ui 작동함")
        if status == 1:
            self.ui.state_label.setText("단속 준비 중")
            self.ui.state_label.setStyleSheet("background-color: yellow;")
            self.ui.pushbutton_1.setText("프로그램 종료")
            self.ui.pushbutton_1.setEnabled(True)
            self.ui.pushbutton_2.setEnabled(False)
            self.click_points = [] # 체크 포인트 초기화
            QMessageBox.information(None, "정보", "status == 1")
        elif status == 2:
            self.ui.state_label.setText("단속 중")
            self.ui.state_label.setStyleSheet("background-color: green;")
            self.ui.pushbutton_1.setText("단속 중단")
            self.ui.pushbutton_1.setEnabled(True)
            self.ui.pushbutton_2.setEnabled(False)
            QMessageBox.information(None, "정보", "status == 2")
        elif status == 3:
            self.ui.state_label.setText("도주 차량 발생")
            self.ui.state_label.setStyleSheet("background-color: red;")
            self.ui.pushbutton_1.setEnabled(False)
            self.ui.pushbutton_2.setEnabled(True)
            QMessageBox.information(None, "정보", "status == 3")

    def toggle_label_color(self):
        """추적 중 또는 경고 상태일 때 상태 라벨 색상 변경"""
        if status == 2:
            colors = ["green", "white"]
        elif status == 3:
            colors = ["red", "blue"]
        else:
            return  # 준비 상태일 때는 색상 변경 없음

        self.current_color_index = (self.current_color_index + 1) % len(colors)
        new_color = colors[self.current_color_index]
        self.ui.state_label.setStyleSheet(f"background-color: {new_color};")



    """@@@@@@@@@@@@@@@@@@@@@@@@@@@디버그@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"""

    def log_debug(self, message):
        """디버그 메시지를 발행하는 함수"""
        debug_msg = String()
        debug_msg.data = str(message)
        self.debug_publisher.publish(debug_msg)



def main(args=None):
    """메인 함수"""
    rclpy.init(args=args)
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()

    # UI 초기화
    ui.setupUi(Form)
    Form.show()

    # CameraNode 초기화 (setupUi 이후에 생성해야 UI 속성을 참조 가능)
    node = CameraNode(ui)
    ui.node = node  # Ui_Form에 CameraNode 연결

    

    # ROS 2 노드 생성 및 실행
    executor = rclpy.executors.SingleThreadedExecutor()
    executor.add_node(node)

    def ros_spin():
        while rclpy.ok():
            rclpy.spin_once(node, timeout_sec=0.1)

    ros_thread = threading.Thread(target=ros_spin, daemon=True)
    ros_thread.start()

    sys.exit(app.exec_())
    rclpy.shutdown()


if __name__ == "__main__":
    main()
