import rclpy
from rclpy.node import Node
from std_msgs.msg import String  # 상태 메시지로 문자열 사용
import time

class RobotStatusNode(Node):
    def __init__(self):
        super().__init__('robot_status')
        
        # 상태 메시지를 퍼블리시
        self.publisher_ = self.create_publisher(String, 'robot_status', 10)
        
        # 상태 리스트
        self.status_list = ["이동 중", "물체 인식 중", "작업 중", "대기 중"]
        self.current_status_index = 0
        
        # 주기적으로 상태를 퍼블리시하는 타이머 설정
        self.timer = self.create_timer(2.0, self.publish_status)  # 2초마다 상태 변경

        ################ 관리자 이메일 초기값 설정 ######################
        self.declare_parameter("admin_email", "default@example.com")

    def publish_status(self):
        # 현재 상태를 퍼블리시
        msg = String()
        msg.data = self.status_list[self.current_status_index]
        self.publisher_.publish(msg)
        self.get_logger().info(f'Published status: {msg.data}')

        # 다음 상태로 변경
        self.current_status_index = (self.current_status_index + 1) % len(self.status_list)


def main(args=None):
    rclpy.init(args=args)

    robot_status_node = RobotStatusNode()

    try:
        rclpy.spin(robot_status_node)  # 노드 실행
    except KeyboardInterrupt:
        robot_status_node.get_logger().info('Shutting down robot_status node...')
    finally:
        robot_status_node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
