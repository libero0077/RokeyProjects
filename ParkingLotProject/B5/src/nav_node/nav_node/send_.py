#!/usr/bin/env python3
# ~/ros2_ws/src/parking_robot/parking_robot/send_goal_pose.py

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose
import math
#(12.75, 28.5)
(1, 4, "0000"), (1, 5, "0000"), (1, 8, "0000"), (1, 9, "0000"), (1, 10, "0000"), (1, 12, "0000"), (1, 13, "0000"), (3, 4, "0000"), (3, 9, "0000"), (3, 12, "0000"), (3, 14, "0000"), (4, 2, "0000"), (4, 4, "0000"), (4, 5, "0000"), (4, 7, "0000"), 
(4, 12, "0000"), (4, 13, "0000"), (6, 3, "0000"), (6, 8, "0000"), (6, 13, "0000"), (7, 4, "0000"), (7, 5, "0000"), (7, 8, "0000"), (7, 9, "0000"), (9, 1, "0000"), (9, 2, "0000"), (9, 4, "0000"), (9, 8, "0000"), (9, 12, "0000"), (9, 13, "0000")
class GoalPosePublisher(Node):
    def __init__(self):
        super().__init__("goal_pose_publisher")
        # 퍼블리셔 생성: robot1과 robot2에 대해 개별적으로 퍼블리시
        self.publisher_robot1 = self.create_publisher(Pose, "tb1/goal_pose", 10)
        self.publisher_robot2 = self.create_publisher(Pose, "tb2/goal_pose", 10)
        self.get_logger().info("GoalPosePublisher Node has been started.")

    def publish_goal_pose(self, robot_id, x, y, yaw_degrees):
        """
        특정 로봇에 goal_pose 메시지를 퍼블리시합니다.
        :param robot_id: 'robot1' 또는 'robot2'
        :param x: 목표 x 좌표 (float)
        :param y: 목표 y 좌표 (float)
        :param yaw_degrees: 목표 방향 (도 단위, float)
        """
        if robot_id not in ["robot1", "robot2"]:
            self.get_logger().error("Invalid robot_id. Use 'robot1' or 'robot2'.")
            return

        # 오일러 각을 쿼터니언으로 변환
        yaw_rad = math.radians(yaw_degrees)
        qx, qy, qz, qw = self.euler_to_quaternion(0, 0, yaw_rad)

        # Pose 메시지 생성
        pose_msg = Pose()
        pose_msg.position.x = float(x)
        pose_msg.position.y = float(y)
        pose_msg.position.z = 0.0  # 평면 이동 가정
        pose_msg.orientation.x = qx
        pose_msg.orientation.y = qy
        pose_msg.orientation.z = qz
        pose_msg.orientation.w = qw

        # 퍼블리시
        if robot_id == "robot1":
            self.publisher_robot1.publish(pose_msg)
            self.get_logger().info(
                f"Published goal_pose to robot1: x={x}, y={y}, yaw={yaw_degrees} degrees"
            )
        else:
            self.publisher_robot2.publish(pose_msg)
            self.get_logger().info(
                f"Published goal_pose to robot2: x={x}, y={y}, yaw={yaw_degrees} degrees"
            )

    @staticmethod
    def euler_to_quaternion(roll, pitch, yaw):
        """
        오일러 각(roll, pitch, yaw)을 쿼터니언으로 변환합니다.
        """
        qx = math.sin(roll / 2) * math.cos(pitch / 2) * math.cos(yaw / 2) - math.cos(
            roll / 2
        ) * math.sin(pitch / 2) * math.sin(yaw / 2)
        qy = math.cos(roll / 2) * math.sin(pitch / 2) * math.cos(yaw / 2) + math.sin(
            roll / 2
        ) * math.cos(pitch / 2) * math.sin(yaw / 2)
        qz = math.cos(roll / 2) * math.cos(pitch / 2) * math.sin(yaw / 2) - math.sin(
            roll / 2
        ) * math.sin(pitch / 2) * math.cos(yaw / 2)
        qw = math.cos(roll / 2) * math.cos(pitch / 2) * math.cos(yaw / 2) + math.sin(
            roll / 2
        ) * math.sin(pitch / 2) * math.sin(yaw / 2)
        return (qx, qy, qz, qw)


def main(args=None):
    rclpy.init(args=args)
    node = GoalPosePublisher()

    try:
        while True:
            print("\n=== Goal Pose Publisher ===")
            robot_id = input("Enter robot ID ('robot1' or 'robot2'): ").strip()
            try:
                x = float(input("Enter target x coordinate: ").strip())
                y = float(input("Enter target y coordinate: ").strip())
                yaw = float(input("Enter target yaw (degrees): ").strip())
            except ValueError:
                print(
                    "Invalid input. Please enter numeric values for coordinates and yaw."
                )
                continue

            node.publish_goal_pose(robot_id, x, y, yaw)

    except KeyboardInterrupt:
        print("\nShutting down GoalPosePublisher Node.")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
