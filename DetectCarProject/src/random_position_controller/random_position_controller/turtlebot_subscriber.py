import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped

class TurtleBotController(Node):
    def __init__(self):
        super().__init__('turtlebot_controller')

        # 웨이포인트 수신
        self.subscription = self.create_subscription(
            PoseStamped,
            '/goal_pose',  # 퍼블리셔에서 발행하는 좌표 주제
            self.target_callback,
            10
        )

        # 네비게이션 목표 지점을 퍼블리시
        self.publisher_ = self.create_publisher(PoseStamped, '/navigate_to_pose', 10)
        self.get_logger().info("TurtleBot Controller Node Initialized")

    def target_callback(self, msg):
        """웨이포인트를 수신하고 네비게이션 스택으로 전달"""
        self.get_logger().info(f"Received waypoint: x={msg.pose.position.x}, y={msg.pose.position.y}")
        self.publisher_.publish(msg)
        self.get_logger().info(f"Published to /navigate_to_pose: x={msg.pose.position.x}, y={msg.pose.position.y}")

def main(args=None):
    rclpy.init(args=args)
    node = TurtleBotController()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("TurtleBot Controller shutting down.")
    finally:
        rclpy.shutdown()

if __name__ == '__main__':
    main()
