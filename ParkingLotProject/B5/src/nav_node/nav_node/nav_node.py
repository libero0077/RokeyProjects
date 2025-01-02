# ~/ros2_ws/src/parking_robot/parking_robot/parking_node.py

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import matplotlib.pyplot as plt
import heapq
import random


class ParkingRobotNode(Node):
    def __init__(self):
        super().__init__("parking_robot_node")

        # Subscriber to 'nav_message' topic
        self.subscription = self.create_subscription(
            String, "nav_message", self.nav_message_callback, 10
        )
        self.subscription  # prevent unused variable warning

        # Publisher to 'nav_callback' topic
        self.nav_callback_publisher = self.create_publisher(String, "nav_callback", 10)

        # Initialize variables
        self.tick = 0
        self.robot_count = 2  # Number of robots
        self.task_list = []  # Task list
        self.filled_parking_slots = [(1, 4, "0000"), (1, 5, "0000"), (1, 8, "0000"), (1, 9, "0000"), (1, 10, "0000"), (1, 12, "0000"), (1, 13, "0000"), (3, 4, "0000"), (3, 9, "0000"), (3, 12, "0000"), (3, 14, "0000"), (4, 2, "0000"), (4, 4, "0000"), (4, 5, "0000"), (4, 7, "0000"), 
(4, 12, "0000"), (4, 13, "0000"), (6, 3, "0000"), (6, 8, "0000"), (6, 13, "0000"), (7, 4, "0000"), (7, 5, "0000"), (7, 8, "0000"), (7, 9, "0000"), (9, 1, "0000"), (9, 2, "0000"), (9, 4, "0000"), (9, 8, "0000"), (9, 12, "0000"), (9, 13, "0000")]  # Parked vehicles

        # Initialize robots
        self.robots = self.initialize_robots(self.robot_count)

        # Define grid map
        self.grid_map = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1],
            [1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1, 1],
            [1, 3, 2, 2, 2, 2, 3, 2, 2, 2, 2, 3, 2, 2, 2, 2, 4, 7, 1],
            [1, 3, 2, 2, 2, 2, 3, 2, 2, 2, 2, 3, 2, 2, 2, 2, 4, 1, 1],
            [1, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 4, 1, 1],
            [1, 3, 2, 2, 2, 2, 3, 2, 2, 2, 2, 3, 2, 2, 2, 2, 4, 1, 1],
            [1, 3, 2, 2, 2, 2, 3, 2, 2, 2, 2, 3, 2, 2, 2, 2, 4, 8, 1],
            [1, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 1, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]

        # Reservation table
        self.reservation_table = {}

        # Initialize visualization
        plt.ion()
        self.fig, self.ax = plt.subplots(figsize=(10, 6))

        # Log that the node is ready
        self.get_logger().info(
            "ParkingRobotNode has started. Awaiting 'tick' commands."
        )

    def nav_message_callback(self, msg):
        """
        Callback function for the 'nav_message' topic.
        Executes the main loop if the received message is 'tick'.
        Otherwise, handles 'in' and 'out' tasks.
        """
        command = msg.data.strip()
        if command == "tick":
            self.get_logger().info("Received 'tick' command. Executing main loop.")
            self.main_loop()
        elif command.startswith("in ") or command.startswith("out "):
            self.task_list.append(command)
            self.get_logger().info(f"Received task: {command}")
        else:
            self.get_logger().warning(f"Invalid command received: {command}")

    def initialize_robots(self, robot_count):
        robots = []
        start_positions = [(3, 17), (7, 17)]  # Starting positions for robots
        for i in range(robot_count):
            robots.append(
                {
                    "status": "idle",  # "idle", "with_vehicle", "without_vehicle"
                    "current_position": start_positions[i],
                    "goal_position": None,
                    "current_path": [],
                    "number": None,
                    "movement_count": 0,
                    "initial_index": i,
                    "vehicle_position": None,  # To store vehicle position during pick_off
                }
            )
        return robots

    def visualize_state(self):
        """Visualizes the current state using matplotlib."""
        self.ax.clear()

        for y, row in enumerate(self.grid_map):
            for x, cell in enumerate(row):
                color = "white"
                if cell == 1:
                    color = "black"  # Wall
                elif cell == 2 or cell == 10:
                    color = "gray"  # Parking spot
                elif cell == 3:
                    color = "lightblue"  # Down one-way
                elif cell == 4:
                    color = "skyblue"  # Up one-way
                elif cell == 5:
                    color = "blue"  # Left one-way
                elif cell == 6:
                    color = "navy"  # Right one-way
                elif cell == 7:
                    color = "lime"  # In position
                elif cell == 8:
                    color = "darkorange"  # Out position
                self.ax.add_patch(plt.Rectangle((x, y), 1, 1, color=color))

        # Display robots and their goals
        robot_colors = ["red", "purple", "cyan", "magenta"]
        for i, robot in enumerate(self.robots):
            # Current position
            self.ax.add_patch(
                plt.Circle(
                    (
                        robot["current_position"][1] + 0.5,
                        robot["current_position"][0] + 0.5,
                    ),
                    0.4,
                    label=f"Robot {i + 1}",
                    color=robot_colors[i % len(robot_colors)],
                )
            )

            # Path
            if robot["current_path"]:
                filtered_path = [
                    pos for pos in robot["current_path"] if isinstance(pos, tuple)
                ]
                path_x = [pos[1] + 0.5 for pos in filtered_path]
                path_y = [pos[0] + 0.5 for pos in filtered_path]
                self.ax.plot(
                    path_x,
                    path_y,
                    linestyle="--",
                    linewidth=2,
                    color=robot_colors[i % len(robot_colors)],
                    alpha=0.7,
                    label=(
                        f"Path {i + 1}"
                        if f"Path {i + 1}" not in self.ax.get_legend_handles_labels()[1]
                        else None
                    ),
                )

            # Goal position
            if robot["goal_position"]:
                self.ax.add_patch(
                    plt.Circle(
                        (
                            robot["goal_position"][1] + 0.5,
                            robot["goal_position"][0] + 0.5,
                        ),
                        0.2,
                        alpha=0.5,
                        color=robot_colors[i % len(robot_colors)],
                    )
                )

        # Display parked vehicles
        for slot in self.filled_parking_slots:
            y, x, _ = slot
            self.ax.add_patch(
                plt.Circle(
                    (x + 0.5, y + 0.5),
                    0.2,
                    color="yellow",
                    alpha=0.8,
                    label=(
                        "Parked Vehicle"
                        if "Parked Vehicle"
                        not in self.ax.get_legend_handles_labels()[1]
                        else None
                    ),
                )
            )

        self.ax.set_xlim(0, len(self.grid_map[0]))
        self.ax.set_ylim(0, len(self.grid_map))
        self.ax.set_aspect("equal")
        self.ax.invert_yaxis()
        plt.xticks(range(len(self.grid_map[0])))
        plt.yticks(range(len(self.grid_map)))
        self.ax.legend(loc="upper left")
        plt.grid(color="black", linewidth=0.5)

        # Check for robots at the same position
        positions = [robot["current_position"] for robot in self.robots]
        if len(positions) != len(set(map(tuple, positions))):
            self.get_logger().warn(
                "Robots are at the same position! Check visualization."
            )
            plt.show(block=False)
        else:
            plt.pause(0.15)
            self.ax.cla()

    def assign_tasks(self):
        """Assigns tasks from the task list to robots."""
        if not self.task_list:
            self.get_logger().info("No tasks to assign.")
            return

        in_robot = self.robots[0]  # First robot for 'in' tasks
        out_robot = self.robots[1]  # Second robot for 'out' tasks

        for task in self.task_list[:]:
            task_type, number = task.split()
            if task_type == "in" and in_robot["status"] == "idle":
                in_robot["goal_position"] = (3, 17)  # Pickup location for 'in' tasks
                in_robot["status"] = "moving_to_pickup"
                in_robot["number"] = number
                self.task_list.remove(task)
                self.get_logger().info(
                    f"Assigned 'in' task: Robot 1 -> Vehicle {number}"
                )
            elif task_type == "out" and out_robot["status"] == "idle":
                # Find the vehicle in parking slots
                goal_info = next(
                    (slot for slot in self.filled_parking_slots if slot[2] == number),
                    None,
                )
                if goal_info:
                    out_robot["goal_position"] = (goal_info[0], goal_info[1])
                    out_robot["status"] = "moving_to_vehicle"
                    out_robot["number"] = number
                    self.task_list.remove(task)
                    self.get_logger().info(
                        f"Assigned 'out' task: Robot 2 -> Vehicle {number}"
                    )
                else:
                    self.get_logger().warning(
                        f"Failed to assign 'out' task: Vehicle {number} not parked."
                    )
                    self.task_list.remove(task)

    def execute_next_command(self, robot):
        """Executes the next command in the robot's path."""
        if not robot["current_path"]:
            self.get_logger().info(
                f"Robot {self.robots.index(robot) + 1}: No commands to execute."
            )
            return

        if self.will_collide_extended(robot, steps_ahead=2):
            self.get_logger().warning(
                f"Robot {self.robots.index(robot) + 1} collision predicted. Waiting."
            )
            robot["current_path"].insert(0, robot["current_position"])
            robot["waiting"] = True
            return

        next_command = robot["current_path"].pop(0)

        if isinstance(next_command, tuple):
            self.get_logger().info(
                f"Robot {self.robots.index(robot)+1} moving to {next_command}. Movement count: {robot['movement_count'] + 1}"
            )
            robot["current_position"] = next_command
            robot["movement_count"] += 1
        elif next_command == "pick_up":
            self.get_logger().info(
                f"Robot {self.robots.index(robot)+1} picking up vehicle {robot['number']}."
            )
            robot["goal_position"] = (99, 99)  # Reset goal position

            if robot["status"] == "moving_to_dropoff":
                vehicle_number = robot["number"]
                vehicle_slot = next(
                    (
                        slot
                        for slot in self.filled_parking_slots
                        if slot[2] == vehicle_number
                    ),
                    None,
                )
                if vehicle_slot:
                    y, x, number = vehicle_slot
                    robot["vehicle_position"] = (y, x)
                    self.filled_parking_slots.remove(vehicle_slot)
                    self.get_logger().info(
                        f"Robot {self.robots.index(robot)+1}: Vehicle {vehicle_number} removed from parking."
                    )
                else:
                    robot["vehicle_position"] = (None, None)
                    self.get_logger().warning(
                        f"Robot {self.robots.index(robot)+1}: Vehicle {vehicle_number} not found in parking slots."
                    )

            robot["movement_count"] = 0
        elif next_command == "pick_off":
            self.get_logger().info(f"Robot {self.robots.index(robot)+1} dropping off.")
            # Store vehicle number and position before removing
            vehicle_number = robot["number"]
            vehicle_slot = next(
                (
                    slot
                    for slot in self.filled_parking_slots
                    if slot[2] == vehicle_number
                ),
                None,
            )
            if vehicle_slot:
                y, x, number = vehicle_slot
                robot["vehicle_position"] = (y, x)
            else:
                robot["vehicle_position"] = (None, None)
                self.get_logger().warning(
                    f"Robot {self.robots.index(robot)+1}: Vehicle {vehicle_number} not found in parking slots."
                )
            robot["movement_count"] = 0
        else:
            self.get_logger().info(
                f"Robot {self.robots.index(robot)+1} executing command: {next_command}"
            )

        if "waiting" in robot:
            self.get_logger().info(
                f"Robot {self.robots.index(robot) + 1} is no longer waiting."
            )
            del robot["waiting"]

    def will_collide_extended(self, robot, steps_ahead=2):
        """Checks if the robot will collide in the next few steps."""
        future_positions = robot["current_path"][:steps_ahead]
        for other in self.robots:
            if other is robot:
                continue
            for future_pos in future_positions:
                if self.is_conflict(future_pos, other):
                    return True
        return False

    def is_conflict(self, pos, other_robot):
        """Determines if there's a conflict with another robot at the given position."""
        if other_robot["current_path"]:
            other_next = other_robot["current_path"][0]
            if isinstance(other_next, tuple) and other_next == pos:
                return True
        if other_robot["current_position"] == pos:
            return True
        return False

    def check_and_reserve_paths(self):
        """Checks for collisions and updates reservation table."""
        self.reservation_table.clear()
        max_path_length = max(len(robot["current_path"]) for robot in self.robots)

        for tick in range(max_path_length):
            positions_at_tick = []
            for robot in self.robots:
                if robot["status"] in [
                    "idle",
                    "moving_to_home",
                    "moving_to_parking_spot",
                ]:
                    positions_at_tick.append(None)
                    continue

                if tick < len(robot["current_path"]):
                    pos = robot["current_path"][tick]
                    if isinstance(pos, tuple):
                        positions_at_tick.append(pos)
                    else:
                        positions_at_tick.append(robot["current_position"])
                else:
                    pos = (
                        robot["current_path"][-1]
                        if robot["current_path"]
                        else robot["current_position"]
                    )
                    if isinstance(pos, tuple):
                        positions_at_tick.append(pos)
                    else:
                        positions_at_tick.append(robot["current_position"])

            # Reserve positions
            for i, pos in enumerate(positions_at_tick):
                if pos is None:
                    continue
                if tick not in self.reservation_table:
                    self.reservation_table[tick] = set()
                self.reservation_table[tick].add(pos)

            # Check for collisions
            active_robot_indices = [
                i for i, pos in enumerate(positions_at_tick) if pos is not None
            ]
            for idx1 in range(len(active_robot_indices)):
                for idx2 in range(idx1 + 1, len(active_robot_indices)):
                    i = active_robot_indices[idx1]
                    j = active_robot_indices[idx2]
                    pos1 = positions_at_tick[i]
                    pos2 = positions_at_tick[j]
                    if self.manhattan_distance(pos1, pos2) <= 1:
                        robot_i = self.robots[i]
                        robot_j = self.robots[j]

                        # Determine priority based on movement_count and initial_index
                        if robot_i["movement_count"] > robot_j["movement_count"]:
                            higher_priority_robot = robot_i
                            lower_priority_robot = robot_j
                        elif robot_i["movement_count"] < robot_j["movement_count"]:
                            higher_priority_robot = robot_j
                            lower_priority_robot = robot_i
                        else:
                            if robot_i["initial_index"] < robot_j["initial_index"]:
                                higher_priority_robot = robot_i
                                lower_priority_robot = robot_j
                            else:
                                higher_priority_robot = robot_j
                                lower_priority_robot = robot_i

                        if "waiting" not in lower_priority_robot:
                            if len(lower_priority_robot["current_path"]) > tick:
                                if tick > 0:
                                    wait_position = lower_priority_robot[
                                        "current_path"
                                    ][tick - 1]
                                    if not isinstance(wait_position, tuple):
                                        wait_position = lower_priority_robot[
                                            "current_position"
                                        ]
                                else:
                                    wait_position = lower_priority_robot[
                                        "current_position"
                                    ]
                                lower_priority_robot["current_path"].insert(
                                    tick, wait_position
                                )
                                lower_priority_robot["waiting"] = True
                                self.get_logger().warn(
                                    f"Collision detected between Robot {i+1} and Robot {j+1} at tick {tick}. "
                                    f"Robot {self.robots.index(lower_priority_robot)+1} will wait."
                                )
                        else:
                            self.get_logger().info(
                                f"Robot {self.robots.index(lower_priority_robot)+1} is already waiting."
                            )

    def main_loop(self):
        """Main loop executed only when a 'tick' command is received."""
        self.get_logger().info(f"\nTick: {self.tick}")
        self.tick += 1

        # Assign tasks
        self.assign_tasks()

        # Execute commands for each robot
        for robot in self.robots:
            self.execute_next_command(robot)

        # Process paths and handle collisions
        self.process_robot_paths()

        # Visualize the current state
        self.visualize_state()

        # Log robot states
        for i, robot in enumerate(self.robots):
            self.get_logger().info(f"Robot {i+1}: {robot}")

        # Publish current_path information to 'nav_callback' topic
        for i, robot in enumerate(self.robots):
            robot_number = i + 1
            if robot["current_path"]:
                first_cmd = robot["current_path"][0]
                if isinstance(first_cmd, tuple):
                    message = f"robot{robot_number} {first_cmd}"
                elif first_cmd == "pick_up":
                    message = f"robot{robot_number} pick_up"
                elif first_cmd == "pick_off":
                    if robot["current_position"]:
                        y, x = robot["current_position"]
                        message = (
                            f"robot{robot_number} pick_off {robot['number']} ({y},{x})"
                        )
                    else:
                        message = f"robot{robot_number} pick_off"
                else:
                    message = f"robot{robot_number} {first_cmd}"
            else:
                message = f"robot{robot_number} idle"

            # Publish the message
            msg = String()
            msg.data = message
            self.nav_callback_publisher.publish(msg)
            self.get_logger().info(f"Published to 'nav_callback': {message}")

    def process_robot_paths(self):
        """Generates and verifies paths for all robots."""
        for robot in self.robots:
            if not robot["current_path"]:
                self.generate_path(robot)

        self.check_and_reserve_paths()

    def generate_path(self, robot):
        """Generates a path for the given robot based on its current status."""
        robot_index = self.robots.index(robot)

        if robot["status"] == "moving_to_pickup":
            if robot["goal_position"] == robot["current_position"]:
                self.get_logger().info(
                    f"Robot {robot_index + 1} arrived at pickup location."
                )
                robot["status"] = "moving_to_parking_spot"
                robot["current_path"] = ["pick_up"]
            else:
                self.get_logger().info(
                    f"Robot {robot_index + 1} moving to pickup location."
                )
                path = self.a_star(
                    self.grid_map, robot["current_position"], robot["goal_position"]
                )
                if path and len(path) > 1:
                    path = path[1:]
                    robot["current_path"] = path
                    self.get_logger().info(
                        f"Robot {robot_index + 1} path: {robot['current_path']}"
                    )
                else:
                    self.get_logger().error(
                        f"Robot {robot_index + 1} failed to generate path to pickup."
                    )

        elif robot["status"] == "moving_to_parking_spot":
            if robot["goal_position"] == robot["current_position"]:
                self.get_logger().info(
                    f"Robot {robot_index + 1} arrived at parking spot {robot['goal_position']}."
                )
                robot["status"] = "moving_to_home"
                robot["current_path"] = ["pick_off"]
            else:
                available_parking_slots = [
                    (y, x)
                    for y, row in enumerate(self.grid_map)
                    for x, cell in enumerate(row)
                    if cell == 2
                    and (y, x)
                    not in [(slot[0], slot[1]) for slot in self.filled_parking_slots]
                ]
                if not available_parking_slots:
                    self.get_logger().warning(
                        f"Robot {robot_index + 1}: No available parking slots."
                    )
                    return

                robot["goal_position"] = random.choice(available_parking_slots)
                self.get_logger().info(
                    f"Robot {robot_index + 1} moving to parking spot {robot['goal_position']}."
                )
                path = self.a_star(
                    self.grid_map, robot["current_position"], robot["goal_position"]
                )
                if path and len(path) > 1:
                    path = path[1:]
                    robot["current_path"] = path
                    self.filled_parking_slots.append(
                        (*robot["goal_position"], robot["number"])
                    )
                    self.get_logger().info(
                        f"Robot {robot_index + 1} path: {robot['current_path']}"
                    )
                else:
                    self.get_logger().error(
                        f"Robot {robot_index + 1} failed to generate path to parking spot."
                    )

        elif robot["status"] == "moving_to_home":
            home_positions = [(3, 17), (7, 17)]
            robot_home_position = home_positions[robot_index % len(home_positions)]
            robot["goal_position"] = robot_home_position
            self.get_logger().info(
                f"Robot {robot_index + 1} moving to home position {robot_home_position}."
            )
            path = self.a_star(
                self.grid_map, robot["current_position"], robot_home_position
            )
            if path and len(path) > 1:
                path = path[1:]
                robot["status"] = "idle"
                robot["current_path"] = path
                self.get_logger().info(
                    f"Robot {robot_index + 1} path to home: {robot['current_path']}"
                )
            else:
                self.get_logger().error(
                    f"Robot {robot_index + 1} failed to generate path to home."
                )

        elif robot["status"] == "moving_to_vehicle":
            if robot["goal_position"] == robot["current_position"]:
                self.get_logger().info(
                    f"Robot {robot_index + 1} arrived at vehicle location."
                )
                robot["status"] = "moving_to_dropoff"
                robot["current_path"] = ["pick_up"]
            else:
                self.get_logger().info(
                    f"Robot {robot_index + 1} moving to vehicle location."
                )
                path = self.a_star(
                    self.grid_map, robot["current_position"], robot["goal_position"]
                )
                if path and len(path) > 1:
                    path = path[1:]
                    robot["current_path"] = path
                    self.get_logger().info(
                        f"Robot {robot_index + 1} path: {robot['current_path']}"
                    )
                else:
                    self.get_logger().error(
                        f"Robot {robot_index + 1} failed to generate path to vehicle."
                    )

        elif robot["status"] == "moving_to_dropoff":
            dropoff_position = (7, 17)  # Define dropoff position
            if robot["goal_position"] == robot["current_position"]:
                self.get_logger().info(
                    f"Robot {robot_index + 1} arrived at dropoff location."
                )
                robot["status"] = "idle"
                robot["current_path"] = ["pick_off"]
            else:
                robot["goal_position"] = dropoff_position
                self.get_logger().info(
                    f"Robot {robot_index + 1} moving to dropoff location {dropoff_position}."
                )
                path = self.a_star(
                    self.grid_map, robot["current_position"], dropoff_position
                )
                if path and len(path) > 1:
                    path = path[1:]
                    robot["current_path"] = path
                    self.get_logger().info(
                        f"Robot {robot_index + 1} path: {robot['current_path']}"
                    )
                else:
                    self.get_logger().error(
                        f"Robot {robot_index + 1} failed to generate path to dropoff."
                    )

    def a_star(self, grid, start, goal):
        """
        A* algorithm for pathfinding.

        :param grid: 2D grid map
        :param start: (y, x) tuple
        :param goal: (y, x) tuple
        :return: List of tuples representing the path
        """
        rows, cols = len(grid), len(grid[0])

        def is_accessible(current, neighbor):
            y, x = neighbor
            if grid[y][x] == 1:
                return False
            if grid[y][x] == 2 and neighbor != goal:
                return False
            return True

        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        def get_allowed_directions(current):
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            y, x = current
            grid_type = grid[y][x]

            if grid_type == 2:
                return [(-1, 0), (1, 0)]
            elif grid_type == 3:
                return [(1, 0)]
            elif grid_type == 4:
                return [(-1, 0), (0, 1)]
            elif grid_type == 5:
                return [(-1, 0), (1, 0), (0, -1)]
            elif grid_type == 6:
                return [(-1, 0), (1, 0), (0, 1)]
            else:
                return directions

        def get_neighbors(node):
            y, x = node
            allowed_dirs = get_allowed_directions(node)
            neighbors = []
            for dy, dx in allowed_dirs:
                ny, nx = y + dy, x + dx
                if 0 <= ny < rows and 0 <= nx < cols:
                    neighbors.append((ny, nx))
            return [n for n in neighbors if is_accessible(node, n)]

        def reconstruct_path(came_from, current):
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            return path[::-1]

        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}

        g_score = {start: 0}
        f_score = {start: heuristic(start, goal)}

        while open_set:
            _, current = heapq.heappop(open_set)

            if current == goal:
                return reconstruct_path(came_from, current)

            for neighbor in get_neighbors(current):
                tentative_g_score = g_score[current] + 1

                if tentative_g_score < g_score.get(neighbor, float("inf")):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)

                    if neighbor not in [item[1] for item in open_set]:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return None

    def manhattan_distance(self, pos1, pos2):
        """Calculates Manhattan distance between two positions."""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def main(args=None):
    rclpy.init(args=args)
    parking_robot_node = ParkingRobotNode()
    try:
        rclpy.spin(parking_robot_node)
    except KeyboardInterrupt:
        pass
    finally:
        parking_robot_node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
