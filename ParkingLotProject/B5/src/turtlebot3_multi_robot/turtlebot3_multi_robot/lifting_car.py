#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
from gazebo_msgs.srv import SetJointPositions

class LiftingCarController(Node):
    def __init__(self):
        super().__init__('lifting_car')
        
        # 구독할 토픽 설정
        self.subscription = self.create_subscription(
            Bool,
            '/change_cylinder_length',
            self.callback,
            10  # 큐 사이즈
        )
        
        # Gazebo 서비스 연결 설정
        self.client = self.create_client(SetJointPositions, '/gazebo/set_joint_positions')
        
        # Gazebo 서비스가 준비될 때까지 기다림
        while not self.client.wait_for_service(timeout_sec=5.0):
            self.get_logger().info('Waiting for /gazebo/set_joint_positions service...')
        
        # 초기 값 설정
        self.model_name = "turtlebot3_waffle"
        self.joint_name = "cylinder_vertical_joint"
        self.default_position = 0.0
        self.extended_position = 0.2  # 최대 확장 길이 (0.13m -> 0.33m)

        self.get_logger().info('Lifting Car Controller Initialized!')

    def callback(self, msg):
        if msg.data:
            self.get_logger().info("Extending cylinder to maximum position")
            position = self.extended_position
        else:
            self.get_logger().info("Retracting cylinder to default position")
            position = self.default_position

        request = SetJointPositions.Request()
        request.model_name = self.model_name
        request.joint_names = [self.joint_name]
        request.positions = [position]

        future = self.client.call_async(request)
        future.add_done_callback(self.response_callback)

    def response_callback(self, future):
        try:
            response = future.result()
            self.get_logger().info(f"Set cylinder position success: {response.success}")
        except Exception as e:
            self.get_logger().error(f"Service call failed: {e}")


def main(args=None):
    rclpy.init(args=args)
    node = LiftingCarController()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Shutting down Lifting Car Controller...')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
