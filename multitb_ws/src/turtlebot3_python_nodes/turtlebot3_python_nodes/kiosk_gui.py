#!/usr/bin/env python3

# scripts/kiosk_gui.py

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLineEdit, QPushButton, QLabel, 
    QWidget, QGridLayout
)
from PyQt5.QtCore import QTimer, Qt
import rclpy
from rclpy.node import Node
from turtlebot3_interfaces.srv import ExitRequest  # 수정된 서비스 파일
from PyQt5.QtGui import QFont
from rclpy.qos import QoSProfile
from std_msgs.msg import String
import json
from datetime import datetime

# ROS2 노드 클래스 (서비스 클라이언트)
class KioskNode(Node):
    def __init__(self):
        super().__init__('kiosk_node')
        self.cli = self.create_client(ExitRequest, 'exit_request')
        # 중앙 관제 시스템이 켜지는 것을 기다리는 로직
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service /exit_request not available, waiting...')
        self.req = ExitRequest.Request()
        self.future = None

    # 서비스 요청을 서버로 보내는 메서드 (비동기)
    def send_exit_request(self, car_number):
        self.req.car_number = car_number
        self.future = self.cli.call_async(self.req)
        return self.future

# 키오스크 GUI 클래스 (PyQt5 기반)
class KioskGui(QMainWindow):
    def __init__(self, ros_node):
        super().__init__()
        self.ros_node = ros_node
        # 퍼블리셔 초기화
        qos_profile = QoSProfile(depth=10)
        self.payment_publisher = self.ros_node.create_publisher(String, '/payment/confirmation', qos_profile)
        self.init_ui()

    # UI 초기화 메서드
    def init_ui(self):
        self.setWindowTitle("Kiosk System")
        self.setFixedSize(500, 700)  # 창 크기 고정
        self.setStyleSheet("background-color: #f5f5f5;")  # 배경색

        # 중앙 위젯 생성
        central_widget = QWidget()
        layout = QVBoxLayout()

        # 안내 메시지 라벨
        self.info_label = QLabel("차량 번호 뒷자리를 눌러주세요.", self)
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setWordWrap(True)
        self.info_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #333;")
        layout.addWidget(self.info_label)

        # 차량 번호 입력 필드
        self.car_number_input = QLineEdit(self)
        self.car_number_input.setReadOnly(True)
        self.car_number_input.setPlaceholderText("차량 번호 입력 중...")
        self.car_number_input.setAlignment(Qt.AlignCenter)
        self.car_number_input.setStyleSheet("""
            QLineEdit {
                font-size: 22px;
                font-weight: bold;
                background-color: #ffffff;
                border: 2px solid #0078D4;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        layout.addWidget(self.car_number_input)

        # 차량 입차 시간 표시
        self.entry_time_label = QLabel("", self)
        self.entry_time_label.setAlignment(Qt.AlignCenter)
        self.entry_time_label.setWordWrap(True)
        self.entry_time_label.setStyleSheet("font-size: 16px; color: #555;")
        layout.addWidget(self.entry_time_label)

        # 숫자 키패드 레이아웃
        keypad_layout = QGridLayout() 
        buttons = [
            '1', '2', '3',
            '4', '5', '6',
            '7', '8', '9',
            'DEL', '0', 'CLEAR'
        ]

        for i, btn_text in enumerate(buttons):
            button = QPushButton(btn_text)
            button.setFixedSize(80, 60)
            button.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    font-size: 18px;
                    font-weight: bold;
                    border-radius: 10px;
                }
                QPushButton:hover {
                    background-color: #45A049;
                }
            """)
            button.clicked.connect(lambda checked, text=btn_text: self.on_keypad_click(text))
            row, col = divmod(i, 3)
            keypad_layout.addWidget(button, row, col)

        layout.addLayout(keypad_layout)

        # 출차 요청 버튼
        self.submit_button = QPushButton("출차 요청", self)
        self.submit_button.setFixedHeight(50)
        self.submit_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 20px;
                font-weight: bold;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #45A049;
            }
        """)
        self.submit_button.clicked.connect(self.on_submit)
        layout.addWidget(self.submit_button)

        # 결제 버튼
        self.pay_button = QPushButton("요금 결제", self)
        self.pay_button.setVisible(False)
        self.pay_button.setFixedHeight(50)
        self.pay_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                font-size: 20px;
                font-weight: bold;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        self.pay_button.clicked.connect(self.on_payment)
        layout.addWidget(self.pay_button)

        # 결제 완료 메시지 라벨 (숨김 상태)
        self.payment_message_label = QLabel("", self)
        self.payment_message_label.setAlignment(Qt.AlignCenter)
        self.payment_message_label.setWordWrap(True)
        self.payment_message_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                color: red;  /* 텍스트 색상을 빨간색으로 변경 */
                background-color: #ffe0e0;  /* 배경색을 연한 빨간색으로 설정 */
                border: 2px solid #ff0000;  /* 빨간색 테두리 */
                border-radius: 10px;
                padding: 10px;
            }
        """)
        self.payment_message_label.setFixedSize(400, 50)
        self.payment_message_label.hide()
        layout.addWidget(self.payment_message_label)

        # 초기 화면으로 리셋하는 버튼 (숨김 상태)
        self.reset_button = QPushButton("초기 화면으로", self)
        self.reset_button.setVisible(False)
        self.reset_button.setFixedHeight(50)
        self.reset_button.setStyleSheet("""
            QPushButton {
                background-color: #FFA500;
                color: white;
                font-size: 20px;
                font-weight: bold;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #FF8C00;
            }
        """)
        self.reset_button.clicked.connect(self.reset_gui)
        layout.addWidget(self.reset_button)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    # 키패드 버튼 클릭 이벤트 핸들러
    def on_keypad_click(self, value):
        if value == 'DEL':  # 숫자 하나만 지움
            current_text = self.car_number_input.text()
            self.car_number_input.setText(current_text[:-1])
        elif value == 'CLEAR':  # 숫자 전체 지움
            self.car_number_input.clear()
            self.entry_time_label.clear()
        else:
            self.car_number_input.setText(self.car_number_input.text() + value)

    # 출차 요청 버튼 클릭 시 실행되는 메서드
    def on_submit(self):
        car_number = self.car_number_input.text().strip()
        if not car_number:
            self.info_label.setText("차량 번호를 다시 입력하세요.")
            return

        self.info_label.setText(f"차량 번호 {car_number} 출차 요청 중...")
        self.submit_button.setEnabled(False)
        self.pay_button.setVisible(False)
        self.entry_time_label.clear()

        # 서비스 호출 -> 출차 요청 버튼을 눌렀을 때 서버에 요청함
        future = self.ros_node.send_exit_request(car_number)
        future.add_done_callback(self.display_response)

    # 서비스 응답을 GUI에 표시하는 메서드
    def display_response(self, future):
        try:
            response = future.result()
        except Exception as e:
            self.info_label.setText("서비스 호출 중 오류가 발생했습니다.")
            self.submit_button.setEnabled(True)
            print(f"Service call failed: {str(e)}")  # 로그 대신 print 사용
            return

        if response.status:
            # 입차 시간 표시
            self.entry_time_label.setText(f"입차 시간: {response.entry_time}")
            self.info_label.setText(f"✅ 결제 요금: {response.fee}원\n{response.log}")
            self.pay_button.setVisible(True)  # 결제 버튼 표시
            self.submit_button.setVisible(False)  # 출차 요청 버튼 숨김
            self.reset_button.setVisible(True)  # 초기 화면 버튼 표시
        else:
            self.info_label.setText(f"출차 요청 실패: {response.log}")

        self.submit_button.setEnabled(True)

    # 결제 버튼 클릭 시 실행되는 메서드
    def on_payment(self):
        car_number = self.car_number_input.text().strip()
        if not car_number:
            self.info_label.setText("유효한 차량 번호가 아닙니다.")
            return
        
        # info_label에 "요금: ..."이 포함되어 있는지 확인
        if "요금: " not in self.info_label.text():
            self.info_label.setText("요금을 확인할 수 없습니다.")
            return

        try:
            # 요금을 파싱하여 정수로 변환
            fee_str = self.info_label.text().split("✅ 결제 요금: ")[1].split("원")[0]
            total_fee = int(fee_str)
        except (IndexError, ValueError):
            self.info_label.setText("요금을 파싱하는 중 오류가 발생했습니다.")
            return

        # 결제 처리 시뮬레이션 (실제 결제 게이트웨이와 연동 필요 시 수정)
        self.info_label.setText("결제가 완료되었습니다. 대기 장소에 기다려주세요.")
        self.pay_button.setVisible(False)
        self.submit_button.setEnabled(False)
        self.car_number_input.setEnabled(False)

        # 결제 정보 준비
        payment_info = {
            "vehicle_id": car_number,
            "entry_time": self.entry_time_label.text().replace("입차 시간: ", ""),
            "exit_time": datetime.now().isoformat(timespec='seconds'),
            "total_fee": total_fee,
            "payment_method": "카드"  # 예시 결제 방식
        }

        # JSON 문자열로 변환
        payment_json = json.dumps(payment_info)

        # 결제 확인 메시지 퍼블리시
        msg = String()
        msg.data = payment_json
        self.payment_publisher.publish(msg)

        # 결제 완료 메시지 표시
        self.payment_message_label.setText("결제가 완료되었습니다. 대기 장소에 기다려주세요.")
        self.payment_message_label.show()

        # 4초 후 GUI 초기화
        QTimer.singleShot(4000, self.close_payment_message_and_reset_gui)


    # 결제 완료 메시지 숨기기 및 GUI 초기화 메서드
    def close_payment_message_and_reset_gui(self):
        self.payment_message_label.hide()
        self.reset_gui()

    # GUI 초기화 메서드
    def reset_gui(self):
        self.info_label.setText("차량 번호 뒷자리를 눌러주세요.")
        self.car_number_input.clear()
        self.entry_time_label.clear()
        self.pay_button.setVisible(False)
        self.submit_button.setVisible(True)  # 출차 요청 버튼 다시 표시
        self.submit_button.setEnabled(True)
        self.car_number_input.setEnabled(True)
        self.reset_button.setVisible(False)  # 초기 화면 버튼 숨김

    # 로거 메서드 추가 (옵셔널)
    def get_logger(self):
        return self.ros_node.get_logger()

# 메인 실행 함수
def main():
    rclpy.init(args=None)
    ros_node = KioskNode()

    app = QApplication(sys.argv)
    kiosk_gui = KioskGui(ros_node)
    kiosk_gui.show()

    # ROS2 스핀을 QTimer로 통합하여 이벤트 루프와 함께 동작하게 함
    timer = QTimer()
    timer.timeout.connect(lambda: rclpy.spin_once(ros_node, timeout_sec=0))
    timer.start(100)  # 100ms마다 spin_once 호출

    exit_code = app.exec_()

    ros_node.destroy_node()
    rclpy.shutdown()

    sys.exit(exit_code)

if __name__ == '__main__':
    main()
