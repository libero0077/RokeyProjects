#!/usr/bin/env python3

# scripts/monitoring_node.py

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from std_srvs.srv import Trigger
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton
from PyQt5.QtCore import Qt, QTimer
import sys
from PyQt5.QtGui import QFont

class LogViewer(QWidget):
    def __init__(self, monitoring_node):
        super().__init__()
        self.monitoring_node = monitoring_node
        self.setWindowTitle("Monitoring Logs")
        self.setFixedSize(600, 800)
        layout = QVBoxLayout()

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setFont(QFont("Courier", 10))
        layout.addWidget(self.log_text)

        self.emergency_button = QPushButton("Emergency Stop")
        self.emergency_button.clicked.connect(self.monitoring_node.send_emergency_stop_request)
        layout.addWidget(self.emergency_button)

        self.setLayout(layout)

class MonitoringNode(Node):
    def __init__(self, log_viewer):
        super().__init__('monitoring_node')
        self.log_viewer = log_viewer
        self.create_subscription(String, '/central_control/logs', self.log_callback, 10)
        
        # Trigger 서비스 클라이언트 생성
        self.emergency_stop_client = self.create_client(Trigger, '/monitoring/emergency_stop')

    def log_callback(self, msg):
        log_entry = msg.data
        self.log_viewer.append_log(log_entry)
        self.get_logger().info(f"Log received: {log_entry}")

    def send_emergency_stop_request(self):
        if not self.emergency_stop_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().error('/monitoring/emergency_stop service is not available.')
            return

        request = Trigger.Request()
        future = self.emergency_stop_client.call_async(request)
        future.add_done_callback(self.handle_emergency_stop_response)

    def handle_emergency_stop_response(self, future):
        try:
            response = future.result()
            if response.success:
                self.get_logger().info('Emergency stop successful.')
                self.log_viewer.append_log('Emergency stop successful.')
            else:
                self.get_logger().warning('Emergency stop failed.')
                self.log_viewer.append_log('Emergency stop failed.')
        except Exception as e:
            self.get_logger().error(f'Error calling emergency stop: {e}')
            self.log_viewer.append_log(f'Error: {e}')

def main(args=None):
    rclpy.init(args=args)
    app = QApplication(sys.argv)

    # MonitoringNode를 먼저 생성
    monitoring_node = MonitoringNode(None)  # 임시로 None 전달
    log_viewer = LogViewer(monitoring_node)  # MonitoringNode를 LogViewer에 전달
    monitoring_node.log_viewer = log_viewer  # MonitoringNode에 LogViewer 참조 추가

    log_viewer.show()

    # QTimer를 사용하여 ROS2 스핀과 Qt 이벤트 루프 통합
    timer = QTimer()
    timer.timeout.connect(lambda: rclpy.spin_once(monitoring_node, timeout_sec=0.1))
    timer.start(100)  # 100ms마다 spin_once 호출

    exit_code = app.exec_()

    monitoring_node.destroy_node()
    rclpy.shutdown()
    sys.exit(exit_code)
    
if __name__ == '__main__':
    main()
