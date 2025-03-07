import math
import random
import time
import rclpy
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from std_msgs.msg import Header, String
from rclpy.action import ActionClient
from control_msgs.action import GripperCommand
from rclpy.node import Node
from sensor_msgs.msg import JointState, Image
from cv_bridge import CvBridge
import os
import threading
import cv2

R1 = 130
R2 = 124
R3 = 126

TH1_OFFSET = -math.atan2(0.024, 0.128)
TH2_OFFSET = -0.5 * math.pi - TH1_OFFSET

JOINT_NAMES = ['joint1', 'joint2', 'joint3', 'joint4']
GRIPPER_OPEN = 0.025
GRIPPER_CLOSE = -0.015
WAIT_TIME = 3

REGIONS = [
    {'x': 130, 'y': 50, 'z': (150, 200)},
    {'x': 130, 'y': 0, 'z': (150, 200)},
    {'x': 130, 'y': -40, 'z': (150, 200)},
    {'x': 80, 'y': 50, 'z': (150, 210)},
    {'x': 80, 'y': 0, 'z': (150, 210)},
    {'x': 80, 'y': -40, 'z': (150, 200)}
]

def solv2(r1, r2, r3):
    d1 = (r3**2 - r2**2 + r1**2) / (2 * r3)
    d2 = (r3**2 + r2**2 - r1**2) / (2 * r3)

    if abs(d1 / r1) > 1 or abs(d2 / r2) > 1:
        raise ValueError("Invalid input to acos")

    s1 = math.acos(max(-1.0, min(1.0, d1 / r1)))
    s2 = math.acos(max(-1.0, min(1.0, d2 / r2)))
    return s1, s2

def solv_robot_arm2(x, y, z, r1, r2, r3):
    Rt = math.sqrt(x**2 + y**2 + z**2)
    St = math.asin(max(-1.0, min(1.0, z / Rt)))
    Sxy = math.atan2(y, x)

    s1, s2 = solv2(r1, r2, Rt)
    sr1 = math.pi / 2 - (s1 + St)
    sr2 = s1 + s2
    sr3 = math.pi - (sr1 + sr2)
    return Sxy, sr1, sr2, sr3

def clamp_angle(angle, min_value, max_value):
    return max(min_value, min(max_value, angle))

