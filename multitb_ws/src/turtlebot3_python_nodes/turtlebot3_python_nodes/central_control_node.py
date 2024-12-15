#!/usr/bin/env python3

import rclpy
import json
from rclpy.node import Node
from std_msgs.msg import String
from std_srvs.srv import Trigger
from turtlebot3_interfaces.srv import ExitRequest  # 사용자 정의 서비스
from turtlebot3_python_nodes.db_manager import DBManager  # DBManager 클래스 import
from rclpy.action import ActionClient
from geometry_msgs.msg import Pose
from datetime import datetime

class CentralControlNode(Node):
    def __init__(self):
        super().__init__('central_control_node')
        
        # 파라미터 가져오기
        #db_path = self.get_parameter('db_path').get_parameter_value().string_value
        db_path = "/home/rokey/Documents/RokeyProjects/multitb_ws/src/turtlebot3_python_nodes/parking_system.db"

        if not db_path:
            self.get_logger().error("DB path parameter 'db_path' is not set.")
            raise ValueError("DB path parameter 'db_path' is not set.")        
        
        # DBManager 초기화 및 DB 초기화
        self.db_manager = DBManager(db_path)
        self.db_manager.initialize_database()
        
        # 로그를 위한 퍼블리셔 (중앙 제어 노드에서 로그 생성)
        self.log_publisher = self.create_publisher(String, '/central_control/logs', 10)
        
        # 토픽 구독자
        self.create_subscription(String, '/entry_camera/vehicle_detected', self.vehicle_detected_callback, 10)
        self.create_subscription(String, '/payment/confirmation', self.payment_confirmation_callback, 10)

        # ExitRequest 서비스 서버 생성
        self.exit_request_service = self.create_service(
            ExitRequest,
            'exit_request',
            self.handle_exit_request
        )
        self.get_logger().info("ExitRequest 서비스가 준비되었습니다.")
           
    def vehicle_detected_callback(self, msg):
        self.get_logger().info(f"Vehicle detected: {msg.data}")
        self.log_publisher.publish(String(data=f"Vehicle detected: {msg.data}"))
        # 차량 감지 시 로봇 제어 명령 수행
        vehicle_id = msg.data  # 예시: msg.data에 vehicle_id가 포함되어 있다고 가정
        # self.handle_vehicle_detection(vehicle_id)
    
    def payment_confirmation_callback(self, msg):
        self.get_logger().info(f"Payment confirmed: {msg.data}")
        self.log_publisher.publish(String(data=f"Payment confirmed: {msg.data}"))
        # 결제 정보 파싱 및 DB 기록
        payment_info = self.parse_payment_info(msg.data)
        if payment_info:
            # Prepare data for Payment_Log table
            payment_data = {
                "vehicle_id": payment_info.get("vehicle_id"),
                "entry_time": payment_info.get("entry_time"),
                "exit_time": payment_info.get("exit_time"),
                "total_fee": payment_info.get("total_fee"),
                "payment_method": payment_info.get("payment_method"),
                "timestamp": datetime.now().isoformat()
            }
            self.db_manager.insert_data("Payment_Log", payment_data)
            self.log_publisher.publish(String(data=f"Payment recorded for vehicle {payment_data.get('vehicle_id')}"))

            # Task_Log을 업데이트하여 작업을 완료("Exited")로 표시
            update_data = {
                "end_time": payment_data["exit_time"],
                "status": "출차 중"
            }
            # "Payment Pending" 상태인 'Exit' Task_Log 찾기
            task_logs = self.db_manager.fetch_data(
                table="Task_Log",
                columns="task_id, slot_id",
                conditions=["vehicle_id = ?", "task_type = ?", "status = ?"],
                parameters=[payment_data['vehicle_id'], "출차", "결제 중"]
            )
            if task_logs:
                task_id, slot_id = task_logs[-1]  # 가장 최근 Task_Log 사용
                self.db_manager.update_data(
                    table="Task_Log",
                    data=update_data,
                    conditions=["task_id = ?"],
                    parameters=[task_id]
                )
                self.log_publisher.publish(String(data=f"Task_Log updated for vehicle {payment_data.get('vehicle_id')}"))

                # Parking_Slot을 업데이트하여 슬롯을 비어있는 상태로 표시
                update_slot_data = {
                    "vehicle_id": None
                }
                self.db_manager.update_data(
                    table="Parking_Slot",
                    data=update_slot_data,
                    conditions=["slot_id = ?"],
                    parameters=[slot_id]
                )
                self.log_publisher.publish(String(data=f"Parking_Slot {slot_id} marked as empty"))
            else:
                self.get_logger().error(f"No Payment Pending Exit Task_Log found for vehicle_id: {payment_data['vehicle_id']}")
        else:
            self.get_logger().error("Invalid payment received.")

    def parse_payment_info(self, data_str):
        try:
            payment_info = json.loads(data_str)
            return payment_info
        except json.JSONDecodeError:
            self.get_logger().error("Failed to parse payment info")
            return {}
        
    def handle_exit_request(self, request, response):
        car_number = request.car_number
        self.get_logger().info(f"Exit request received for car number: {car_number}")
        # DB에서 요금 계산
        fee = self.db_manager.calculate_fee(car_number)
        # DB에서 입차 시간 가져오기
        entry_time = self.get_entry_time(car_number)
        self.get_logger().info(f"fee: {fee}, entry_time: {entry_time}")

        if fee > 0 and entry_time:
            # Task_Log에 출차 요청 기록 (end_time은 결제 후 설정)
            slot_id = self.get_slot_id(car_number)
            if slot_id is None:
                self.get_logger().error(f"No Parking_Slot found for vehicle_id: {car_number}")
                response.status = False
                response.entry_time = ""
                response.fee = 0
                response.log = "출차 요청 실패: 슬롯을 찾을 수 없습니다."
                self.log_publisher.publish(String(data=f"{car_number} 차량의 출차 요청이 실패했습니다: 슬롯을 찾을 수 없습니다."))
                return response
            
            # 차량의 마지막 입차 이미지 경로 조회
            vehicle_img = self.db_manager.get_last_parking_image(car_number)
            if not vehicle_img:
                vehicle_img = "default_img.jpg"  # 기본 이미지 경로 설정

            # Task_Log에 출차 요청 기록 (end_time은 결제 후 설정)
            task_data = {
                "robot_id": 1,  # 예시 로봇 ID, 실제 환경에 맞게 설정 필요
                "vehicle_id": car_number,
                "vehicle_img": vehicle_img,  # 이전 입차 이미지 경로 사용
                "slot_id": slot_id,
                "task_type": "출차",
                "start_time": datetime.now().isoformat(timespec='seconds'),  # 마이크로초 제외
                "end_time": None,
                "status": "결제 중"
            }
            self.db_manager.insert_data("Task_Log", task_data)
            self.log_publisher.publish(String(data=f"Task_Log created for vehicle {car_number} with status 'Payment Pending'"))

            # 응답 설정
            response.status = True
            response.entry_time = entry_time
            response.fee = fee
            response.log = "출차 요청이 성공적으로 접수되었습니다. 요금을 결제해주세요."
            
            # 로그 퍼블리시
            self.log_publisher.publish(String(data=f"{car_number} 차량의 출차 요청이 접수되었습니다. 요금: {fee}원"))
        else:
            response.status = False
            response.entry_time = ""
            response.fee = 0
            response.log = "출차 요청 실패: 차량을 찾을 수 없습니다."
            
            self.log_publisher.publish(String(data=f"{car_number} 차량의 출차 요청이 실패했습니다: 차량을 찾을 수 없습니다."))
        
        return response

    def get_entry_time(self, vehicle_id):
        """Fetches the entry time for the given vehicle_id from Task_Log."""
        task_logs = self.db_manager.fetch_data(
            table="Task_Log",
            columns="start_time",
            conditions=[f"vehicle_id = '{vehicle_id}'", "end_time IS NULL"]
        )
        if task_logs:
            # Assuming the latest entry without an end_time is the current parking session
            return task_logs[-1][0]  # start_time
        else:
            self.get_logger().error(f"No active Task_Log found for vehicle_id: {vehicle_id}")
            return ""

    # def send_move_command(self, robot_namespace, goal_pose):
    #     action_client = self.action_clients.get(robot_namespace)
    #     if action_client:
    #         goal_msg = MoveRobot.Goal()
    #         goal_msg.pose = goal_pose
    #         action_client.wait_for_server()
    #         send_goal_future = action_client.send_goal_async(goal_msg, feedback_callback=self.feedback_callback)
    #         send_goal_future.add_done_callback(self.goal_response_callback)
    #     else:
    #         self.get_logger().error(f'No action client found for {robot_namespace}')

    def get_slot_id(self, vehicle_id):
        """vehicle_id에 할당된 slot_id를 가져옵니다."""
        slot_id = self.db_manager.get_slot_id_by_vehicle_id(vehicle_id)
        if slot_id:
            return slot_id
        else:
            self.get_logger().error(f"No Parking_Slot found for vehicle_id: {vehicle_id}")
            return None
    
    def handle_emergency_stop(self, request, response):
        self.get_logger().info("Emergency stop requested.")
        # 비상 정지 로직 수행
        success = self.execute_emergency_stop()
        response.success = success
        response.message = "Emergency stop executed." if success else "Emergency stop failed."
        return response
    
    def execute_emergency_stop(self):
        # 로봇 정지 로직 구현
        self.get_logger().info("Executing emergency stop.")
        return True
    
    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected.')
            return
        self.get_logger().info('Goal accepted.')
        goal_handle.execute()
    
    def feedback_callback(self, feedback):
        self.get_logger().info(f'Received feedback: {feedback.feedback}')
    
    def handle_vehicle_detection(self, vehicle_id):
        # 차량 감지 시 로봇에게 명령 보내기 (예시)
        # 예: tb1에게 차량 픽업 명령 보내기
        goal_pose = Pose()  # 목표 위치 설정
        # 목표 위치는 실제 시나리오에 맞게 설정 필요
        goal_pose.position.x = 1.0
        goal_pose.position.y = 1.0
        goal_pose.position.z = 0.0
        goal_pose.orientation.w = 1.0
        self.send_move_command('tb1', goal_pose)

def main(args=None):
    rclpy.init(args=args)
    node = CentralControlNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Central Control Node shutting down...')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()