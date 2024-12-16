#!/usr/bin/env python3
import math
import json
import time
from typing import List, Dict, Any, Tuple

import cv2
import numpy as np
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.qos import QoSProfile
from rclpy.executors import MultiThreadedExecutor

from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from std_msgs.msg import Header, String
from sensor_msgs.msg import JointState
from control_msgs.action import GripperCommand

import threading

# 로봇 매니퓰레이터 파라미터
R1 = 130
R2 = 124
R3 = 126

TH1_OFFSET = - math.atan2(0.024, 0.128)
TH2_OFFSET = - 0.5 * math.pi - TH1_OFFSET

JOINT_NAMES = ['joint1', 'joint2', 'joint3', 'joint4']
WAIT_TIME = 2.0  # 각 동작 후 대기 시간(초)

GRIPPER_OPEN = 0.02
GRIPPER_CLOSE = -0.02

# 카메라 기준 오프셋 (재계산된 값)
CAMERA_OFFSET_X = 120.0    # x축 오프셋
CAMERA_OFFSET_Y = 0.0      # y축 오프셋
CAMERA_OFFSET_Z = 0.0      # z축 오프셋 (필요 시 조정)

# 컨테이너 위치
CONTAINER_X = 0
CONTAINER_Y = -240
CONTAINER_Z = 78  # 놓는 위치 z 좌표

# 신뢰도 임계값 설정
CONFIDENCE_THRESHOLD = 0.5

class KalmanFilter:
    def __init__(self, process_variance, measurement_variance):
        self.process_variance = process_variance
        self.measurement_variance = measurement_variance
        self.posteri_estimate = 0.0
        self.posteri_error_estimate = 1.0

    def update(self, measurement):
        # Prediction Update
        priori_estimate = self.posteri_estimate
        priori_error_estimate = self.posteri_error_estimate + self.process_variance

        # Measurement Update
        blending_factor = priori_error_estimate / (priori_error_estimate + self.measurement_variance)
        self.posteri_estimate = priori_estimate + blending_factor * (measurement - priori_estimate)
        self.posteri_error_estimate = (1 - blending_factor) * priori_error_estimate

        return self.posteri_estimate

def solv2(r1, r2, r3):
    d1 = (r3**2 - r2**2 + r1**2) / (2*r3)
    d2 = (r3**2 + r2**2 - r1**2) / (2*r3)

    # 클램핑을 통해 acos의 인자 범위를 [-1, 1]로 제한
    d1_over_r1 = max(min(d1 / r1, 1.0), -1.0)
    d2_over_r2 = max(min(d2 / r2, 1.0), -1.0)

    try:
        s1 = math.acos(d1_over_r1)
        s2 = math.acos(d2_over_r2)
    except ValueError as e:
        # 각도가 유효하지 않을 경우 경고 로그
        print(f"Warning: Invalid angles calculated. d1/r1: {d1_over_r1}, d2/r2: {d2_over_r2}")
        raise e

    return s1, s2

def solv_robot_arm2(x, y, z, r1, r2, r3):
    Rt = math.sqrt(x**2 + y**2 + z**2)
    if Rt == 0:
        Rt = 1e-6  # Avoid division by zero
    Rxy = math.sqrt(x**2 + y**2)
    St = math.asin(z / Rt)
    Sxy = math.atan2(y, x)

    s1, s2 = solv2(r1, r2, Rt)

    sr1 = math.pi/2 - (s1 + St)
    sr2 = s1 + s2
    sr3 = math.pi - (sr1 + sr2)

    J0 = (0, 0, 0)
    J1 = (R1 * math.sin(sr1) * math.cos(Sxy),
          R1 * math.sin(sr1) * math.sin(Sxy),
          R1 * math.cos(sr1))
    J2 = (J1[0] + R2 * math.sin(sr1 + sr2) * math.cos(Sxy),
          J1[1] + R2 * math.sin(sr1 + sr2) * math.sin(Sxy),
          J1[2] + R2 * math.cos(sr1 + sr2))
    J3 = (J2[0] + R3 * math.sin(sr1 + sr2 + sr3) * math.cos(Sxy),
          J2[1] + R3 * math.sin(sr1 + sr2 + sr3) * math.sin(Sxy),
          J2[2] + R3 * math.cos(sr1 + sr2 + sr3))

    return J0, J1, J2, J3, Sxy, sr1, sr2, sr3, St, Rt

