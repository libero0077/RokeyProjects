# 노드 3 (RobotController) 코드 수정

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
## 2D pose estimate을 자동으로 해주기 위해 추가 ####
import time  # 초기화 대기를 위해 필요
from nav2_msgs.srv import SetInitialPose  # SetInitialPose 서비스 추가

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
        self.subscription  # prevent unused variable warning

        # 액션 클라이언트 생성
        self.action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

        # 위치 좌표 정의
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

        ############################ 로봇 상태를 퍼블리시하기 위한 퍼블리셔 생성 ####################
        self.status_publisher = self.create_publisher(String, 'robot_status', qos_profile)
        self.get_logger().info("Robot Status Publisher Initialized.")
        ####################################################################################

        ### 2D pose estimate을 자동으로 해주는 과정 ####################################
        # SetInitialPose 서비스 클라이언트 생성
        self.set_initial_pose_client = self.create_client(SetInitialPose, '/set_initial_pose')

        # 서비스 초기화 대기
        while not self.set_initial_pose_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for SetInitialPose service...')

        # 초기 위치 설정
        self.set_initial_pose()
        ##############################################################################

    ########### 2D pose estimate을 자동으로 해주는 과정 ###############
    def set_initial_pose(self):
        """SetInitialPose 서비스를 사용하여 초기 위치를 설정"""
        req = SetInitialPose.Request()

        # 초기 위치 설정
        req.pose.header.frame_id = 'map'
        req.pose.pose.pose.position.x = 0.02887068462523727
        req.pose.pose.pose.position.y = -0.012281313266620303
        req.pose.pose.pose.position.z = 0.0

        # 초기 자세 설정 (쿼터니언 값 사용)
        req.pose.pose.pose.orientation.x = 0.0
        req.pose.pose.pose.orientation.y = 0.0
        req.pose.pose.pose.orientation.z = -0.0020148885693665403
        req.pose.pose.pose.orientation.w = 0.9999979701099663

        # 초기 공분산 설정
        req.pose.pose.covariance = [
            0.17590620940375784, -0.017164822007954904, 0.0, 0.0, 0.0, 0.0,
            -0.017164822007954904, 0.2120207762335773, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0, 0.0, 0.06125552509931215
        ]

        # 서비스 호출
        future = self.set_initial_pose_client.call_async(req)
        future.add_done_callback(self.set_initial_pose_callback)

    ###### 아래 메서드는 2D pose estimate가 제대로 되었는지 확인을 꼭 해야한다면 필요하지만, #####
    ###### 굳이 확인을 하지 않아도 된다면 주석 처리해도 괜찮음 ################################
    def set_initial_pose_callback(self, future):
        try:
            response = future.result()
            self.get_logger().info('Initial pose set successfully.')
        except Exception as e:
            self.get_logger().error(f'Failed to set initial pose: {str(e)}')
    #########################################################

    def command_callback(self, msg):
        """로봇 명령을 수신하여 처리하는 콜백 함수"""
        try:
            data = json.loads(msg.data)
            command = data.get('command')
            position_key = data.get('position')
            order_item_ids = data.get('order_item_ids', [])

            if command == 'move' and position_key in self.positions:
                position = self.positions[position_key]
                
                # 로봇 이동 시작 상태 퍼블리시
                status_msg = String()
                
                # Standardizing message format with JSON
                status_data = {
                    "status": "",
                    "position": position_key,
                    "order_item_ids": order_item_ids
                }
                
                # Set the appropriate status based on the position
                if position_key == 'waiting':
                    status_data["status"] = "로봇이 대기 위치로 이동 중입니다."
                elif position_key == 'kitchen':
                    status_data["status"] = "로봇이 주방 위치로 이동 중입니다."
                else:
                    status_data["status"] = f"로봇이 {order_item_ids}을 배송하기 위해 {position_key}으로 이동 중입니다."

                # Publish the message as a JSON string
                status_msg.data = json.dumps(status_data)
                self.status_publisher.publish(status_msg)
                self.get_logger().info(f"Published robot status: {status_msg.data}")  # 추가된 로그

                # Move to the target position
                self.move_to_position(position, position_key, order_item_ids)
            else:
                self.get_logger().warn(f"Unknown command or position: {command}, {position_key}")
        except json.JSONDecodeError:
            self.get_logger().error("Failed to decode JSON from robot_command")

    def move_to_position(self, position, position_key, order_item_ids):
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
        self._send_goal_future.add_done_callback(lambda future: self.goal_response_callback(future, position_key, order_item_ids))

    def goal_response_callback(self, future, position_key, order_item_ids):
        """액션 서버로부터의 응답을 처리하는 콜백 함수"""
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            return

        self.get_logger().info('Goal accepted :)')

        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(lambda future: self.get_result_callback(future, position_key, order_item_ids))

    def get_result_callback(self, future, position_key, order_item_ids):
        """액션 수행 결과를 처리하는 콜백 함수"""
        result = future.result().result
        status = future.result().status

        if status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info('Goal succeeded!')

            # 목표 도착 상태 퍼블리시
            status_msg = {
                "status": "",
                "position": position_key,
                "order_item_ids": order_item_ids
            }

            if position_key == 'waiting':
                status_msg["status"] = "대기 위치입니다."
            elif position_key == 'kitchen':
                status_msg["status"] = "주방 위치입니다."
            elif "table_" in position_key:  # 테이블에 도착했을 경우
                status_msg["status"] = (
                    "음식이 도착했습니다. "
                    "음식을 수령하셨다면 복귀 버튼을 눌러주세요."
                )
            else:
                status_msg["status"] = f"{position_key} 위치입니다."

            # JSON 직렬화 후 퍼블리시
            self.status_publisher.publish(String(data=json.dumps(status_msg)))
            self.get_logger().info(f"Published robot status: {status_msg}")
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