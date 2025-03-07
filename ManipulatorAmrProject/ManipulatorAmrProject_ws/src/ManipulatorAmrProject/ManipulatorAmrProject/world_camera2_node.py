import cv2
import time
import numpy as np
import cv2.aruco as aruco
import transforms3d
import threading
from collections import deque
import rclpy
from rclpy.node import Node
from rclpy.callback_groups import ReentrantCallbackGroup
from geometry_msgs.msg import Twist
from visualization_msgs.msg import MarkerArray
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Pose


from geometry_msgs.msg import PoseStamped

from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy

class ArucoMarkerDetector(Node):
    def __init__(self):
        super().__init__('aruco_marker_detector')
        
        # ArUco 마커 ID와 이름 매핑
        self.marker_names = {
            20: "origin",
            6: "turtle",
            16: "point1",
            14: "point2",
        }
        
        # 카메라 보정 매트릭스
        self.mtx = np.array([[1.40399902e+03, 0.00000000e+00, 7.06425163e+02],
                             [0.00000000e+00, 1.40304826e+03, 4.37298164e+02],
                             [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
        
        # 카메라 왜곡 계수
        self.dist = np.array([[4.85986335e-02, 1.17952692e-01, -8.58481339e-05, -3.71521243e-03, -6.76945165e-01]])
        
        # ArUco 사전 및 파라미터 설정
        self.aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_5X5_100)
        self.parameters = aruco.DetectorParameters()
        
        # 마커 크기 (미터 단위)
        self.marker_length = 0.1065
        
        # 위치 버퍼 크기
        self.buffer_size = 10
        
        # 마커 위치 저장을 위한 딕셔너리 초기화
        self.marker_world_positions = {}
        self.last_known_positions = {}
        self.initialize_marker_positions()
        
        # 카메라 초기화
        self.cap = self.initialize_camera()
        
        qos_profile = QoSProfile(
                reliability=QoSReliabilityPolicy.BEST_EFFORT,
                history=QoSHistoryPolicy.KEEP_LAST,
                depth=10
            )
        
        # ROS2 퍼블리셔 생성 (터틀봇 제어용)
        self.cmd_publisher = self.create_publisher(Twist, '/cmd_vel', qos_profile)
        
        # 터틀봇 포즈 퍼블리셔 생성
        self.turtle_pose_publisher = self.create_publisher(PoseStamped, '/turtle_pose', 10)
        
        # 현재 터틀봇 마커 방향 초기화
        self.turtle_yaw = None
        
        # 콜백 그룹 생성
        self.callback_group = ReentrantCallbackGroup()
        
        # 타이머 생성 (10Hz로 cmd_vel 발행)
        self.create_timer(0.1, self.publish_cmd_vel_timer_callback, callback_group=self.callback_group)
        
        # 속도 저장 변수
        self.current_linear_velocity = 0.0
        self.current_angular_velocity = 0.0
        
        # 스레드 생성
        self.camera_thread = threading.Thread(target=self.camera_loop)
        self.camera_thread.start()
        
        # cmd_vel 토픽 연결 확인
        if not self.verify_cmd_vel_connection():
            self.get_logger().warn("터틀봇과의 연결이 확인되지 않았습니다. 제어가 작동하지 않을 수 있습니다.")
        

        # 로깅 레벨 설정
        self.get_logger().set_level(rclpy.logging.LoggingSeverity.INFO)
        
    def publish_cmd_vel_timer_callback(self):
        try:
            cmd_vel_msg = Twist()
            cmd_vel_msg.linear.x = self.current_linear_velocity
            cmd_vel_msg.angular.z = self.current_angular_velocity
            self.cmd_publisher.publish(cmd_vel_msg)
            # 로그 메시지
            self.get_logger().info(f"Publishing cmd_vel: linear_x={self.current_linear_velocity:.2f}, angular_z={self.current_angular_velocity:.2f}")
        except Exception as e:
            self.get_logger().error(f"Error publishing cmd_vel: {str(e)}")


    def initialize_marker_positions(self):
        # 마커 위치 버퍼 초기화
        for marker_id, name in self.marker_names.items():
            if name.startswith("point") or name == "turtle":
                self.marker_world_positions[name] = deque(maxlen=self.buffer_size)
        
        # 마지막으로 알려진 위치 초기화
        self.last_known_positions = {name: None for name in self.marker_world_positions if name.startswith("point")}

    def initialize_camera(self):
        # 카메라 연결 및 설정
        cap, index = self.find_camera_index()
        if cap is None:
            self.get_logger().error("카메라를 연결할 수 없습니다.")
            return None
        
        # 카메라 속성 설정 (해상도 및 코덱)
        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        return cap

    def find_camera_index(self, start_index=1, end_index=10):
        # 사용 가능한 카메라 인덱스 찾기
        for index in range(start_index, end_index + 1):
            cap = cv2.VideoCapture(index)
            if cap.isOpened():
                self.get_logger().info(f"카메라 연결됨: 인덱스 {index}")
                return cap, index
            cap.release()
        
        self.get_logger().warn("사용 가능한 카메라를 찾을 수 없습니다.")
        return None, -1

    def detect_markers(self, frame):
        # ArUco 마커 감지
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, rejected = aruco.detectMarkers(gray, self.aruco_dict, parameters=self.parameters)
        return corners, ids

    def estimate_poses(self, corners):
        # 마커의 포즈 추정
        return aruco.estimatePoseSingleMarkers(corners, self.marker_length, self.mtx, self.dist)

    def process_markers(self, frame, corners, ids, rvecs, tvecs):
        # 감지된 마커 처리
        marker_positions = {}
        for i, (marker_id, rvec, tvec, corner) in enumerate(zip(ids.flatten(), rvecs, tvecs, corners)):
            name = self.marker_names.get(marker_id, f"id_{marker_id}")
            marker_positions[name] = (rvec, tvec)
            self.draw_marker(frame, corner, rvec, tvec)
        return marker_positions

    def draw_marker(self, frame, corner, rvec, tvec):
        # 마커 시각화
        cv2.polylines(frame, [corner.reshape((-1, 1, 2)).astype(np.int32)], True, (0, 255, 0), 2)
        cv2.drawFrameAxes(frame, self.mtx, self.dist, rvec, tvec, 0.1)

    def calculate_world_coordinates(self, marker_positions):
        # 월드 좌표계 변환 행렬 계산
        if "origin" in marker_positions:
            rvec_ref, tvec_ref = marker_positions["origin"]
            R_ref, _ = cv2.Rodrigues(rvec_ref)
            t_ref = tvec_ref.reshape(3, 1)
            R_camera_to_world = R_ref.T
            t_camera_to_world = -np.dot(R_ref.T, t_ref)
            return R_camera_to_world, t_camera_to_world
        return None, None
    
    def publish_cmd_vel(self, linear_velocity, angular_velocity):
        cmd_vel_msg = Twist()
        cmd_vel_msg.linear.x = linear_velocity
        cmd_vel_msg.angular.z = angular_velocity
        self.cmd_publisher.publish(cmd_vel_msg)
        self.get_logger().info(f"Publishing cmd_vel: linear={linear_velocity}, angular={angular_velocity}")

    def calculate_velocities(self, turtle_position, turtle_yaw, target_position):
        dx = target_position[0][0] - turtle_position[0][0]
        dy = target_position[1][0] - turtle_position[1][0]
        distance = np.sqrt(dx**2 + dy**2)
        target_angle = np.arctan2(dy, dx)
        angle_diff = target_angle - turtle_yaw
        angle_diff = np.arctan2(np.sin(angle_diff), np.cos(angle_diff))  # -π에서 π 사이로 정규화
        # 최대 속도 설정
        max_linear_speed = 0.1
        max_angular_speed = 0.2  # 회전 속도는 더 빠르게 설정
        if abs(angle_diff) > np.radians(5):  # 5도 이상 차이 나면 회전만 수행
            linear_speed = 0  # 직선 속도는 0
            angular_speed = max_angular_speed * np.tanh(angle_diff)  # 회전 속도
            self.get_logger().info(f"회전 중: 각도 차이 = {np.degrees(angle_diff):.2f}° \n (회전 속도 = {angular_speed:.2f})")
        else:  # 5도 이내면 직선 이동만 수행
            linear_speed = min(max_linear_speed, 0.5 * distance)  # 직선 속도
            angular_speed = 0  # 회전 속도는 0
            self.get_logger().info(f" 직선 이동 중: 거리 = {distance:.2f} \n (속도 = {linear_speed:.2f})")
        # 계산된 속도를 클래스 변수에 할당
        self.current_linear_velocity = float(linear_speed)
        self.current_angular_velocity = float(angular_speed)
        return linear_speed, angular_speed
    
    def process_turtle_marker(self, marker_positions, R_camera_to_world, t_camera_to_world):
        avg_turtle_position = None
        turtle_yaw_deg = None
        if "turtle" in marker_positions and R_camera_to_world is not None:
            rvec_turtle, tvec_turtle = marker_positions["turtle"]
            R_turtle, _ = cv2.Rodrigues(rvec_turtle)
            t_turtle = tvec_turtle.reshape(3, 1)
            turtle_position_world = np.dot(R_camera_to_world, t_turtle) + t_camera_to_world
            R_turtle_world = np.dot(R_camera_to_world, R_turtle)
            x_axis = R_turtle_world[:, 0]
            turtle_yaw = np.arctan2(x_axis[1], x_axis[0])
            turtle_yaw_deg = np.degrees(turtle_yaw)

            self.marker_world_positions["turtle"].append(turtle_position_world)
            avg_turtle_position = np.mean(self.marker_world_positions["turtle"], axis=0)
            self.last_known_positions["turtle"] = avg_turtle_position
            self.turtle_yaw = turtle_yaw

            # 터틀봇 포즈 퍼블리시
            self.publish_turtle_pose(avg_turtle_position, turtle_yaw)

            # 목표 위치 (예: point1)를 가져옵니다.
            target_position = self.last_known_positions.get("point1")
            if target_position is not None:
                self.calculate_velocities(avg_turtle_position, turtle_yaw, target_position)

        return avg_turtle_position, turtle_yaw_deg


    def process_point_markers(self, marker_positions, R_camera_to_world, t_camera_to_world, avg_turtle_position, turtle_yaw):
        # 포인트 마커 처리
        points_info = []
        for name in self.marker_world_positions.keys():
            if not name.startswith("point"):
                continue
            
            avg_world_position = self.calculate_point_position(name, marker_positions, R_camera_to_world, t_camera_to_world)
            if avg_world_position is None:
                continue

            if avg_turtle_position is not None:
                distance, relative_angle_deg = self.calculate_distance_and_angle(avg_world_position, avg_turtle_position, turtle_yaw)
                if relative_angle_deg is not None:
                    points_info.append({"name": name, "distance": distance * 100, "angle": relative_angle_deg})
                else:
                    points_info.append({"name": name, "distance": distance * 100, "angle": "N/A"})

        return points_info

    def calculate_point_position(self, name, marker_positions, R_camera_to_world, t_camera_to_world):
        # 포인트 마커의 위치 계산
        if name in marker_positions and R_camera_to_world is not None:
            rvec_point, tvec_point = marker_positions[name]
            t_point = tvec_point.reshape(3, 1)
            world_position = np.dot(R_camera_to_world, t_point) + t_camera_to_world
            self.marker_world_positions[name].append(world_position)
            avg_world_position = np.mean(self.marker_world_positions[name], axis=0)
            self.last_known_positions[name] = avg_world_position
        elif name in self.last_known_positions and self.last_known_positions[name] is not None:
            avg_world_position = self.last_known_positions[name]
        else:
            return None
        return avg_world_position
    
    


    def draw_marker_info(self, frame, name, avg_world_position, marker_center_x, marker_center_y):
        # 마커 정보를 프레임에 그리기
        cv2.putText(frame, f"{name} X: {avg_world_position[0][0]*100:.2f} cm", (marker_center_x - 150, marker_center_y - 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        cv2.putText(frame, f"{name} Y: {avg_world_position[1][0]*100:.2f} cm", (marker_center_x - 150, marker_center_y - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        cv2.putText(frame, f"{name} Z: {avg_world_position[2][0]*100:.2f} cm", (marker_center_x - 150, marker_center_y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    def draw_turtle_point_line(self, frame, turtle_center, point_center):
        # 터틀봇과 포인트 사이의 선 그리기
        cv2.line(frame, turtle_center, point_center, (0, 0, 255), 2)

    def display_points_info(self, frame, points_info, turtle_yaw_deg):
        """
        화면에 터틀봇과 포인트 마커 정보 표시
        """
        y_offset = 20  # 텍스트 표시 시작 y좌표

        # 터틀봇 좌표 표시
        turtle_position = self.last_known_positions.get("turtle")
        if turtle_position is not None:
            cv2.putText(frame, f"Turtle X: {turtle_position[0][0]*100:.2f} cm", (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            y_offset += 20
            cv2.putText(frame, f"Turtle Y: {turtle_position[1][0]*100:.2f} cm", (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            y_offset += 20
            cv2.putText(frame, f"Turtle Z: {turtle_position[2][0]*100:.2f} cm", (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            y_offset += 20
        else:
            cv2.putText(frame, "Turtle position: Unknown", (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            y_offset += 20
        
        
        # 터틀봇 방향(yaw) 정보 표시
        if turtle_yaw_deg is not None:
            cv2.putText(frame, f"Turtle Yaw (World): {turtle_yaw_deg:.2f}°", (10, y_offset), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
        else:
            cv2.putText(frame, "Turtle Yaw: N/A", (10, y_offset), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
        y_offset += 20

        # 포인트 마커 정보 표시
        for info in points_info:
            distance = info['distance']
            angle = info['angle']
            
            if isinstance(distance, (int, float)) and isinstance(angle, (int, float)):
                text = f"{info['name']}: Distance={distance:.2f} cm, Relative Angle={angle:.2f}°"
            else:
                text = f"{info['name']}: Distance={distance} cm, Relative Angle={angle}°"
            
            cv2.putText(frame, text, (10, y_offset), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
            y_offset += 20
            
    def calculate_angle_between_positions(self, start_position, end_position):
        dx = end_position[0][0] - start_position[0][0]
        dy = end_position[1][0] - start_position[1][0]
        angle = np.arctan2(dy, dx)
        return angle

    def calculate_distance_and_angle(self, point_position, turtle_position, turtle_yaw):
        # 터틀봇과 포인트 간의 x, y, z 거리 계산
        dx = point_position[0][0] - turtle_position[0][0]
        dy = point_position[1][0] - turtle_position[1][0]
        dz = point_position[2][0] - turtle_position[2][0]

        # 3차원 유클리드 거리 계산
        distance = np.sqrt(dx**2 + dy**2 + dz**2)

        # 포인트까지의 각도 계산 (x-z 평면에서)
        angle_to_point = np.arctan2(dx, dz)

        # 터틀봇의 방향(yaw)을 알 수 없는 경우 처리
        if turtle_yaw is None:
            relative_angle = None
            relative_angle_deg = None
        else:
            # 터틀봇 기준 상대 각도 계산
            relative_angle = angle_to_point - turtle_yaw
            # 각도를 -π에서 π 사이로 정규화
            relative_angle = (relative_angle + np.pi) % (2 * np.pi) - np.pi
            # 라디안을 도(degree)로 변환
            relative_angle_deg = np.degrees(relative_angle)

        return distance, relative_angle_deg

    
    
    def move_to_target(self, current_position, current_yaw, target_position):
        distance, angle = self.calculate_distance_and_angle(target_position, current_position, current_yaw)
        
        # 목표 지점을 향해 회전
        angular_speed = 0.5  # 회전 속도 (rad/s)
        rotation_time = abs(angle) / angular_speed
        self.publish_cmd_vel(0.0, angular_speed if angle > 0 else -angular_speed)
        time.sleep(rotation_time)
        
        # 목표 지점을 향해 이동w=-4.
        linear_speed = 0.2  # 선형 속도 (m/s)
        move_time = distance / linear_speed
        self.publish_cmd_vel(linear_speed, angular_speed)
        time.sleep(move_time)
        
        # 정지
        self.publish_cmd_vel(0.0, 0.0)
        
        
        # 목표 지점에 도착했는지 확인
        final_distance, _ = self.calculate_distance_and_angle(current_position, target_position, current_yaw)
        return final_distance < 0.05  # 5cm 이내에 도착했다고 판단
        
    def create_marker_array_msg(self, marker_positions, R_camera_to_world, t_camera_to_world):
        marker_array = MarkerArray()
        for name, (rvec, tvec) in marker_positions.items():
            marker = Marker()
            marker.header.frame_id = "camera_frame"
            marker.header.stamp = self.get_clock().now().to_msg()
            marker.ns = name
            marker.id = self.marker_names.get(name, 0)
            marker.pose = self.calculate_world_pose(rvec, tvec, R_camera_to_world, t_camera_to_world)
            marker_array.markers.append(marker)
        return marker_array
    
    def publish_turtle_pose(self, position, yaw):
        pose_msg = PoseStamped()
        pose_msg.header.stamp = self.get_clock().now().to_msg()
        pose_msg.header.frame_id = "world"
        pose_msg.pose.position.x = position[0][0]
        pose_msg.pose.position.y = position[1][0]
        pose_msg.pose.position.z = position[2][0]
        
        # Yaw를 쿼터니언으로 변환
        quat = transforms3d.quaternions.axangle2quat([0, 0, 1], yaw)
        pose_msg.pose.orientation.w = quat[0]
        pose_msg.pose.orientation.x = quat[1]
        pose_msg.pose.orientation.y = quat[2]
        pose_msg.pose.orientation.z = quat[3]

        self.turtle_pose_publisher.publish(pose_msg)
        self.get_logger().info(f"Published turtle pose: x={position[0][0]:.2f}, y={position[1][0]:.2f}, z={position[2][0]:.2f}, yaw={np.degrees(yaw):.2f}°")
    
    
    
    def follow_waypoints(self):
        for waypoint in self.waypoints:
            target_position = self.last_known_positions.get(waypoint)
            if target_position is None:
                self.get_logger().warn(f"웨이포인트 {waypoint}의 위치를 알 수 없습니다. 건너뜁니다.")
                continue
            
            self.get_logger().info(f"웨이포인트 {waypoint}로 이동 중...")
            
            turtle_position = self.last_known_positions.get("turtle")
            if turtle_position is None:
                self.get_logger().warn("터틀봇의 위치를 알 수 없습니다. 웨이포인트 이동을 중단합니다.")
                break
            
            turtle_yaw = getattr(self, 'turtle_yaw', None)
            
            while not self.move_to_target(turtle_position, turtle_yaw, target_position):
                time.sleep(0.1)  # 짧은 대기 시간
                turtle_position = self.last_known_positions.get("turtle")
                if turtle_position is None:
                    self.get_logger().warn("터틀봇의 위치를 잃었습니다. 웨이포인트 이동을 중단합니다.")
                    break
            
            self.get_logger().info(f"웨이포인트 {waypoint}에 도착했습니다. 5초 대기...")
            time.sleep(5)  # 5초 대기
    
    def calculate_world_pose(self, rvec, tvec, R_camera_to_world, t_camera_to_world):
        R_marker, _ = cv2.Rodrigues(rvec)
        t_marker = tvec.reshape(3, 1)
        
        R_marker_world = np.dot(R_camera_to_world, R_marker)
        t_marker_world = np.dot(R_camera_to_world, t_marker) + t_camera_to_world
        
        pose = Pose()
        pose.position.x = t_marker_world[0][0]
        pose.position.y = t_marker_world[1][0]
        pose.position.z = t_marker_world[2][0]
        
        quat = transforms3d.quaternions.mat2quat(R_marker_world)
        pose.orientation.w = quat[0]
        pose.orientation.x = quat[1]
        pose.orientation.y = quat[2]
        pose.orientation.z = quat[3]
        
        return pose
    
    def verify_cmd_vel_connection(self):
        # 토픽 연결 상태 확인
        timeout = 2.0  # 2초 대기
        start_time = time.time()
        
        while (time.time() - start_time) < timeout:
            if self.cmd_publisher.get_subscription_count() > 0:
                self.get_logger().info("cmd_vel 토픽 연결 확인됨")
                return True
            time.sleep(0.1)
        
        self.get_logger().error("cmd_vel 토픽 연결 실패")
        return False

    
    def camera_loop(self):
        while rclpy.ok():
            try:
                if self.cap is None or not self.cap.isOpened():
                    self.get_logger().warn("카메라가 연결되지 않았습니다. 재초기화 중...")
                    self.cap = self.initialize_camera()
                    if self.cap is None:
                        time.sleep(1)
                        continue

                ret, frame = self.cap.read()
                if not ret:
                    self.get_logger().warn("프레임을 읽을 수 없습니다.")
                    self.current_linear_velocity = 0.0
                    self.current_angular_velocity = 0.0
                    continue

                undistorted_frame = cv2.undistort(frame, self.mtx, self.dist)
                corners, ids = self.detect_markers(undistorted_frame)

                if ids is not None:
                    rvecs, tvecs, _ = self.estimate_poses(corners)
                    marker_positions = self.process_markers(undistorted_frame, corners, ids, rvecs, tvecs)
                    R_camera_to_world, t_camera_to_world = self.calculate_world_coordinates(marker_positions)
                    avg_turtle_position, turtle_yaw_deg = self.process_turtle_marker(marker_positions, R_camera_to_world, t_camera_to_world)
                    points_info = self.process_point_markers(marker_positions, R_camera_to_world, t_camera_to_world, avg_turtle_position, turtle_yaw_deg)
                    self.display_points_info(undistorted_frame, points_info, turtle_yaw_deg)

                cv2.imshow("Aruco Marker Detection", undistorted_frame)
                
                key = cv2.waitKey(1) & 0xFF
                if key == 27:  # ESC 키를 누르면 종료
                    break

            except Exception as e:
                self.get_logger().error(f"카메라 루프에서 오류 발생: {str(e)}")
                # self.current_linear_velocity = 0.0
                # self.current_angular_velocity = 0.0

            time.sleep(0.1)  # 시스템 부하 방지

        cv2.destroyAllWindows()

    
    def run(self):
        try:
            while rclpy.ok():
                if self.cap is None or not self.cap.isOpened():
                    self.get_logger().warn("카메라가 연결되지 않았습니다. 재초기화 중...")
                    self.cap = self.initialize_camera()
                    if self.cap is None:
                        time.sleep(1)
                        continue
                # 카메라 상태 확인 후 spin_once 호출
                rclpy.spin_once(self, timeout_sec=0.1)
        except KeyboardInterrupt:
            pass
        finally:
            if self.cap is not None:
                self.cap.release()
            cv2.destroyAllWindows()
            
def main(args=None):
    rclpy.init(args=args)
    detector = ArucoMarkerDetector()
    
    try:
        detector.run()
    except KeyboardInterrupt:
        pass
    finally:
        detector.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()  