class TaskManager:
    def __init__(self, node):
        self.node = node
        self.task_queue = []
        self.processing = False
        self.lock = threading.Lock()

    def add_task(self, task_dict):
        with self.lock:
            self.task_queue.append(task_dict)
            self.node.get_logger().info(f"Task added: {task_dict}")
        if not self.processing:
            threading.Thread(target=self.process_tasks, daemon=True).start()

    def process_tasks(self):
        self.processing = True
        while True:
            with self.lock:
                if not self.task_queue:
                    self.processing = False
                    break
                task = self.task_queue.pop(0)
            self.node.get_logger().info(f"Processing task: {task}")
            try:
                self.node.reset_task_state()  # 태스크 상태 초기화
                self.execute_task(task)      # 새로운 태스크 실행
            except Exception as e:
                self.node.get_logger().error(f"Error executing task {task}: {e}")

    def execute_task(self, task):
        tasks = task.get('task', [])
        offset_xy = task.get('offset_xy', [0, 0])
        self.node.offset_xy = offset_xy

        for color in tasks:
            self.node.get_logger().info(f"Starting sub-task: Pick {color} box")

            # 필요한 박스 수 확인 및 대기
            required_boxes = tasks.count(color)
            self.node.get_logger().info(f"Required '{color}' boxes: {required_boxes}")

            while True:
                available_boxes = self.node.get_available_boxes_by_color(color)
                self.node.get_logger().info(f"Detected available_boxes: {available_boxes}")

                # 탐지된 박스 수가 필요한 박스 수 이상일 경우 루프 종료
                if len(available_boxes) >= required_boxes:
                    self.node.get_logger().info(f"Sufficient '{color}' boxes detected: {available_boxes}")
                    break

                self.node.get_logger().warning(f"No '{color}' boxes detected. Waiting...")
                time.sleep(2)  # 2초 대기 후 재시도

            # 가장 가까운 박스를 선택
            target_box = available_boxes[0]  # 리스트에서 첫 번째 박스 가져오기
            self.node.get_logger().info(f"Selected box: {target_box}")

            # 박스 중심 좌표 계산
            cx = target_box['center_x']
            cy = target_box['center_y']

            self.node.get_logger().info(f"Original box center: cx={cx}, cy={cy}")

            # 바운딩 박스 중심 보정 및 필터링
            undistorted_points = cv2.undistortPoints(
                np.array([[[cx, cy]]], dtype=np.float32),
                self.node.mtx,
                self.node.dist,
                P=self.node.mtx
            )
            corrected_cx, corrected_cy = undistorted_points[0][0]
            filtered_cx = self.node.kalman_filter_x.update(corrected_cx)
            filtered_cy = self.node.kalman_filter_y.update(corrected_cy)

            self.node.get_logger().info(f"Filtered target center: cx={filtered_cx}, cy={filtered_cy}")

            # 프레임 중심과의 차이 계산
            dx = (self.node.frame_center_x - filtered_cx) / 3
            dy = (self.node.frame_center_y - filtered_cy) / 3

            self.node.get_logger().info(f"Difference from frame center: dx={dx}, dy={dy}")

            # 현재 로봇의 위치 가져오기
            current_x, current_y, current_z = self.node.current_xyz
            self.node.get_logger().info(f"Current XYZ: x={current_x}, y={current_y}, z={current_z}")

            # 목표 위치 계산
            target_x = current_x + dy + CAMERA_OFFSET_X + self.node.offset_xy[0]
            target_y = current_y + dx + CAMERA_OFFSET_Y + self.node.offset_xy[1]
            target_z = CAMERA_OFFSET_Z

            self.node.get_logger().info(f"Calculated target position: x={target_x}, y={target_y}, z={target_z}")

            # 로봇을 목표 위치로 이동
            self.node.move_arm(target_x, target_y, 40)

            time.sleep(2)

            # 그리퍼 닫기
            self.node.control_gripper(GRIPPER_CLOSE)

            # 로봇을 들어올리기 (z=150)
            self.node.move_arm(target_x, target_y, 150)

            # 컨테이너 위치로 이동
            self.node.move_arm(CONTAINER_X, CONTAINER_Y, CONTAINER_Z)

            # 그리퍼 열기
            self.node.control_gripper(GRIPPER_OPEN, wait=False)

            self.node.get_logger().info(f"Completed sub-task: Pick {color} box")

            # 선택한 박스를 피킹 상태로 업데이트
            target_box['picked'] = True

            # 초기 위치로 복귀
            self.node.move_arm(70, 0, 210)

            # 컨베이어에 놓았음을 알리는 메시지 전송
            self.node.send_conveyor_command("start:1000")

            # 초기화
            self.node.reset_task_state()
            self.node.get_logger().info("Resetting detected boxes and task state.")

        # 태스크 완료 메시지
        self.node.get_logger().info(f"All tasks completed: {tasks}")

        # 컨베이어에 놓았음을 알리는 메시지 전송
        self.node.send_conveyor_command("start:10000")

