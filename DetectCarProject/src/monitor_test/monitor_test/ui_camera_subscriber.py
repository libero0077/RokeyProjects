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

# 시스템 상태를 나타내는 변수 (0: 좌표 보정, 1: 준비 상태, 2: 단속 중, 3: 경고 상태)
status = 0

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
        self.prg_exit_bt = QtWidgets.QPushButton(Form)
        self.prg_exit_bt.setGeometry(QtCore.QRect(1150, 30, 181, 61))
        font.setPointSize(18)
        self.prg_exit_bt.setFont(font)
        self.prg_exit_bt.clicked.connect(self.prg_exit_bt_push)

        # 추적 중단 버튼 생성
        self.stop_bt = QtWidgets.QPushButton(Form)
        self.stop_bt.setGeometry(QtCore.QRect(940, 30, 181, 61))
        self.stop_bt.setFont(font)
        self.stop_bt.setEnabled(False)
        self.stop_bt.clicked.connect(self.stop_bt_push)

        # UI 텍스트 설정
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)


    def retranslateUi(self, Form):
        """UI에 표시될 텍스트를 설정"""
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "음주 운전 도주 차량 검거 시스템"))
        self.L_camera_label.setText(_translate("Form", "Camera 1"))
        self.R_camera_label.setText(_translate("Form", "Camera 2"))
        self.state_label.setText(_translate("Form", "카메라 좌표 보정"))
        self.down_time_label.setText(_translate("Form", "단속 경과 시간 : 00:00:00"))
        self.up_time_label.setText(_translate("Form", "단속 시작 시간 : 2024/11/11/24:00:00"))
        self.prg_exit_bt.setText(_translate("Form", "프로그램 종료"))
        self.stop_bt.setText(_translate("Form", "단속 시작"))

    def reset_ui(self):
        """UI를 초기화하여 단속 준비 상태로 변경"""
        self.state_label.setText("단속 준비 중")
        self.state_label.setStyleSheet("background-color: yellow;")

    def prg_exit_bt_push(self):
        """프로그램 종료"""
        global status

        if status == 1 or status == 2:  # 지도 보정모드, 준비 완료
            reply = QMessageBox.question(
                None,
                'Confirm',
                '정말 프로그램을 종료하시겠습니까?',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes
            )
            if reply == QMessageBox.Yes:
                QApplication.instance().quit()


    def stop_bt_push(self):
        """추적 중단 버튼"""
        global status

        if status == 1:
            reply = QMessageBox.question(
                None,
                'Confirm',
                '단속을 시작하시겠습니까?',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes
            )
            if reply == QMessageBox.Yes:
                self.node.set_status(2)

        elif status == 2:
            reply = QMessageBox.question(
                None,
                'Confirm',
                '정말 단속을 중단하시겠습니까?',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes
            )
            if reply == QMessageBox.Yes:
                self.node.set_runaway_to_pass()
                self.node.clear_all_object_states()
                self.node.set_status(1)

        elif status == 3:
            reply = QMessageBox.question(
            None,
            'Confirm',
            '정말 차량 추적을 중단하시겠습니까?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes
            )
            if reply == QMessageBox.Yes:
                self.node.set_runaway_to_pass()
                self.node.set_status(2)

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

        # 좌표 확인용 리스트
        self.area_points = []  # 클릭된 좌표 저장
        self.map_points = []  # 맵 좌표 저장

    

        # YOLO 관련
        self.yolo_model = YOLO("/home/lsw/ros2_rokey/src/monitor_test/monitor_test/models/best.pt")  # YOLOv8 모델 로드
        self.object_ids = {}  # {object_id: last_seen_frame}
        self.next_id = 1  # 고유 ID 생성용
        


        #self.object_entry_times = {}  # 객체 ID별 입장 시간 저장
        self.object_states = {}  # 트래킹 중인 객체의 정보를 저장
        
        self.current_color_index = 0

        # QLabel 클릭 이벤트와 함수 연결
        self.ui.L_camera_label.clicked.connect(self.handle_label_click)

        # QTimer 설정 (상태 색상 변경)
        self.color_timer = QTimer()
        self.color_timer.timeout.connect(self.toggle_label_color)
        self.color_timer.start(1000)  # 1초 간격으로 색상 변경

        self.elapsed_timer = QTimer()
        self.elapsed_timer.timeout.connect(self.update_elapsed_time)
        self.start_time = None  # 단속 시작 시간 초기화

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
            CompressedImage, '/webcam/yolo/compressed_image', self.callback_right_camera, qos_profile
        )

        # 디버그 로그 발행자 설정
        self.debug_publisher = self.create_publisher(String, 'debug_logs', 10)

        # 새로운 퍼블리셔
        self.string_publisher = self.create_publisher(String, '/move_go', 10)
        self.timer = self.create_timer(1, self.move_go)  # 1초 간격(1Hz)

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
        #self.display_image(cv_image, self.ui.R_camera_label)


    def callback_left_camera(self, msg):
        """왼쪽 카메라 콜백 처리, YOLO 탐지 수행"""
        global status

        np_arr = np.frombuffer(msg.data, np.uint8)
        # 이미지를 current_image에 저장함
        self.current_image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)


        #YOLO 합성 시작
        if status == 0:  # 상태가 0
            pass    #추가 안함
        elif status == 1 and len(self.area_points) < 4: # 상태가 1 | 영역 포인트가 4 미만 이면
            pass    #추가 안함
        elif status > 0 and len(self.area_points) == 4: # 상태가 1이상 | 영역 포인트가 4
            # YOLO로 객체 추적
            #results = self.yolo_model.track(source=self.current_image, conf=0.5, show=False, tracker="botsort.yaml")
            results = self.yolo_model.track(source=self.current_image, conf=0.5, show=False, tracker="bytetrack.yaml")

            # 트래킹 결과의 객체 정보
            self.tracking_results = results  # YOLO의 트래킹 결과 데이터

            # YOLO 데이터 처리
            self.current_image = self.draw_tracking_boxes(self.current_image, self.tracking_results, status=status)

        #points 합성 시작
        overlay = self.current_image.copy() # 오버레이 레이어 생성
        if len(self.map_points) < 4:
            #좌표값으로 점 생성
            for point in self.map_points:
                cv2.circle(self.current_image, center=point, radius=4, color=(255, 0, 0), thickness=-1)   #파랑
        elif len(self.map_points) == 4:
            #좌표 리스트 정렬
            self.map_points = self.sort_diamond_points(self.map_points)
            self.map_points_array = np.array(self.map_points, dtype=np.int32)
            #좌표값으로 마름모 생성 - 파란색
            cv2.polylines(self.current_image, [self.map_points_array], isClosed=True, color=(139, 0, 0), thickness=2) #파랑

            if status == 0:
                self.set_status(1)
        
        # 상태가 0 이 아니면
        if status > 0:
            if len(self.area_points) < 4:
                for point in self.area_points:
                    cv2.circle(self.current_image, center=point, radius=4, color=(0, 128, 0), thickness=-1) #초록
            
            elif len(self.area_points) == 4:
                #좌표 리스트 정렬 및 변환
                self.area_points = self.sort_diamond_points(self.area_points)
                self.area_points_array = np.array(self.area_points, dtype=np.int32)
                #좌표 값으로 마름모 생성
                #cv2.polylines(self.current_image, [self.area_points_array], isClosed=True, color=(255, 0, 0), thickness=2)
                #마름모 내부를 투명 연두로 채움

                cv2.polylines(self.current_image, [self.area_points_array], isClosed=True, color=(0, 255, 0), thickness=2)  # 초록
                cv2.fillPoly(overlay, [self.area_points_array], color=(0, 165, 255))  # 초록색 투명 백그라운드
                
        
        # 오버레이와 원본 이미지 합성 (투명도 조절)
        cv2.addWeighted(overlay, 0.10, self.current_image, 0.90, 0, self.current_image)   

        # 이미지 출력
        self.display_image(self.current_image, self.ui.L_camera_label)





    def draw_tracking_boxes(self, image, tracking_results, status, target_ID=None):


        """
        if results[0].boxes is not None:    # 입력 소스가 있을때 동작
            for box in results[0].boxes:    # 박스의 좌표와 클래스 정보를 추출
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = box.conf.item()  # 신뢰도
                cls = int(box.cls.item()) if hasattr(box.cls, 'item') else int(box.cls) # 클래스
                label = f"{results[0].names[cls]} {conf:.2f}"
                cv2.rectangle(self.current_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(self.current_image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        """
        
        if tracking_results[0].boxes is not None:   # 입력 소스가 있을때 동작
            # YOLO 트래킹 결과를 기반으로 바운딩 박스를 이미지에 그리는 함수
            current_time = time.time()
                
            if status == 1:
                # 박스만 그리고 반환
                for obj in tracking_results[0].boxes:
                    x1, y1, x2, y2 = map(int, obj.xyxy[0])
                    cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)
                return image
        
        
            elif status == 2:
                # 고유 ID 부여 및 영역 벗어난 시간 추적
                for obj in tracking_results[0].boxes:
                    x1, y1, x2, y2 = map(int, obj.xyxy[0])
                    object_center = ((x1 + x2) // 2, (y1 + y2) // 2)

                    # 기본 설정: 객체는 아직 ID가 없음
                    assigned_id = None
                    min_distance = float('inf')  # 최소 거리 초기화
                    box_color = (255, 255, 255)  # 기본 박스 색상 (흰색)
                    label = "Detected"  # 기본 라벨 초기화

                    # 기존 ID와 비교하여 가장 가까운 ID를 찾음
                    for obj_id, state in self.object_states.items():
                        prev_center = state.get('last_position')
                        if prev_center:
                            distance = np.linalg.norm(np.array(object_center) - np.array(prev_center))
                            if distance < 100 and distance < min_distance:  # 거리 임계값(50)
                                assigned_id = obj_id
                                min_distance = distance

                    if self.is_inside_area(object_center):  # 내부 영역에 있으면
                        # 영역 내부 객체 처리
                        if assigned_id is None: # ID가 없으면
                            # 새 객체 ID 부여 및 최초 진입 시간 기록
                            assigned_id = self.next_id  # 지정된 ID 부여
                            self.next_id += 1   # 다음 ID 업데이트
                            self.object_states[assigned_id] = { # 오브젝트의 상태[부여 ID]
                                'enter_time': current_time, # 들어온 시간 기록
                                'last_seen': current_time,  # 마지막 시간 기록
                                'inside_last_seen': current_time,
                                'inside': True, # 영역에 진입 했었음
                                'status': 'Inside',  # 상태 (None, "Pass", "Run away")  # 상태 - 영역에 있음
                                'last_position': object_center, # 마지막 위치
                                'detected': True,  # 현재 프레임에서 탐지됨
                            }
                        else:   # 아이디가 있으면
                            # 기존 객체 상태 업데이트
                            obj_state = self.object_states[assigned_id] # 오브젝트 ID 확인
                            obj_state['last_seen'] = current_time   # 마지막 시간 기록
                            obj_state['inside_last_seen'] = current_time
                            obj_state['last_position'] = object_center  # 마지막 위치 기록
                            obj_state['inside'] = True  # 영역에 있음

                        # 상태 업데이트 및 라벨링
                        obj_state = self.object_states[assigned_id] # 오브젝트 ID 확인
                        elapsed_time = current_time - obj_state['enter_time']   # 영역에 들어온 시간과 현재 시간을 비교

                        # 상태 고정: Pass 또는 Run away 상태로 변경된 후에는 상태를 더 이상 수정하지 않음
                        if obj_state['status'] == 'Inside' and elapsed_time > 3:    # 비교한 시간이 3보다 크고 상태가 영역에 있음 일때
                            obj_state['status'] = "Pass"    # 상태를 패스로 변경

                        # 색상 및 라벨 결정
                        if obj_state['status'] == "Inside": # 상태를 진입함 일때
                            label = f"ID: {assigned_id} ({elapsed_time:.1f}s)"  # 라벨에 아이디와 진입후 시간을 표시
                            box_color = (0, 255, 255)  # 노란색 (Inside)    # 박스를 노란색으로
                        elif obj_state['status'] == "Pass": # 상태가 패스 일때
                            label = f"ID: {assigned_id} Pass" # 라벨에 아이디와 pass를 표시
                            box_color = (255, 0, 0)  # 파란색 (Pass)    # 파란색
                        elif obj_state['status'] == "Run away": # 상태가 패스 일때
                            label = f"ID: {assigned_id} Run away" # 라벨에 아이디와 pass를 표시
                            box_color = (0, 0, 255)  # 파란색 (Pass)    # 파란색

                    else:   # 내부 영역에 없으면
                        # 영역 외부 객체 처리
                        if assigned_id is not None: # 아이디가 부여된게 있음
                            obj_state = self.object_states[assigned_id] # 오브젝트 ID 확인

                            # 도주 검사
                            if obj_state['status'] == 'Inside' and current_time - obj_state['inside_last_seen'] > 0.5: # 영역 안에 있다가 밖으로 나왔는데 0.5초가 지났을 경우
                                obj_state['status'] = "Run away"    # 상태 도주로 변경
                                self.runaway_ID = assigned_id  # 도주 객체 ID 기록
                                self.set_status(3)

                            # 색상 및 라벨 결정
                            if obj_state['status'] == "Pass":   # 상태가 pass인 경우                              
                                label = f"ID: {assigned_id} Pass" # 라벨에 아이디와 pass를 표시
                                box_color = (255, 0, 0)  # 파란색 (Pass)    # 박스를 파란색으로
                            elif obj_state['status'] == "Run away": # 상태가 도주인 경우
                                label = f"ID: {assigned_id} Run away" # 라벨에 아이디와 도주를 표시
                                box_color = (0, 0, 255)  # 빨간색 (Run away)    # 박스를 빨간색으로

                            # 영역 외부에서도 마지막 위치 유지
                            #x1, y1 = object_center # 객체의 중심 위치
                            #x2, y2 = x1 + 50, y1 + 50  # 고정 크기 박스 (예제)

                        # 박스와 라벨 그리기
                    if assigned_id is not None: # 아이디가 부여된게 있음
                        obj_state['last_position'] = object_center
                        obj_state['last_seen'] = current_time  # 탐지된 시간 갱신

                    cv2.rectangle(image, (x1, y1), (x2, y2), box_color, 2)  # 해당 영역에 박스를 그림
                    cv2.putText(image, label, (x1, y1 - 10),    # 텍스트를 입력함
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, box_color, 2)

                # 오래된 객체 정리 (2초 이상 탐지되지 않은 객체 삭제)
                to_remove_ids = [obj_id for obj_id, state in self.object_states.items()
                                if current_time - state['last_seen'] > 2]
                for obj_id in to_remove_ids:
                    del self.object_states[obj_id]

                return image

            elif status == 3:
                target_found = False  # 현재 타겟(도주 객체)을 찾았는지 여부
                processed_ids = set()

                # 모든 감지된 객체를 처리
                for obj in tracking_results[0].boxes:
                    x1, y1, x2, y2 = map(int, obj.xyxy[0])
                    object_center = ((x1 + x2) // 2, (y1 + y2) // 2)

                    # 객체 ID 매칭
                    assigned_id = None
                    min_distance = float('inf')

                    for obj_id, state in self.object_states.items():
                        prev_center = state.get('last_position')
                        if prev_center:
                            distance = np.linalg.norm(np.array(object_center) - np.array(prev_center))
                            if distance < 100 and distance < min_distance:  # 거리 임계값
                                assigned_id = obj_id
                                min_distance = distance
                
                    if assigned_id is None:
                    # 새로운 객체로 간주
                        self.object_states[None] = {
                            'enter_time': current_time,
                            'last_seen': current_time,
                            'last_position': object_center,
                            'status': "None",  # 항상 도주 상태로 설정
                            'detected': True,  # 현재 프레임에서 탐지됨
                        }
                        # 박스와 라벨 출력
                        box_color = (255, 255, 255)  # 빨간색
                        label = "Detected"

                    else:
                        # 기존 객체 업데이트
                        obj_state = self.object_states[assigned_id]
                        obj_state['last_seen'] = current_time
                        obj_state['last_position'] = object_center
                        obj_state['status'] = "Run away"  # 도주 상태로 변경
                        obj_state['detected'] = True,  # 현재 프레임에서 탐지됨

                        # 박스와 라벨 출력
                        box_color = (0, 0, 255)  # 빨간색
                        label = f"ID: {assigned_id} Run away"

                        # 1초마다 auto_transform_coordinates() 호출
                        if 'last_call_time' not in obj_state or (current_time - obj_state['last_call_time']) >= 1:
                            x, y = obj_state['last_position']
                            self.mx, self.my = self.auto_transform_coordinates(x, y)
                            obj_state['last_call_time'] = current_time  # 마지막 호출 시간 업데이트
                            obj_state['transformed_coordinates'] = (self.mx, self.my)  # 변환된 좌표를 상태에 저장

                        if 'transformed_coordinates' in self.object_states[assigned_id]:
                            self.mx, self.my = self.object_states[assigned_id]['transformed_coordinates']
                        label += f"  X: {self.mx:.2f} Y: {self.my:.2f}"

                    cv2.rectangle(image, (x1, y1), (x2, y2), box_color, 2)
                    cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, box_color, 2)
                    target_found = True  # 감지된 객체 있음
                    processed_ids.add(assigned_id)  # 처리된 ID 추가

                for obj_id, obj_state in self.object_states.items():
                    # 'Run away' 상태의 객체가 감지된 경우
                    if obj_id in processed_ids:  # 이미 처리된 객체는 건너뜀
                        continue

                    if obj_state.get('status') == "Run away" and obj_state.get('last_position'):
                        obj_state['detected'] = False  # 탐지되지 않음
                        last_position = obj_state.get('last_position')

                        if last_position:
                            x, y = last_position
                            box_size = 50  # 고정 크기 박스
                            half_box = box_size // 2
                            x1, y1 = x - half_box, y - half_box
                            x2, y2 = x + half_box, y + half_box

                        # "Last Seen" 라벨 출력
                        label = f"ID: {obj_id} Directionless"
                        box_color = (0, 0, 255)  # 빨간색
                        cv2.rectangle(image, (x1, y1), (x2, y2), box_color, 2)
                        cv2.putText(image, label, (x1, y1 - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, box_color, 2)

                return image








    def is_inside_area(self, point):
        """
        점이 마름모 영역 내부에 있는지 확인.
        """
        self.np_area_points = np.array(self.area_points, dtype=np.int32)
        return cv2.pointPolygonTest(self.np_area_points, point, False) >= 0







    def change_target(self, x, y):
        
        # 초기화
        min_distance = float('inf') 
        closest_object = None   
        runaway_id = None

        # 오브젝트 정보들 읽어옴
        for odj_id, obj_state in self.object_states.items():
            if obj_state.get('status') == "Run away": # 상태가 runaway
                runaway_id = odj_id # 해당 상태의 index를 도주 아이디로 저장
                break
        
        # 객체를 순회 하며 정보를 읽어옴
        for obj in self.tracking_results[0].boxes:
            x1, y1, x2, y2 = map(int, obj.xyxy[0])
            object_center = ((x1 + x2) // 2, (y1 + y2) // 2)

            distance =  ((x - object_center[0]) ** 2 + (y - object_center[1]) ** 2) ** 0.5 # 포인트와 객체의 거리를 구함
            if distance < 50 and distance < min_distance:  # 거리 임계값
                min_distance = distance 
                closest_object = obj    #거리가 가까운 obj를 선택한 obj로 지정

        # 3. 가장 가까운 객체에 'Run away' 상태 ID와 정보 업데이트
        x1, y1, x2, y2 = map(int, closest_object.xyxy[0])
        object_center = ((x1 + x2) // 2, (y1 + y2) // 2)

        # 기존 'Run away' ID 정보 업데이트
        self.object_states[runaway_id]['last_position'] = object_center
        self.object_states[runaway_id]['last_seen'] = self.current_time
        self.object_states[runaway_id]['status'] = "Run away"
        
        


    def set_runaway_to_pass(self):
        """
        Run away 상태의 객체를 Pass로 변경
        """
        global status
        if status == 3:
            for obj_id, obj_state in self.object_states.items():
                if obj_state.get('status') == "Run away":
                    obj_state['status'] = "Pass"  # 상태 변경
                    print(f"Object ID {obj_id} status changed to Pass")  # 디버깅 로그
        elif status == 2:
            for obj_id, obj_state in self.object_states.items():
                if obj_state.get('status') == "Pass":
                    obj_state['status'] = "None"  # 상태 변경
                    print(f"Object ID {obj_id} status changed to None")  # 디버깅 로그


    def clear_all_object_states(self):
        self.object_states.clear()
        self.next_id = 1
        print("All object states have been cleared.")








    """@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@판단@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"""

    def auto_transform_coordinates(self, x, y):

        image_corners = self.sort_diamond_points(self.map_points)  # Example image corners
        map_corners = [(0, 0), (300, 0), (300, 300), (0, 300)]  # Example map corners
    
        # Convert corners to numpy arrays
        src_points = np.array(image_corners, dtype=np.float32)
        dst_points = np.array(map_corners, dtype=np.float32)
    
        # Calculate homography matrix
        homography_matrix, _ = cv2.findHomography(src_points, dst_points, method=cv2.RANSAC)
    
        point_homogeneous = np.array([x, y, 1], dtype=np.float32).reshape(-1, 1)

        # Transform points
        transformed_point_homogeneous = np.dot(homography_matrix, point_homogeneous)
        x_prime, y_prime, w = transformed_point_homogeneous.flatten()
    
        return x_prime / w, y_prime / w
    


    """@@@@@@@@@@@@@@@@@@@@@@@@@클릭 좌표 인식 및 마름모 생성@@@@@@@@@@@@@@@@@@@@@@@@@@@"""

    def handle_label_click(self, x, y):
        """라벨 클릭 시 좌표 저장 및 마름모 업데이트"""
        global status

        if status == 0:
            if len(self.map_points) < 4:
                self.map_points.append((x, y))

        elif status == 1:
            if len(self.area_points) < 4:
                self.area_points.append((x, y))
                self.ui.state_label.setText("단속 영역 설정중")
                if len(self.area_points) == 4: 
                    self.ui.state_label.setText("단속 준비 완료")
                    self.ui.stop_bt.setEnabled(True)   # 정지 버튼 활성화
            elif len(self.area_points) == 4:  # 점이 4개 되면 선 연결 및 내부 채우기
                self.area_points = []
                self.ui.stop_bt.setEnabled(False)   # 정지 버튼 비활성화
                self.ui.state_label.setText("단속 영역 설정중")
        elif status == 3:
            self.change_target(x,y)


    def sort_diamond_points(self, points):
        """마름모 좌표를 시계 방향으로 정렬"""
        cx = sum(p[0] for p in points) / 4
        cy = sum(p[1] for p in points) / 4
        return sorted(points, key=lambda p: math.atan2(p[1] - cy, p[0] - cx))
    




    """@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@이미지 좌표 변환@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"""
    







    """@@@@@@@@@@@@@@@@@@@@@@@@@@@@상태 관리@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"""

    def set_status(self, new_status):
        """상태를 변경하고 UI를 업데이트"""
        global status
        status = new_status


        if status == 0: # 이미지 보정 모드
            self.ui.state_label.setText("이미지 좌표 보정중 (노란색)")
            self.ui.state_label.setStyleSheet("background-color: yellow;")

        elif status == 1:  # 단속 준비 상태
            self.elapsed_timer.stop()  # 타이머 중지
            self.escape_time = None
            self.escape_elapsed_time = 0
            self.start_time = None

        elif status == 2:  # 단속 중 상태
            self.start_time = time.time()  # 현재 시간을 단속 시작 시간으로 기록
            self.elapsed_timer.start(1000)  # 1초마다 경과 시간 갱신

            # 도주 관련 변수 초기화
            self.escape_time = None
            self.escape_elapsed_time = 0

        elif status == 3:  # 도주 발생 상태로 변경될 때
            self.escape_time = time.time()  # 현재 시간을 도주 발생 시간으로 기록
            self.elapsed_timer.start(1000)  # 도주 경과 시간도 1초마다 갱신

        self.update_ui()


    def update_ui(self):
        """현재 상태에 따라 UI를 업데이트"""
        global status

        if status == 0:
            self.ui.state_label.setText("카메라 좌표 보정")
            self.ui.state_label.setStyleSheet("background-color: yellow;")
            self.ui.prg_exit_bt.setEnabled(True)    # 프로그램 종료 버튼 활성화
            self.ui.stop_bt.setEnabled(False)   # 정지 버튼 비활성화

        elif status == 1:
            if len(self.area_points) < 4:
                self.ui.state_label.setText("단속 영역 설정중")
                self.ui.stop_bt.setEnabled(False)   # 정지 버튼 활성화
            else:
                self.ui.state_label.setText("단속 준비 완료")
                self.ui.stop_bt.setEnabled(True)   # 정지 버튼 활성화
                self.ui.stop_bt.setText("단속 시작")    # 단속 시작 버튼으로 변경

            self.ui.state_label.setStyleSheet("background-color: yellow;")
            self.ui.prg_exit_bt.setEnabled(True)    # 프로그램 종료 버튼 활성화

            #self.click_points = [] # 체크 포인트 초기화
            self.ui.up_time_label.setText("단속 시작 시간 : --:--:--")
            self.ui.down_time_label.setText("단속 경과 시간 : --:--:--")

        elif status == 2:
            self.ui.state_label.setText("음주 단속 중")
            self.ui.state_label.setStyleSheet("background-color: green;")
            self.ui.prg_exit_bt.setEnabled(False)
            self.ui.stop_bt.setText("단속 중단")    # 단속 중단 버튼으로 변경

            # 단속 시작 시간을 표시
            start_time_str = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(self.start_time))
            self.ui.up_time_label.setText(f"단속 시작 시간 : {start_time_str}")

        elif status == 3:
            self.ui.state_label.setText("도주 차량 발생")
            self.ui.state_label.setStyleSheet("background-color: red;")
            self.ui.prg_exit_bt.setEnabled(False)
            self.ui.stop_bt.setText("추적 중단")    # 추적 중단 버튼으로 변경

            # 도주 발생 시간을 표시
            if self.escape_time:
                escape_time_str = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(self.escape_time))
                self.ui.up_time_label.setText(f"도주 발생 시간 : {escape_time_str}")


    def update_elapsed_time(self):
        """경과 시간을 갱신하여 UI에 표시"""
        global status

        if status == 2 and self.start_time:
        # 단속 경과 시간 갱신
            elapsed_seconds = int(time.time() - self.start_time)
            elapsed_time_str = time.strftime('%H:%M:%S', time.gmtime(elapsed_seconds))
            self.ui.down_time_label.setText(f"단속 경과 시간 : {elapsed_time_str}")

        elif status == 3 and self.escape_time:
        # 도주 경과 시간 갱신
            self.escape_elapsed_time = int(time.time() - self.escape_time)
            escape_elapsed_time_str = time.strftime('%H:%M:%S', time.gmtime(self.escape_elapsed_time))
            self.ui.down_time_label.setText(f"도주 경과 시간 : {escape_elapsed_time_str}")

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




    #@@@@@@@@@@@@@@@@@@@@@@@@@@터틀봇에 좌표 전송하기@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    def move_go(self):
        global status
        new_msg = String()

        if status < 3:
            new_msg.data = "home"
        else:
            new_msg.data = f"X: {self.mx:.2f} Y: {self.my:.2f}"


        self.string_publisher.publish(new_msg)


    """@@@@@@@@@@@@@@@@@@@@@@@@@@@디버그@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"""

    def log_debug(self, message):
        """디버그 메시지를 발행하는 함수"""
        if not hasattr(self, 'debug_publisher') or self.debug_publisher is None:
            print("[ERROR] Debug publisher is not initialized.")
            return

        try:
            debug_msg = String()
            debug_msg.data = str(message)
            self.debug_publisher.publish(debug_msg)
        except Exception as e:
            print(f"[ERROR] Failed to publish debug message: {e}")



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