class Turtlebot3ManipulationWithCamera(Node):
    def __init__(self):
        super().__init__('turtlebot3_manipulation_with_camera')

        # 상태 플래그
        self.stop_flag = True  # 초기에는 정지 상태
        self.current_thread = None

        self.train_images_subscriber = self.create_subscription(
            String, '/collect_data_control', self.collect_data_control_callback, 10
        )

        self.train_images_publisher = self.create_publisher(String, '/collect_commend', 10)

        self.joint_pub = self.create_publisher(JointTrajectory, '/arm_controller/joint_trajectory', 10)
        self.gripper_action_client = ActionClient(self, GripperCommand, 'gripper_controller/gripper_cmd')
        self.joint_subscription = self.create_subscription(JointState, '/joint_states', self.joint_state_callback, 10)

        self.image_subscription = self.create_subscription(Image, 'usb_camera/image_raw', self.image_callback, 10)
        self.bridge = CvBridge()

        self.current_gripper = GRIPPER_OPEN
        self.current_angles = [0.0, 0.0, 0.0, 0.0]
        self.current_frame = None

        self.image_save_path = os.path.expanduser("~/autotrain/images")
        os.makedirs(self.image_save_path, exist_ok=True)

        self.current_index = self.get_highest_image_index()

        self.joint_update_event = threading.Event()

        if not self.wait_for_joint_update():
            self.get_logger().error("Failed to initialize joint states. Using default angles.")

    def collect_data_control_callback(self, msg):
        """collect_data_control 토픽 콜백"""
        self.get_logger().info(f"Received message from /collect_data_control: {msg.data}")

        # 명령을 /collect_commend로 그대로 퍼블리시
        forward_msg = String(data=msg.data)
        self.train_images_publisher.publish(forward_msg)
        self.get_logger().info(f"Forwarded message to /collect_commend: {msg.data}")

        # start 명령 처리
        if msg.data.lower() == "start":
            # stop_flag를 False로 하여 동작 시작
            self.stop_flag = False
            if self.current_thread is None or not self.current_thread.is_alive():
                self.current_thread = threading.Thread(target=self.random_movement_and_capture, args=(50,))
                self.current_thread.start()

        # stop 명령 처리
        elif msg.data.lower() == "stop":
            # stop_flag를 True로 하여 동작 중지
            self.stop_flag = True

    def get_highest_image_index(self):
        max_index = 0
        for filename in os.listdir(self.image_save_path):
            if filename.startswith("image_") and filename.endswith(".jpg"):
                try:
                    index = int(filename.split("_")[1].split(".")[0])
                    max_index = max(max_index, index)
                except ValueError:
                    continue
        return max_index

    def wait_for_joint_update(self, timeout=5.0):
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.joint_update_event.wait(timeout=0.1):
                if self.current_angles != [0.0, 0.0, 0.0, 0.0]:
                    self.get_logger().info(f"Joint states initialized: {self.current_angles}")
                    self.joint_update_event.clear()
                    return True
        return False

    def joint_state_callback(self, msg):
        joint_positions = {}
        for name, position in zip(msg.name, msg.position):
            joint_positions[name] = position

        try:
            self.current_angles = [
                joint_positions['joint1'],
                joint_positions['joint2'],
                joint_positions['joint3'],
                joint_positions['joint4']
            ]
            self.joint_update_event.set()
        except KeyError as e:
            self.get_logger().warning(f"Missing joint data: {e}")

    def image_callback(self, msg):
        try:
            self.current_frame = self.bridge.imgmsg_to_cv2(msg, "bgr8")
            self.get_logger().info("Camera frame received successfully.")
        except Exception as e:
            self.get_logger().error(f"Failed to process image: {e}")

    def move_arm(self, x, y, z):
        if not self.wait_for_joint_update():
            self.get_logger().error("Cannot move arm: joint states not available.")
            return

        try:
            Sxy, sr1, sr2, sr3 = solv_robot_arm2(x, y, z, R1, R2, R3)
            target_angles = [
                clamp_angle(Sxy, -math.pi, math.pi),
                clamp_angle(sr1 + TH1_OFFSET, -math.pi / 2, math.pi / 2),
                clamp_angle(sr2 + TH2_OFFSET, -math.pi / 2, math.pi / 2),
                clamp_angle(sr3, 0, math.pi)
            ]

            msg = JointTrajectory(
                header=Header(frame_id=''),
                joint_names=JOINT_NAMES,
                points=[
                    JointTrajectoryPoint(
                        positions=target_angles,
                        velocities=[0.0] * 4,
                        time_from_start=rclpy.time.Duration(seconds=WAIT_TIME).to_msg(),
                    )
                ],
            )

            self.joint_pub.publish(msg)
            self.get_logger().info(f"Moving arm to x={x}, y={y}, z={z}")

            # 이동 대기
            time.sleep(4)

        except Exception as e:
            self.get_logger().error(f"Failed to move arm: {e}")

    def save_image(self):
        if self.current_frame is not None:
            self.current_index += 1
            image_filename = os.path.join(self.image_save_path, f"image_{self.current_index}.jpg")
            cv2.imwrite(image_filename, self.current_frame)
            self.get_logger().info(f"Image saved to {image_filename}")
        else:
            self.get_logger().warning("No image received yet.")

    def random_movement_and_capture(self, num_moves):
        for i in range(num_moves):
            if self.stop_flag:
                self.get_logger().info("Stop flag is True, stopping movements.")
                break

            region = random.choice(REGIONS)
            x = region['x']
            y = region['y']
            z = random.randint(region['z'][0] // 10, region['z'][1] // 10) * 10
            self.get_logger().info(f"Move {i+1}/{num_moves}: x={x:.2f}, y={y:.2f}, z={z:.2f}")

            self.move_arm(x, y, z)
            if self.stop_flag:
                self.get_logger().info("Stop flag is True, stopping movements.")
                break

            time.sleep(6)  # 위치 도달 후 이미지 갱신 대기

            self.save_image()
            self.get_logger().info(f"Captured image {i + 1}/{num_moves}.")

def main(args=None):
    rclpy.init(args=args)
    from rclpy.executors import MultiThreadedExecutor
    executor = MultiThreadedExecutor()

    node = Turtlebot3ManipulationWithCamera()
    executor.add_node(node)

    try:
        executor.spin()
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down gracefully...")
    except Exception as e:
        node.get_logger().error(f"Runtime error: {e}")
    finally:
        executor.shutdown()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()