class Turtlebot3ManipulationTest(Node):
    def __init__(self):
        super().__init__('turtlebot3_manipulation_test')

        # QoS 프로필 복원: 기본 설정 사용
        qos_profile = QoSProfile(depth=10)

        # 퍼블리셔, 액션 클라이언트, 서브스크립션 설정
        self.joint_pub = self.create_publisher(JointTrajectory, '/arm_controller/joint_trajectory', qos_profile)
        self.gripper_action_client = ActionClient(
            self, GripperCommand, 'gripper_controller/gripper_cmd', callback_group=None
        )
        self.joint_subscription = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_state_callback,
            qos_profile
        )

        self.conveyor_publisher = self.create_publisher(String, 'conveyor_command', qos_profile)

        # YOLO 탐지 구독
        self.detection_subscription = self.create_subscription(
            String,
            'usb_camera/detections',
            self.detection_callback,
            qos_profile
        )

        # 태스크 명령 구독
        self.task_subscription = self.create_subscription(
            String,
            'task_commands',
            self.task_callback,
            qos_profile
        )

        # 초기화 변수
        self.current_gripper = GRIPPER_OPEN
        self.current_angles = [0.0, 0.0, 0.0, 0.0]
        self.current_xyz = [0.0, 0.0, 0.0]
        self.target_box = None

        # 프레임 중심 좌표 설정 (이미지 해상도에 기반)
        self.frame_width = 640
        self.frame_height = 480
        self.frame_center_x = self.frame_width / 2
        self.frame_center_y = self.frame_height / 2

        # 캘리브레이션 보정 값
        self.mtx = np.array([[922.71090711, 0.0, 333.59917498],
                             [0.0, 922.47035275, 245.09738171],
                             [0.0, 0.0, 1.0]])

        self.dist = np.array([[ 0.11328408, -0.17540197, -0.0043151, -0.00195606, 0.26917646]])

        # 추가: 박스 만료 시간 (초 단위)
        self.box_expiration_time = 5.0  # 2초 동안 감지되지 않으면 제거
        self.last_frame_time = time.time()

        # 탐지된 박스 및 타임스탬프 초기화
        self.detected_boxes = {}       # label_id -> box 정보
        self.box_timestamps = {}       # label_id -> timestamp
        self.detected_boxes_lock = threading.Lock()  # 락 초기화
        
        # 조인트 상태 초기화
        if not self.wait_for_joint_update():
            self.get_logger().error("Failed to initialize joint states. Using default angles.")
            self.current_angles = [0.0, 0.0, 0.0, 0.0]

        self.get_logger().info(f"Initial joint states: {self.current_angles}")

        # 초기 위치 (70,0,210)으로 이동 후 그리퍼 오픈
        self.move_arm(70, 0, 210)
        self.control_gripper(GRIPPER_OPEN)

        # 칼만 필터 초기화
        self.kalman_filter_x = KalmanFilter(process_variance=1e-4, measurement_variance=1e-2)
        self.kalman_filter_y = KalmanFilter(process_variance=1e-4, measurement_variance=1e-2)

        # 태스크 매니저 초기화
        self.task_manager = TaskManager(self)
        self.offset_xy = [0, 0]

        # 추가: 카메라 이미지 구독 및 시각화
        self.image_subscription = self.create_subscription(
            # 실제 카메라 이미지 토픽과 메시지 타입으로 변경 필요
            # 예: sensor_msgs.msg.Image
            # 현재는 예시로 std_msgs/String을 사용
            String,
            'usb_camera/image',
            self.image_callback,
            qos_profile
        )

    def reset_task_state(self):
        """Reset the robot state before starting a new task."""
        self.offset_xy = [0, 0]   # 오프셋 초기화
        # 현재 위치를 유지하며 초기화를 최소화
        self.get_logger().info("Task state reset: Keeping current XYZ and detected boxes.")

    def wait_for_joint_update(self, timeout=5.0):
        start_time = time.time()
        while time.time() - start_time < timeout:
            rclpy.spin_once(self, timeout_sec=0.1)
            if self.current_angles != [0.0, 0.0, 0.0, 0.0]:
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
            self.refresh_current_xyz()
            self.get_logger().debug(f"Updated joint angles: {self.current_angles}")
        except KeyError as e:
            self.get_logger().warning(f"Missing joint data: {e}")

    def detection_callback(self, msg):
        """YOLO 탐지 결과를 처리."""
        try:
            detections = json.loads(msg.data)
            self.get_logger().info(f"YOLO Detections raw data: {msg.data}")

            current_time = time.time()
            new_detected_boxes = {}
            new_timestamps = {}

            for det in detections:
                if det["confidence"] < CONFIDENCE_THRESHOLD:
                    self.get_logger().info(f"Detection with low confidence ({det['confidence']}) ignored.")
                    continue

                color = det["label"].lower()
                bbox = det["bbox"]
                center_x = (bbox[0] + bbox[2]) / 2
                center_y = (bbox[1] + bbox[3]) / 2
                box_id = f"{color}_{int(center_x)}_{int(center_y)}"

                new_detected_boxes[box_id] = {
                    'color': color,
                    'bbox': bbox,
                    'center_x': center_x,
                    'center_y': center_y,
                    'confidence': det["confidence"],
                    'picked': False,
                }
                new_timestamps[box_id] = current_time

            with self.detected_boxes_lock:
                # 만료된 박스 제거
                self.detected_boxes = {
                    box_id: box
                    for box_id, box in self.detected_boxes.items()
                    if (current_time - self.box_timestamps.get(box_id, 0)) < self.box_expiration_time
                }
                # 새로 탐지된 박스 추가
                self.detected_boxes.update(new_detected_boxes)
                self.box_timestamps.update(new_timestamps)

            self.get_logger().info(f"Updated detected_boxes: {self.detected_boxes}")

        except json.JSONDecodeError as e:
            self.get_logger().error(f"Failed to parse YOLO detection: {e}")

    def get_available_boxes_by_color(self, color):
        """Return available boxes of a specific color."""
        current_time = time.time()
        with self.detected_boxes_lock:
            self.get_logger().info(f"All detected_boxes: {self.detected_boxes}")
            available_boxes = []
            for box_id, box in self.detected_boxes.items():
                picked_status = box['picked']
                expiration_status = (current_time - self.box_timestamps.get(box_id, 0)) < self.box_expiration_time
                color_match = box['color'] == color

                # 디버깅 로그: 각 조건 확인
                self.get_logger().info(
                    f"Box ID: {box_id} | Picked: {picked_status}, Expired: {not expiration_status}, "
                    f"Color Match: {color_match} | Box: {box}"
                )

                if color_match and not picked_status and expiration_status:
                    available_boxes.append(box)

            self.get_logger().info(f"Filtered available_boxes for '{color}': {available_boxes}")
            return available_boxes

        
    def mark_box_as_picked(self, box):
        """Mark a specific box as picked."""
        with self.detected_boxes_lock:
            box["picked"] = True
            self.get_logger().info(f"Marked box as picked: {box}")

    def task_callback(self, msg):
        """태스크 명령을 수신하고 TaskManager에 추가."""
        try:
            task_dict = json.loads(msg.data)
            self.get_logger().info(f"Received task: {task_dict}")
            self.task_manager.add_task(task_dict)
        except json.JSONDecodeError as e:
            self.get_logger().error(f"Failed to parse task command: {e}")

    def mark_box_as_picked(self, label_id):
        """특정 박스를 피킹 완료된 상태로 표시."""
        with self.detected_boxes_lock:
            if label_id in self.detected_boxes:
                self.detected_boxes[label_id]['picked'] = True
                self.get_logger().info(f"Box with label_id '{label_id}' marked as picked.")

    def update_status(self):
        self.refresh_current_xyz()
        self.log_current_status()

    def refresh_current_xyz(self):
        J0, J1, J2, J3 = self.forward_kinematics_all(self.current_angles)
        self.current_xyz = list(J3)

    def log_current_status(self):
        angles = self.current_angles
        J0, J1, J2, J3 = self.forward_kinematics_all(angles)
        self.get_logger().info(f"Current joint angles: {angles}")
        self.get_logger().info(f"Forward Kinematics J2: {J2}, EE XYZ: {J3}")
        self.get_logger().info(f"Current XYZ: {self.current_xyz}")

    def forward_kinematics_all(self, angles):
        Sxy = angles[0]
        sr1 = angles[1] - TH1_OFFSET
        sr2 = angles[2] - TH2_OFFSET
        sr3 = angles[3]

        J0 = (0, 0, 0)
        J1 = (R1 * math.sin(sr1) * math.cos(Sxy),
              R1 * math.sin(sr1) * math.sin(Sxy),
              R1 * math.cos(sr1))
        J2 = (J1[0] + R2 * math.sin(sr1 + sr2) * math.cos(Sxy),
              J1[1] + R2 * math.sin(sr1 + sr2) * math.sin(Sxy),
              J1[2] + R2 * math.cos(sr1 + sr2))
        J3 = (J2[0] + R3 * math.sin(sr1 + sr2 + sr3) * math.cos(Sxy),
              J2[1] + R3 * math.sin(sr1 + sr2 + sr3) * math.sin(Sxy),
              J2[2] + R3 * math.cos(sr1 + sr2 + sr3))

        return J0, J1, J2, J3

    def move_arm(self, x, y, z):
        """Move the robot arm to the specified (x, y, z) position."""
        try:
            J0, J1, J2, J3, Sxy, sr1, sr2, sr3, St, Rt = solv_robot_arm2(x, y, z, R1, R2, R3)
            target_angles = [
                Sxy,
                sr1 + TH1_OFFSET,
                sr2 + TH2_OFFSET,
                sr3
            ]

            # Move command log 추가
            self.get_logger().info(f"Moving arm to target position: x={x}, y={y}, z={z}, with target angles: {target_angles}")

            msg = JointTrajectory(
                header=Header(frame_id=''),
                joint_names=JOINT_NAMES,
                points=[
                    JointTrajectoryPoint(
                        positions=target_angles,
                        velocities=[0.0]*4,
                        time_from_start=rclpy.duration.Duration(seconds=WAIT_TIME).to_msg(),
                    )
                ],
            )
            self.joint_pub.publish(msg)

            # 명령 완료 확인
            start_time = time.time()
            while time.time() - start_time < WAIT_TIME:
                rclpy.spin_once(self, timeout_sec=0.1)
            self.update_status()

        except Exception as e:
            self.get_logger().error(f"Failed to move arm: {e}")

    def send_conveyor_command(self, command):
        """Send a command to the conveyor."""
        msg = String()
        msg.data = command
        self.conveyor_publisher.publish(msg)
        self.get_logger().info(f"Sent conveyor command: {command}")

    def control_gripper(self, position, wait=True):
        """Control the gripper to open or close."""
        try:
            if not self.gripper_action_client.wait_for_server(timeout_sec=5.0):
                self.get_logger().error("Gripper action server not available!")
                return
            goal = GripperCommand.Goal()
            goal.command.position = position
            goal.command.max_effort = -1.0
            send_goal_future = self.gripper_action_client.send_goal_async(goal)
            rclpy.spin_until_future_complete(self, send_goal_future)

            result = send_goal_future.result()
            if not result.accepted:
                self.get_logger().error("Gripper command was rejected by the server.")
                return
            self.get_logger().info("Gripper command accepted.")

            if wait:
                time.sleep(WAIT_TIME)
                self.update_status()

        except Exception as e:
            self.get_logger().error(f"Failed to control gripper: {e}")

    def align_camera_to_box(self):
        """Align the camera to the target box."""
        if not self.target_box:
            self.get_logger().warning("No target box available for alignment.")
            return

        # 박스 중심 계산
        cx = (self.target_box["bbox"][0] + self.target_box["bbox"][2]) / 2
        cy = (self.target_box["bbox"][1] + self.target_box["bbox"][3]) / 2

        #### 바운딩 박스 중심 보정
        undistorted_points = cv2.undistortPoints(
            np.array([[[cx, cy]]], dtype=np.float32), 
            self.mtx, 
            self.dist, 
            P=self.mtx
        )
        corrected_cx, corrected_cy = undistorted_points[0][0]

        # 칼만 필터를 통해 중심 좌표 보정
        filtered_cx = self.kalman_filter_x.update(corrected_cx)
        filtered_cy = self.kalman_filter_y.update(corrected_cy)

        self.get_logger().info(f"Filtered target center: cx={filtered_cx}, cy={filtered_cy}")

        # 실제 이미지 해상도에 맞게 설정 (예: 1280x960)
        frame_width = 640
        frame_height = 480
        frame_center_x = frame_width / 2
        frame_center_y = frame_height / 2

        self.get_logger().info(f"Frame center: x={frame_center_x}, y={frame_center_y}")

        # 프레임 중심과의 차이 계산
        dx = (frame_center_x - filtered_cx) / 3
        dy = (frame_center_y - filtered_cy) / 3

        self.get_logger().info(f"Difference from frame center: dx={dx}, dy={dy}")

        # 현재 로봇의 위치 가져오기
        current_x, current_y, current_z = self.current_xyz
        self.get_logger().info(f"Current XYZ: x={current_x}, y={current_y}, z={current_z}")

        # 오프셋 적용: 카메라 오프셋과 태스크 명령 오프셋을 모두 더함
        target_x = current_x + dy + CAMERA_OFFSET_X + self.offset_xy[0]
        target_y = current_y + dx + CAMERA_OFFSET_Y + self.offset_xy[1]
        target_z = current_z + CAMERA_OFFSET_Z

        self.get_logger().info(f"Calculated target position: x={target_x}, y={target_y}, z={target_z}")

        self.move_arm(target_x, target_y, target_z)

    def image_callback(self, msg):
        """카메라 이미지 처리 및 시각화 (필요 시 구현)"""
        # 실제 카메라 이미지 토픽을 구독하고, 이미지 데이터를 처리하는 로직 추가
        pass

def main(args=None):
    rclpy.init(args=args)
    node = Turtlebot3ManipulationTest()

    # 멀티스레드 실행기 사용
    executor = MultiThreadedExecutor()
    executor.add_node(node)

    usage = """
    Control Your Turtlebot3 Manipulator via ROS2 Topics!
    ---------------------------------------------------
    Use 'ros2 topic pub' to send tasks to 'task_commands' topic.
    Example:
    ros2 topic pub /task_commands std_msgs/String '{"task": ["red", "red"], "offset_xy": [0, 0]}'

    Available automatic commands:
        Tasks will be processed automatically as they are received.
    """

    print(usage)

    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()
