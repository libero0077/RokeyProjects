import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.duration import Duration
from std_msgs.msg import String
from boxproject_interfaces.action import Taskaction  # TaskAction은 사용자 정의 액션 인터페이스

class RobotArmNode(Node):
    def __init__(self):
        super().__init__('robot_arm_node')

        self.action_server = ActionServer(
            self,
            Taskaction,
            '/robot_arm_task',
            self.execute_callback,
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback,
        )

        self.get_logger().info("Robot Arm Node initialized with Action Server.")

        # 상태 변수 초기화
        self.current_task = None
        self.is_paused = False

    def goal_callback(self, goal_request):
        """Goal 요청 처리: 모든 작업을 수락"""
        self.get_logger().info(f"Received goal request: {goal_request.task}")
        return GoalResponse.ACCEPT

    def cancel_callback(self, goal_handle):
        """Cancel 요청 처리"""
        self.get_logger().info(f"Cancel request received for task: {self.current_task}")
        return CancelResponse.ACCEPT

    async def execute_callback(self, goal_handle):
        """Goal 실행"""
        task = goal_handle.request.task
        self.get_logger().info(f"Executing task: {task}")

        feedback = Taskaction.Feedback()
        feedback.status = f"Starting task {task}."
        goal_handle.publish_feedback(feedback)

        # Simulate task steps
        for step in ["moving", "gripping box", "lifting box", "placing on conveyor"]:
            if goal_handle.is_cancel_requested:
                self.get_logger().info(f"Task {task} canceled at step: {step}.")
                goal_handle.canceled()
                return Taskaction.Result(result=f"Task {task} canceled.")
            
            feedback.status = f"{task}: {step}"
            goal_handle.publish_feedback(feedback)
            self.get_logger().info(feedback.status)
            await self.sleep(1)  # Simulate step execution

        self.get_logger().info(f"Task {task} completed.")
        goal_handle.succeed()
        return Taskaction.Result(result=f"Task {task} completed.")

    def pause_task(self):
        """현재 작업 일시 중지"""
        if self.current_task:
            self.is_paused = True
            self.get_logger().info(f"Task {self.current_task} paused.")

    def resume_task(self):
        """일시 중지된 작업 재개"""
        if self.is_paused:
            self.is_paused = False
            self.get_logger().info(f"Task {self.current_task} resumed.")

    async def sleep(self, seconds: float):
        """비동기 대기"""
        await self.get_clock().sleep_for(Duration(seconds=seconds))

def main(args=None):
    rclpy.init(args=args)
    node = RobotArmNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down Robot Arm Node.")
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()