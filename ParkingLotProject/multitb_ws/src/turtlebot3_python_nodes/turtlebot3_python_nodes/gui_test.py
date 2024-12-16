import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import random
import json
import time

class TestPublisher(Node):
    def __init__(self):
        super().__init__('test_publisher')
        # 주차장 상태 퍼블리셔
        self.parking_status_publisher = self.create_publisher(String, '/parking_status', 10)
        # 주차장 로그 퍼블리셔
        self.log_publisher = self.create_publisher(String, '/log', 10)
        # 주차장 상태 퍼블리셔
        self.robot_state_publisher = self.create_publisher(String, '/robot_state', 10)
        self.timer = self.create_timer(2.0, self.publish_messages)

    def publish_messages(self):
        # 로그 메시지 발행
        log_levels = ["INFO", "WARN"]
        log_msg = String()
        log_data = {
            "level": random.choice(log_levels),
            "log": f"Test log message at {time.time()}"
        }
        log_msg.data = json.dumps(log_data)
        self.log_publisher.publish(log_msg)

        self.get_logger().info(f"Published log message: [{log_data['level']}]")

        # 로봇 상태 메시지 발행
        robot_states = ["이동 중", "물체 인식 중", "작업 중", "대기 중"]
        robot_state_msg = String()
        robot_state_data = {
            "current_state": random.choice(robot_states),
            "current_position": [random.uniform(0, 10), random.uniform(0, 10)]
        }
        robot_state_msg.data = json.dumps(robot_state_data)
        self.robot_state_publisher.publish(robot_state_msg)

        self.get_logger().info(f"Published robot state: {robot_state_data}")
        
        # 주차장 상태 메시지 발행
        parking_status_msg = String()
        parking_status_data = {
            "available_spots": random.randint(0, 100),
            "is_full": random.choice([True, False]),
            "waiting_vehicles": random.randint(0, 10)
        }
        parking_status_msg.data = json.dumps(parking_status_data)
        self.parking_status_publisher.publish(parking_status_msg)

        self.get_logger().info(f"Published parking status: {parking_status_data}")

def main(args=None):
    rclpy.init(args=args)
    test_publisher = TestPublisher()
    rclpy.spin(test_publisher)
    test_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
