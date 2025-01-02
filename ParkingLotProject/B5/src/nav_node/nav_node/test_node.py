# ~/ros2_ws/src/parking_robot/parking_robot/nav_message_publisher_node.py

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped  # Pose에서 PoseStamped로 변경
import tkinter as tk
from tkinter import ttk
import threading
import time
import re
import math

class NavMessagePublisherNode(Node):
    def __init__(self):
        super().__init__("nav_message_publisher_node")
        self.publisher = self.create_publisher(String, "nav_message", 10)
        
        # 기존 'nav_callback' 토픽 구독 유지
        self.nav_callback_subscriber = self.create_subscription(
            String, "nav_callback", self.nav_callback_callback, 10
        )
        self.nav_callback_subscriber  # prevent unused variable warning

        # 새로운 '/vehicle_detected' 토픽 서브스크라이버 추가
        self.vehicle_detected_subscriber = self.create_subscription(
            String, "/vehicle_detected", self.vehicle_detected_callback, 10
        )
        self.vehicle_detected_subscriber  # prevent unused variable warning

        # Initialize GUI
        self.root = tk.Tk()
        self.root.title("Nav Message Publisher")

        # Create label and entry for publishing messages
        self.label = tk.Label(self.root, text="Enter your message:")
        self.label.pack(pady=5)

        self.entry = tk.Entry(self.root, width=50)
        self.entry.pack(pady=5)

        self.button = tk.Button(self.root, text="Publish", command=self.publish_message)
        self.button.pack(pady=10)

        # Create a text box to display 'nav_callback' messages
        self.callback_label = tk.Label(self.root, text="Nav Callback Messages:")
        self.callback_label.pack(pady=5)

        self.callback_text = tk.Text(self.root, height=15, width=60, state="disabled")
        self.callback_text.pack(pady=5)

        # Create a frame for tick timing controls
        self.tick_frame = tk.Frame(self.root)
        self.tick_frame.pack(pady=10)

        self.tick_label = tk.Label(self.tick_frame, text="Tick Interval (seconds):")
        self.tick_label.pack(side=tk.LEFT, padx=5)

        self.tick_interval = tk.DoubleVar(value=1.0)  # Default tick interval 1.0 second
        self.tick_slider = ttk.Scale(
            self.tick_frame, from_=0.1, to=10.0, orient=tk.HORIZONTAL, variable=self.tick_interval, command=self.update_tick_label
        )
        self.tick_slider.pack(side=tk.LEFT, padx=5)

        self.tick_value_label = tk.Label(self.tick_frame, text="1.0 s")
        self.tick_value_label.pack(side=tk.LEFT, padx=5)

        # Close ROS2 gracefully on GUI exit
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Initialize variables
        self.robot_status = {"robot1": "idle", "robot2": "idle"}
        self.robot_positions = {
            "robot1": (17.0, 4.0),  # (x, y)
            "robot2": (17.0, 6.0),  # (x, y)
        }
        self.status_lock = threading.Lock()  # 상태 접근을 위한 락 추가

        # Define map_grid transformation
        # 11 rows (0-10) and 19 columns (0-18)
        self.map_grid = []
        for y in range(11):
            row = []
            for x in range(19):
                row.append((float(x), float(y)))  # 수정: (x, y) 순서으로 변환
            self.map_grid.append(row)

        # 사용자 지정 변환 매핑 추가 (예시)
        # map_grid_transform[y][x] = (transformed_x, transformed_y)
        # 여기서 (y, x) -> (transformed_x, transformed_y)로 정확히 매핑
        self.map_grid_transform = [
            # y=0
            [
                (-28.5, 30.25), (-25.425, 30.25), (-22.575, 30.25), (-17.925, 30.25),
                (-15.0, 30.25), (-12.0, 30.25), (-9.075, 30.25),  (-4.425, 30.25),
                (-1.5, 30.25),  (1.5, 30.25),    (4.425, 30.25),  (9.075, 30.25),
                (12.0, 30.25),  (15.0, 30.25),   (17.925, 30.25), (22.575, 30.25),
                (25.425, 30.25), (28.5, 30.25),   (31.5, 30.25)
            ],
            # y=1
            [
                (-28.5, 24.25), (-25.425, 24.25), (-22.575, 24.25), (-17.925, 24.25),
                (-15.0, 24.25), (-12.0, 24.25), (-9.075, 24.25),  (-4.425, 24.25),
                (-1.5, 24.25),  (1.5, 24.25),    (4.425, 24.25),  (9.075, 24.25),
                (12.0, 24.25),  (15.0, 24.25),   (17.925, 24.25), (22.575, 24.25),
                (25.425, 24.25), (28.5, 24.25),   (31.5, 24.25)
            ],
            # y=2
            [
                (-28.5, 18.5), (-25.425, 18.5), (-22.575, 18.5), (-17.925, 18.5),
                (-15.0, 18.5), (-12.0, 18.5), (-9.075, 18.5),  (-4.425, 18.5),
                (-1.5, 18.5),  (1.5, 18.5),    (4.425, 18.5),  (9.075, 18.5),
                (12.0, 18.5),  (15.0, 18.5),   (17.925, 18.5), (22.575, 18.5),
                (25.425, 18.5), (28.5, 18.5),   (31.5, 18.5)
            ],
            # y=3
            [
                (-28.5, 12.75), (-25.425, 12.75), (-22.575, 12.75), (-17.925, 12.75),
                (-15.0, 12.75), (-12.0, 12.75), (-9.075, 12.75),  (-4.425, 12.75),
                (-1.5, 12.75),  (1.5, 12.75),    (4.425, 12.75),  (9.075, 12.75),
                (12.0, 12.75),  (15.0, 12.75),   (17.925, 12.75), (22.575, 12.75),
                (25.425, 12.75), (28.5, 12.75),   (31.5, 12.75)
            ],
            # y=4
            [
                (-28.5, 5.75), (-25.425, 5.75), (-22.575, 5.75), (-17.925, 5.75),
                (-15.0, 5.75), (-12.0, 5.75), (-9.075, 5.75),  (-4.425, 5.75),
                (-1.5, 5.75),  (1.5, 5.75),    (4.425, 5.75),  (9.075, 5.75),
                (12.0, 5.75),  (15.0, 5.75),   (17.925, 5.75), (22.575, 5.75),
                (25.425, 5.75), (28.5, 5.75),   (31.5, 5.75)
            ],
            # y=5
            [
                (-28.5, 0.0), (-25.425, 0.0), (-22.575, 0.0), (-17.925, 0.0),
                (-15.0, 0.0), (-12.0, 0.0), (-9.075, 0.0),  (-4.425, 0.0),
                (-1.5, 0.0),  (1.5, 0.0),    (4.425, 0.0),  (9.075, 0.0),
                (12.0, 0.0),  (15.0, 0.0),   (17.925, 0.0), (22.575, 0.0),
                (25.425, 0.0), (28.5, 0.0),   (31.5, 0.0)
            ],
            # y=6
            [
                (-28.5, -5.75), (-25.425, -5.75), (-22.575, -5.75), (-17.925, -5.75),
                (-15.0, -5.75), (-12.0, -5.75), (-9.075, -5.75),  (-4.425, -5.75),
                (-1.5, -5.75),  (1.5, -5.75),    (4.425, -5.75),  (9.075, -5.75),
                (12.0, -5.75),  (15.0, -5.75),   (17.925, -5.75), (22.575, -5.75),
                (25.425, -5.75), (28.5, -5.75),   (31.5, -5.75)
            ],
            # y=7
            [
                (-28.5, -12.75), (-25.425, -12.75), (-22.575, -12.75), (-17.925, -12.75),
                (-15.0, -12.75), (-12.0, -12.75), (-9.075, -12.75),  (-4.425, -12.75),
                (-1.5, -12.75),  (1.5, -12.75),    (4.425, -12.75),  (9.075, -12.75),
                (12.0, -12.75),  (15.0, -12.75),   (17.925, -12.75), (22.575, -12.75),
                (25.425, -12.75), (28.5, -12.75),   (31.5, -12.75)
            ],
            # y=8
            [
                (-28.5, -18.5), (-25.425, -18.5), (-22.575, -18.5), (-17.925, -18.5),
                (-15.0, -18.5), (-12.0, -18.5), (-9.075, -18.5),  (-4.425, -18.5),
                (-1.5, -18.5),  (1.5, -18.5),    (4.425, -18.5),  (9.075, -18.5),
                (12.0, -18.5),  (15.0, -18.5),   (17.925, -18.5), (22.575, -18.5),
                (25.425, -18.5), (28.5, -18.5),   (31.5, -18.5)
            ],
            # y=9
            [
                (-28.5, -24.25), (-25.425, -24.25), (-22.575, -24.25), (-17.925, -24.25),
                (-15.0, -24.25), (-12.0, -24.25), (-9.075, -24.25),  (-4.425, -24.25),
                (-1.5, -24.25),  (1.5, -24.25),    (4.425, -24.25),  (9.075, -24.25),
                (12.0, -24.25),  (15.0, -24.25),   (17.925, -24.25), (22.575, -24.25),
                (25.425, -24.25), (28.5, -24.25),   (31.5, -24.25)
            ],
            # y=10
            [
                (-28.5, -30.25), (-25.425, -30.25), (-22.575, -30.25), (-17.925, -30.25),
                (-15.0, -30.25), (-12.0, -30.25), (-9.075, -30.25),  (-4.425, -30.25),
                (-1.5, -30.25),  (1.5, -30.25),    (4.425, -30.25),  (9.075, -30.25),
                (12.0, -30.25),  (15.0, -30.25),   (17.925, -30.25), (22.575, -30.25),
                (25.425, -30.25), (28.5, -30.25),   (31.5, -30.25)
            ],
        ]

        # Update map_grid with transformed coordinates
        for y, row in enumerate(self.map_grid_transform):
            for x, transformed in enumerate(row):
                if 0 <= y < len(self.map_grid) and 0 <= x < len(self.map_grid[y]):
                    # Ensure all coordinates are floats
                    transformed_x = float(transformed[0])
                    transformed_y = float(transformed[1])
                    self.map_grid[y][x] = (
                        transformed_x,
                        transformed_y,
                    )  # 수정: (x, y) 순서
                    self.get_logger().info(
                        f"Map Grid Updated: ({y}, {x}) -> ({transformed_x}, {transformed_y})"
                    )
                else:
                    self.get_logger().warning(
                        f"Invalid grid coordinates during map_grid update: ({y}, {x})"
                    )

        # Create separate goal_pose publishers for each robot using PoseStamped
        self.goal_pose_publishers = {
            "robot1": self.create_publisher(PoseStamped, "tb1/goal_pose", 10),
            "robot2": self.create_publisher(PoseStamped, "tb2/goal_pose", 10),
        }

        # Start ROS2 spinning in a separate thread
        self.spin_thread = threading.Thread(target=self.spin_ros, daemon=True)
        self.spin_thread.start()

        # Start the tick timer
        self.tick_thread = threading.Thread(target=self.tick_loop, daemon=True)
        self.tick_thread.start()

    def publish_message(self):
        """Publish the text in the entry box to the 'nav_message' topic."""
        message = self.entry.get().strip()
        if message:
            msg = String()
            msg.data = message
            self.publisher.publish(msg)
            self.get_logger().info(f"Published: {message}")
            self.entry.delete(0, tk.END)  # Clear the entry box after publishing
        else:
            self.get_logger().warn("Empty message. Nothing published.")

    def nav_callback_callback(self, msg):
        """Callback function for the 'nav_callback' topic."""
        message = msg.data.strip()
        self.get_logger().info(f"Received on 'nav_callback': {message}")
        self.update_callback_text(message)
        self.process_nav_callback(message)

    def vehicle_detected_callback(self, msg):
        """Callback function for the '/vehicle_detected' topic."""
        message = msg.data.strip()
        self.get_logger().info(f"Received on '/vehicle_detected': {message}")
        self.process_vehicle_detected(message)

    def update_callback_text(self, message):
        """Update the text box with the received 'nav_callback' message."""
        self.callback_text.config(state="normal")
        self.callback_text.insert(tk.END, message + "\n")
        self.callback_text.see(tk.END)  # Auto-scroll to the end
        self.callback_text.config(state="disabled")

    def on_close(self):
        """Shut down ROS2 node when the GUI is closed."""
        self.get_logger().info("Shutting down NavMessagePublisherNode.")
        self.destroy_node()
        rclpy.shutdown()
        self.root.destroy()

    def run(self):
        """Run the tkinter main loop."""
        self.root.mainloop()

    def spin_ros(self):
        """Spin ROS2 to handle callbacks."""
        rclpy.spin(self)

    def tick_loop(self):
        """Loop that sends 'tick' messages at adjustable intervals."""
        while rclpy.ok():
            tick_interval = self.tick_interval.get()
            self.send_tick()
            time.sleep(tick_interval)

    def send_tick(self):
        """Send a 'tick' message."""
        msg = String()
        msg.data = "tick"
        self.publisher.publish(msg)
        self.get_logger().info("Published: tick")

    def update_tick_label(self, event):
        """Update the tick interval label based on slider."""
        current_value = self.tick_interval.get()
        self.tick_value_label.config(text=f"{current_value:.1f} s")

    def process_nav_callback(self, message):
        """
        Process messages received on 'nav_callback' topic.
        Update robot status and robot_positions accordingly.
        Send goal_pose commands based on map_grid_transform.
        """
        # Regex patterns to parse messages
        idle_pattern = r"robot(\d+) idle"
        position_pattern = r"robot(\d+) \((\d+),\s*(\d+)\)"
        pick_up_pattern = r"robot(\d+) pick_up"
        pick_off_pattern = r"robot(\d+) pick_off (\d+) \((\d+),\s*(\d+)\)"

        # Check for idle message
        idle_match = re.match(idle_pattern, message)
        if idle_match:
            robot_num = idle_match.group(1)
            robot_id = f"robot{robot_num}"
            with self.status_lock:
                self.robot_status[robot_id] = "idle"
            self.get_logger().info(f"{robot_id} is now idle.")
            return

        # Check for position message
        position_match = re.match(position_pattern, message)
        if position_match:
            robot_num = position_match.group(1)
            y = int(position_match.group(2))
            x = int(position_match.group(3))
            robot_id = f"robot{robot_num}"
            with self.status_lock:
                self.robot_status[robot_id] = "moving"
            self.get_logger().info(f"{robot_id} is moving to grid ({y}, {x}).")

            # Get transformed coordinates from map_grid_transform
            if 0 <= y < len(self.map_grid_transform) and 0 <= x < len(
                self.map_grid_transform[y]
            ):
                transformed_x, transformed_y = self.map_grid_transform[y][x]  # (x, y)
                self.get_logger().info(
                    f"{robot_id} target transformed position: ({transformed_x}, {transformed_y})"
                )
            else:
                self.get_logger().error(
                    f"Received invalid grid coordinates: ({y}, {x})"
                )
                return

            # Log the transformed coordinates
            self.get_logger().info(
                f"{robot_id} transformed coordinates for movement: ({transformed_x}, {transformed_y})"
            )

            # Get current position (x, y)
            current_x, current_y = self.robot_positions.get(robot_id, (0.0, 0.0))
            self.get_logger().info(
                f"{robot_id} current position: ({current_x}, {current_y})"
            )

            # **거리 및 각도 계산 제거**

            # Create PoseStamped message
            pose_stamped_msg = PoseStamped()
            pose_stamped_msg.header.frame_id = "map"
            pose_stamped_msg.header.stamp = self.get_clock().now().to_msg()
            pose_stamped_msg.pose.position.x = float(transformed_x)  # 실제 x 좌표 사용
            pose_stamped_msg.pose.position.y = float(transformed_y)  # 실제 y 좌표 사용
            pose_stamped_msg.pose.position.z = 0.0  # Assuming flat ground
            # Set orientation to default (identity quaternion)
            pose_stamped_msg.pose.orientation.x = 0.0
            pose_stamped_msg.pose.orientation.y = 0.0
            pose_stamped_msg.pose.orientation.z = 0.0
            pose_stamped_msg.pose.orientation.w = 1.0

            # Publish to the appropriate robot's goal_pose topic
            if robot_id in self.goal_pose_publishers:
                self.goal_pose_publishers[robot_id].publish(pose_stamped_msg)
                self.get_logger().info(
                    f"Sent goal_pose to {robot_id}: position=({pose_stamped_msg.pose.position.x}, {pose_stamped_msg.pose.position.y}, {pose_stamped_msg.pose.position.z}), "
                    f"orientation=({pose_stamped_msg.pose.orientation.x}, {pose_stamped_msg.pose.orientation.y}, {pose_stamped_msg.pose.orientation.z}, {pose_stamped_msg.pose.orientation.w})"
                )
            else:
                self.get_logger().error(f"No goal_pose publisher found for {robot_id}")
                return

            # Update robot_positions after movement
            self.robot_positions[robot_id] = (
                float(transformed_x),
                float(transformed_y),
            )
            self.get_logger().info(
                f"{robot_id} updated position to: ({transformed_x}, {transformed_y})"
            )
            return

        # Check for pick_up message
        pick_up_match = re.match(pick_up_pattern, message)
        if pick_up_match:
            robot_num = pick_up_match.group(1)
            robot_id = f"robot{robot_num}"
            with self.status_lock:
                self.robot_status[robot_id] = "with_vehicle"
            self.get_logger().info(f"{robot_id} picked up a vehicle.")
            return

        # Check for pick_off message
        pick_off_match = re.match(pick_off_pattern, message)
        if pick_off_match:
            robot_num = pick_off_match.group(1)
            vehicle_num = pick_off_match.group(2)
            y = int(pick_off_match.group(3))
            x = int(pick_off_match.group(4))
            robot_id = f"robot{robot_num}"
            with self.status_lock:
                self.robot_status[robot_id] = "idle"
            self.get_logger().info(
                f"{robot_id} dropped off vehicle {vehicle_num} at grid ({y}, {x})."
            )

            # Get transformed coordinates from map_grid_transform
            if 0 <= y < len(self.map_grid_transform) and 0 <= x < len(
                self.map_grid_transform[y]
            ):
                transformed_x, transformed_y = self.map_grid_transform[y][x]  # (x, y)
                self.get_logger().info(
                    f"{robot_id} drop_off transformed position: ({transformed_x}, {transformed_y})"
                )
            else:
                self.get_logger().error(
                    f"Received invalid grid coordinates for pick_off: ({y}, {x})"
                )
                return

            # Create PoseStamped message
            pose_stamped_msg = PoseStamped()
            pose_stamped_msg.header.frame_id = "map"
            pose_stamped_msg.header.stamp = self.get_clock().now().to_msg()
            pose_stamped_msg.pose.position.x = float(transformed_x)  # 실제 x 좌표 사용
            pose_stamped_msg.pose.position.y = float(transformed_y)  # 실제 y 좌표 사용
            pose_stamped_msg.pose.position.z = 0.0  # Assuming flat ground
            # Set orientation to default drop_off orientation
            pose_stamped_msg.pose.orientation.x = 0.0
            pose_stamped_msg.pose.orientation.y = 0.0
            pose_stamped_msg.pose.orientation.z = 0.7071
            pose_stamped_msg.pose.orientation.w = 0.7071

            # Publish to the appropriate robot's goal_pose topic
            if robot_id in self.goal_pose_publishers:
                self.goal_pose_publishers[robot_id].publish(pose_stamped_msg)
                self.get_logger().info(
                    f"Sent drop_off goal_pose to {robot_id}: position=({pose_stamped_msg.pose.position.x}, {pose_stamped_msg.pose.position.y}, {pose_stamped_msg.pose.position.z}), "
                    f"orientation=({pose_stamped_msg.pose.orientation.x}, {pose_stamped_msg.pose.orientation.y}, {pose_stamped_msg.pose.orientation.z}, {pose_stamped_msg.pose.orientation.w})"
                )
            else:
                self.get_logger().error(f"No goal_pose publisher found for {robot_id}")
                return

            # Update robot_positions to drop_off position
            self.robot_positions[robot_id] = (
                float(transformed_x),
                float(transformed_y),
            )
            self.get_logger().info(
                f"{robot_id} updated position to: ({transformed_x}, {transformed_y})"
            )
            return

        # If message doesn't match any pattern
        self.get_logger().warning(f"Unrecognized message format: {message}")

    def process_vehicle_detected(self, message):
        """
        Process messages received on '/vehicle_detected' topic.
        Expected message format: "1234, 대기 지역에 차량이 진입하였습니다" or "1234, 차량이 나갑니다"
        """
        # Regex pattern to extract vehicle number and task
        pattern = r"(\d{4}),\s*(.+)"
        match = re.match(pattern, message)
        if match:
            vehicle_num = match.group(1)
            task = match.group(2).strip()

            self.get_logger().info(f"Vehicle Number: {vehicle_num}, Task: {task}")

            if "진입하였습니다" in task:
                nav_message = f"in {vehicle_num}"
                self.publish_nav_message(nav_message)
            elif "요청합니다" in task:
                nav_message = f"out {vehicle_num}"
                self.publish_nav_message(nav_message)
            else:
                self.get_logger().warning(f"Unknown task in message: {task}")
        else:
            self.get_logger().warning(f"Message format incorrect: {message}")

    def publish_nav_message(self, message):
        """Publish a message to the 'nav_message' topic."""
        msg = String()
        msg.data = message
        self.publisher.publish(msg)
        self.get_logger().info(f"Published to 'nav_message': {message}")

    def calculate_distance_and_angle(self, current_pos, target_pos):
        """
        Calculate the Euclidean distance and angle between current_pos and target_pos.
        current_pos and target_pos are tuples of (x, y).
        Returns distance in meters and angle in radians.
        """
        dx = target_pos[0] - current_pos[0]
        dy = target_pos[1] - current_pos[1]
        distance = math.hypot(dx, dy)
        angle = math.atan2(dy, dx)
        return distance, angle

    def euler_to_quaternion(self, roll, pitch, yaw):
        """
        Convert Euler angles to quaternion.
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


# Entry point of the node
def main(args=None):
    rclpy.init(args=args)
    node = NavMessagePublisherNode()

    try:
        node.run()
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down NavMessagePublisherNode.")
    finally:
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
