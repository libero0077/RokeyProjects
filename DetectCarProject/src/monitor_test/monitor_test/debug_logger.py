# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
import threading
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class Ui_MainWindow(object):
    """디버그 UI 설정 클래스"""
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(781, 399)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.recovery_msg = QtWidgets.QTextBrowser(self.centralwidget)
        self.recovery_msg.setGeometry(QtCore.QRect(10, 10, 761, 291))
        self.recovery_msg.setObjectName("recovery_msg")
        self.send_msg_bt = QtWidgets.QPushButton(self.centralwidget)
        self.send_msg_bt.setGeometry(QtCore.QRect(10, 310, 89, 31))
        self.send_msg_bt.setObjectName("send_msg_bt")
        self.send_msg = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.send_msg.setGeometry(QtCore.QRect(110, 310, 661, 31))
        self.send_msg.setObjectName("send_msg")
        self.prepare_send_bt = QtWidgets.QPushButton(self.centralwidget)
        self.prepare_send_bt.setGeometry(QtCore.QRect(10, 360, 89, 31))
        self.prepare_send_bt.setObjectName("prepare_send_bt")
        self.tracking_send_bt = QtWidgets.QPushButton(self.centralwidget)
        self.tracking_send_bt.setGeometry(QtCore.QRect(110, 360, 89, 31))
        self.tracking_send_bt.setObjectName("tracking_send_bt")
        self.warning_send_bt = QtWidgets.QPushButton(self.centralwidget)
        self.warning_send_bt.setGeometry(QtCore.QRect(210, 360, 89, 31))
        self.warning_send_bt.setObjectName("warning_send_bt")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # 버튼 클릭 이벤트 연결
        self.send_msg_bt.clicked.connect(self.send_custom_message)
        self.prepare_send_bt.clicked.connect(lambda: self.send_state_message("PREPARE"))
        self.tracking_send_bt.clicked.connect(lambda: self.send_state_message("TRACKING"))
        self.warning_send_bt.clicked.connect(lambda: self.send_state_message("WARNING"))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Debug Interface"))
        self.send_msg_bt.setText(_translate("MainWindow", "send"))
        self.prepare_send_bt.setText(_translate("MainWindow", "PREPARE"))
        self.tracking_send_bt.setText(_translate("MainWindow", "TRACKING"))
        self.warning_send_bt.setText(_translate("MainWindow", "WARNING"))

    def set_ros_node(self, ros_node):
        """ROS 2 노드 설정"""
        self.ros_node = ros_node

    def send_custom_message(self):
        """사용자가 입력한 메시지를 ROS 2 노드에 발행"""
        if hasattr(self, 'ros_node'):
            message = self.send_msg.toPlainText()
            self.ros_node.publish_debug_message(message)

    def send_state_message(self, state):
        """상태 메시지를 ROS 2 노드에 발행"""
        if hasattr(self, 'ros_node'):
            self.ros_node.publish_state_message(state)

    def append_log_message(self, message):
        """디버그 로그를 UI에 추가"""
        self.recovery_msg.append(message)


class DebugNode(Node):
    """ROS 2 디버그 노드 클래스"""
    
    def __init__(self, ui):
        super().__init__('debug_node')
        self.ui = ui
        self.ui.set_ros_node(self)  # UI와 노드 연결

        # 발행자 설정 (상태 변경 요청 및 사용자 정의 메시지 발행)
        self.state_publisher = self.create_publisher(String, 'state_change', 10)
        self.debug_publisher = self.create_publisher(String, 'debug_command', 10)

        # 구독자 설정 (디버그 로그 수신)
        self.log_subscriber = self.create_subscription(String, 'debug_logs', self.log_callback, 10)

    def publish_state_message(self, state):
        """상태 변경 메시지 발행"""
        msg = String()
        msg.data = state
        self.state_publisher.publish(msg)
        self.get_logger().info(f"Published state: {state}")

    def publish_debug_message(self, message):
        """사용자 정의 디버그 메시지 발행"""
        msg = String()
        msg.data = message
        self.debug_publisher.publish(msg)
        self.get_logger().info(f"Published debug message: {message}")

    def log_callback(self, msg):
        """디버그 로그 메시지 수신 콜백"""
        message = f"[Debug Log] {msg.data}"
        self.get_logger().info(f"Received log: {message}")
        # UI에 디버그 메시지 추가
        self.ui.append_log_message(message)


def main(args=None):
    rclpy.init(args=args)

    # PyQt5 애플리케이션 설정
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    # ROS 2 노드 생성 및 설정
    debug_node = DebugNode(ui)
    executor = rclpy.executors.SingleThreadedExecutor()
    executor.add_node(debug_node)

    # ROS 스핀을 위한 스레드 시작
    def ros_spin():
        while rclpy.ok():
            rclpy.spin_once(debug_node, timeout_sec=0.1)

    ros_thread = threading.Thread(target=ros_spin, daemon=True)
    ros_thread.start()

    # PyQt5 애플리케이션 실행
    sys.exit(app.exec_())
    rclpy.shutdown()


if __name__ == "__main__":
    main()
