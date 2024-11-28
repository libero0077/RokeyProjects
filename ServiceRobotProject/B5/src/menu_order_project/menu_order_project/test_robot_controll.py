# 추후 수정해야할 파일 => 재수정

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped, Quaternion
from rclpy.qos import QoSProfile
import json
import math

from action_msgs.msg import GoalStatus
from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose

'''
RobotController 클래스:
subscription: 'robot_command' 토픽을 구독하여 명령을 수신
action_client: navigate_to_pose 액션 서버에 목표 위치를 보냄
positions: 각 위치에 대한 좌표를 딕셔너리로 저장 (임의의 좌표 값이며, 나중에 실제 좌표로 수정 )
명령 처리 (command_callback): 수신한 명령에 따라 로봇을 이동
이동 함수 (move_to_position): 목표 위치를 설정하고 액션 서버에 목표를 보냄
쿼터니언 변환 함수 (euler_to_quaternion): 오일러 각도를 쿼터니언으로 변환
'''
class RobotController(Node):
    def __init__(self):
        super().__init__('robot_controller')

        # QoS 설정
        qos_profile = QoSProfile(depth=10)

        # 로봇 명령을 수신하기 위한 구독자 생성
        self.subscription = self.create_subscription(
            String,
            'robot_command',
            self.command_callback,
            qos_profile
        )

        # 액션 클라이언트 생성
        self.action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

        # 위치 좌표 정의 (amcl_pose로부터 추출한 실제 좌표로 업데이트)
        self.positions = {
            'waiting': {'x': 1.5287821904725307, 'y': -1.6564363922167273, 'theta': 0.08051796784565991},
            'kitchen': {'x': -0.45619495436058893, 'y': 0.5627857193272424, 'theta': 0.11337987469541375},
            'table_1': {'x': 0.4608367135716978, 'y': 1.5926609706591535, 'theta': 0.19478139000050054},
            'table_2': {'x': 0.44415937076368955, 'y': 0.4999638724737042, 'theta': -0.14039798973855175},
            'table_3': {'x': 0.4398148607080405, 'y': -0.5713670076206864, 'theta': -0.10709628753351007},
            'table_4': {'x': 1.983667568246241, 'y': 2.0623549505022147, 'theta': -0.17066896417045635},
            'table_5': {'x': 2.0777497362532062, 'y': 1.0475412036423666, 'theta': -0.12801790809238955},
            'table_6': {'x': 1.9639341467418672, 'y': -1.1660702113994799, 'theta': 0.11646105876604701},
            'table_7': {'x': 3.193308523192465, 'y': 2.0342932481312683, 'theta': -0.09997536240913828},
            'table_8': {'x': 3.109162110811999, 'y': 1.064675670588104, 'theta': 0.0911863336818867},
            'table_9': {'x': 3.153391448984137, 'y': -1.0491125084255173, 'theta': -0.19493162164767266},
        }

    def command_callback(self, msg):
        """로봇 명령을 수신하여 처리하는 콜백 함수"""
        data = json.loads(msg.data)
        command = data['command']
        position_key = data.get('position')

        if command == 'move' and position_key in self.positions:
            position = self.positions[position_key]
            self.move_to_position(position)
        else:
            self.get_logger().warn(f"Unknown command or position: {command}, {position_key}")

    def move_to_position(self, position):
        """로봇을 지정된 위치로 이동시키는 함수"""
        # NavigateToPose 목표 메시지 생성
        goal_msg = NavigateToPose.Goal()

        # 목표 위치 설정
        goal_msg.pose.pose.position.x = position['x']
        goal_msg.pose.pose.position.y = position['y']

        # 오일러 각도를 쿼터니언으로 변환하여 방향 설정
        q = self.euler_to_quaternion(0, 0, position['theta'])
        goal_msg.pose.pose.orientation = q

        # 좌표 프레임 설정
        goal_msg.pose.header.frame_id = 'map'
        goal_msg.pose.header.stamp = self.get_clock().now().to_msg()

        # 액션 서버가 실행될 때까지 대기
        while not self.action_client.wait_for_server(timeout_sec=1.0):
            self.get_logger().info('Waiting for action server...')

        # 목표를 액션 서버로 보내기
        self._send_goal_future = self.action_client.send_goal_async(goal_msg, feedback_callback=self.feedback_callback)
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        """액션 서버로부터의 응답을 처리하는 콜백 함수"""
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            return

        self.get_logger().info('Goal accepted :)')

        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        """액션 수행 결과를 처리하는 콜백 함수"""
        result = future.result().result
        status = future.result().status

        if status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info('Goal succeeded!')
        else:
            self.get_logger().info(f'Goal failed with status: {status}')

    def feedback_callback(self, feedback_msg):
        """액션 수행 중 피드백을 처리하는 콜백 함수"""
        feedback = feedback_msg.feedback
        current_x = feedback.current_pose.pose.position.x
        current_y = feedback.current_pose.pose.position.y
        self.get_logger().info(f'Current position: x={current_x}, y={current_y}')

    def euler_to_quaternion(self, roll, pitch, yaw):
        """오일러 각도를 쿼터니언으로 변환하는 함수"""
        qx = math.sin(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) - \
             math.cos(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)
        qy = math.cos(roll/2) * math.sin(pitch/2) * math.cos(yaw/2) + \
             math.sin(roll/2) * math.cos(pitch/2) * math.sin(yaw/2)
        qz = math.cos(roll/2) * math.cos(pitch/2) * math.sin(yaw/2) - \
             math.sin(roll/2) * math.sin(pitch/2) * math.cos(yaw/2)
        qw = math.cos(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) + \
             math.sin(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)
        return Quaternion(x=qx, y=qy, z=qz, w=qw)

def main(args=None):
    rclpy.init(args=args)
    robot_controller = RobotController()
    rclpy.spin(robot_controller)
    robot_controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
