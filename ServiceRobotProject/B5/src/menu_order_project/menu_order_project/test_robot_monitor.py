import sys
import threading
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QMessageBox, QPushButton
)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap, QFont, QColor, QPalette
import json

class RobotStatusMonitor(Node):
    def __init__(self, gui):
        super().__init__('robot_status_monitor')
        self.gui = gui
        self.subscription = self.create_subscription(
            String,
            'robot_status',
            self.robot_status_callback,
            10  # QoS profile depth
        )
        self.subscription  # prevent unused variable warning

    def robot_status_callback(self, msg):
        try:
            # Log the raw message
            self.get_logger().info(f"Received raw message: {msg.data}")

            # Check if the message looks like a valid JSON string
            if msg.data.startswith('{') and msg.data.endswith('}'):
                # Attempt to decode using unicode_escape for potential issues with encoding
                decoded_data = msg.data.encode('utf-8').decode('unicode_escape')
                self.get_logger().info(f"Decoded message: {decoded_data}")

                # Try parsing the JSON message
                status_msg = json.loads(decoded_data)
                
                # Extract relevant fields
                status = status_msg.get("status", "")
                position = status_msg.get("position", "")
                order_item_ids = status_msg.get("order_item_ids", [])

                # Update GUI with the extracted data
                self.gui.update_status(status, position, order_item_ids)
            else:
                self.get_logger().error(f"Message is not a valid JSON: {msg.data}")
        except json.JSONDecodeError as e:
            self.get_logger().error(f"Failed to parse robot status message: {str(e)}")
        except UnicodeDecodeError as e:
            self.get_logger().error(f"Unicode decode error: {str(e)}")


class RobotMonitorGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

        # ROS 노드 초기화
        rclpy.init()
        self.node = RobotStatusMonitor(self)
        self.node.get_logger().info("Robot Status Monitor Node initialized.")

        '''# ROS 스핀을 별도의 스레드에서 실행
        self.ros_thread = threading.Thread(target=self.ros_spin, daemon=True)
        self.ros_thread.start()'''

        # QTimer를 사용하여 주기적으로 ROS 이벤트 처리
        self.timer = QTimer()
        self.timer.timeout.connect(self.ros_spin_once)
        self.timer.start(100)  # 100ms마다 spin_once 호출

        ###################### 로봇 복귀 명령을 수행하기 위해서 새로운 퍼블리셔 생성 ############################
        ######## 복귀 버튼을 눌르면 로봇 컨트롤러에게 다시 대기 위치로 돌아가도록 퍼블리시를 해주어야 하기 떄문 #########
        qos_profile = rclpy.qos.QoSProfile(depth=10)
        self.command_publisher = self.node.create_publisher(String, 'robot_command', qos_profile)
        ##############################################################################################

    def init_ui(self):
        self.setWindowTitle("로봇 상태 모니터링")
        self.setGeometry(100, 100, 500, 400)  # 창 크기 조정

        # 메인 레이아웃 설정
        main_layout = QVBoxLayout()

        # 로봇 이미지 추가
        self.robot_image_label = QLabel(self)
        pixmap = QPixmap("Robot.png")  # 프로젝트 디렉토리에 'robot.png'가 있어야 합니다.
        if pixmap.isNull():
            # 이미지 로드 실패 시 기본 텍스트 표시
            self.robot_image_label.setText("로봇 이미지 로드 실패")
            self.robot_image_label.setAlignment(Qt.AlignCenter)
        else:
            pixmap = pixmap.scaled(350, 350, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.robot_image_label.setPixmap(pixmap)
            self.robot_image_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.robot_image_label)

        # 로봇 상태 레이블
        self.status_label = QLabel("로봇 상태: 대기 중")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setFont(QFont("Arial", 16, QFont.Bold))
        main_layout.addWidget(self.status_label)

        # 추가 메시지 레이블 (로봇이 이동 중일 때 표시)
        self.warning_label = QLabel("")
        self.warning_label.setAlignment(Qt.AlignCenter)
        font = QFont("Arial", 12)
        font.setItalic(True)
        self.warning_label.setFont(font)
        self.warning_label.setStyleSheet("color: red;")
        main_layout.addWidget(self.warning_label)

        ############### 서빙로봇 복귀 버튼 추가#####################################
        self.return_button = QPushButton("복귀")
        self.return_button.setFont(QFont("Arial", 14, QFont.Bold))
        self.return_button.setStyleSheet("background-color: #4CAF50; color: white;")
        self.return_button.setFixedHeight(50)
        self.return_button.clicked.connect(self.send_return_command)
        self.return_button.setVisible(False)  # 초기에는 숨김
        main_layout.addWidget(self.return_button)
        ####################################################################

        # 로봇 상태에 따른 배경색 변경을 위한 레이아웃
        self.status_background = QWidget()
        self.status_layout = QVBoxLayout()
        self.status_background.setLayout(self.status_layout)
        self.status_layout.addWidget(self.status_label)
        self.status_layout.addWidget(self.warning_label)
        main_layout.addWidget(self.status_background)

        # 전체 레이아웃 설정
        self.setLayout(main_layout)

        # 초기 스타일 설정
        self.set_initial_style()

    def set_initial_style(self):
        """초기 스타일 설정: 대기 중일 때 배경색"""
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#F0F0F0"))  # 밝은 회색 배경
        self.setPalette(palette)

    def update_status(self, status, position, order_item_ids):
        """로봇 상태 메시지를 받아 GUI를 업데이트하는 함수"""
        self.status_label.setText(f"로봇 상태: {status}")

        # 상태에 따라 추가 메시지와 스타일 변경
        if "이동 중입니다" in status:
            self.warning_label.setText("🚧 로봇이 이동 중입니다. 주변을 조심해 주세요! 🚧")
            self.status_background.setStyleSheet("background-color: #FFDAB9;")  # 복숭아색 배경
        ############## 로봇이 테이블에 도착했을때 알림 뜨도록 설정 ##################################
        elif "음식이 도착했습니다" in status:
            self.warning_label.setText("🚧 로봇이 도착했습니다! 🚧")
            self.return_button.setVisible(True)  # 복귀 버튼 활성화
            self.status_background.setStyleSheet("background-color: #FFDAB9;")  # 복숭아색 배경
        ###################################################################################
        elif "대기 위치입니다" in status or "주방 위치입니다" in status:
            self.warning_label.setText("")  # 추가 메시지 숨기기
            #### 복귀 버튼을 숨기고 있어야함 ###
            self.return_button.setVisible(False)  # 복귀 버튼 숨김
            self.status_background.setStyleSheet("background-color: #90EE90;")  # 연두색 배경
        else:
            self.warning_label.setText("")  # 기본 상태일 때 추가 메시지 숨기기
            ################### 복귀 버튼은 로봇이 테이블에 도착했을 떄만 나오도록 설정 ###############
            self.return_button.setVisible(False)  # 복귀 버튼 숨김
            self.status_background.setStyleSheet("background-color: #F0F0F0;")  # 기본 배경색

    '''def ros_spin(self):
        """ROS 이벤트를 처리하는 함수 (별도 스레드에서 실행)"""
        rclpy.spin(self.node)'''
    
    def ros_spin_once(self):
        """ROS 이벤트를 주기적으로 처리"""
        rclpy.spin_once(self.node, timeout_sec=0)

    def closeEvent(self, event):
        """창이 닫힐 때 ROS 노드 종료"""
        self.node.destroy_node()
        rclpy.shutdown()
        event.accept()
    ############################### 복귀 명령을 퍼블리시 하기 위한 메서드 #####################
    def send_return_command(self):
        """복귀 명령을 퍼블리시"""
        command_msg = String()
        command_msg.data = json.dumps({"command": "move", "position": "waiting"})
        self.command_publisher.publish(command_msg)

        ######## 손님이 복귀 버튼을 누르면 복귀 버튼을 다시 숨겨야함 #####
        self.return_button.setVisible(False)
    ####################################################################################
def main():
    app = QApplication(sys.argv)
    gui = RobotMonitorGUI()
    gui.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
