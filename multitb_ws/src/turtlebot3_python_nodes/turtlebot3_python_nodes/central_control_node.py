#!/usr/bin/env python3

import rclpy
import json
from rclpy.node import Node
from std_msgs.msg import String
from std_srvs.srv import Trigger
from turtlebot3_interfaces.srv import ExitRequest, GetSystemState  # 사용자 정의 서비스
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

        # ExitRequest 서비스 서버 생성
        self.exit_request_service = self.create_service(
            ExitRequest,
            'exit_request',
            self.handle_exit_request
        )
        self.get_logger().info("ExitRequest 서비스가 준비되었습니다.")
        
        # GetSystemState 서비스 서버 생성
        self.get_system_state_service = self.create_service(
            GetSystemState,
            'get_system_state',
            self.handle_get_system_state
        )
        self.get_logger().info("GetSystemState 서비스가 준비되었습니다.")
           
        # 로그를 위한 퍼블리셔 (중앙 제어 노드에서 로그 생성)
        self.log_publisher = self.create_publisher(String, '/central_control/logs', 10)

        # 로봇 상태 퍼블리셔 추가
        self.robot_status_publisher = self.create_publisher(String, '/central_control/robot_status', 10)
        
        # 주차 슬롯 상태 퍼블리셔 추가
        self.slot_status_publisher = self.create_publisher(String, '/parking_status', 10)

        # /vehicle_detected 토픽에 "1234, 차량 1234번 출차합니다." 이런 식으로 보낼 수 있음
        self.vehicle_pub = self.create_publisher(String, '/vehicle_detected', 10)


        # 토픽 구독자
        self.create_subscription(String, '/vehicle_detected', self.vehicle_detected_callback, 10)
        self.create_subscription(String, '/payment/confirmation', self.payment_confirmation_callback, 10)
        self.create_subscription(String, '/nav_callback', self.nav_callback, 10)

    def nav_callback(self, msg):
        # 예: "robot1 pick_off 1234 (4,9)"
        parts = msg.data.split()
        if len(parts) < 4:
            self.get_logger().error("nav_callback message format invalid")
            return

        robot_name = parts[0]    # robot1 or robot2
        action_type = parts[1]   # pick_off (출차/입차 완료 신호)
        vehicle_id = parts[2]
        coord_str = parts[3].strip("()")
        x_str, y_str = coord_str.split(",")
        x, y = int(x_str), int(y_str)

        # pick_off 일 때만 처리 (pick_up은 무시)
        if action_type != "pick_off":
            self.get_logger().info(f"nav_callback ignored: action_type={action_type}")
            return

        if robot_name == "robot1":
            # 입차 완료 시나리오
            # DB에서 해당 차량의 "주차 중" 상태를 찾아서 "주차 완료"로 업데이트
            self.finish_parking(vehicle_id)
            self.log(f"입차 작업 완료: 차량 {vehicle_id}, 좌표({x},{y})", origin="nav_callback")

        elif robot_name == "robot2":
            # 출차 완료 시나리오
            # DB에서 해당 차량의 "출차 중" 상태를 "출차 완료"로 변경
            self.finish_checkout(vehicle_id, x, y)
            
        else:
            self.get_logger().error(f"알 수 없는 로봇: {robot_name}")

    def finish_parking(self, vehicle_id):
        # "주차 중" 상태인 Task_Log를 "주차 완료"로 업데이트
        task_logs = self.db_manager.fetch_data(
            table="Task_Log",
            columns="task_id",
            conditions=["vehicle_id = ?", "task_type = ?"],
            parameters=[vehicle_id, "주차"]
        )
        if task_logs:
            task_id = task_logs[-1][0]
            update_data = {
                "end_time": datetime.now().isoformat(timespec='seconds'),
                "status": "주차 완료"
            }
            self.db_manager.update_data(
                table="Task_Log",
                data=update_data,
                conditions=["task_id = ?"],
                parameters=[task_id]
            )
        else:
            self.get_logger().error(f"주차 중 상태의 작업을 찾을 수 없음: 차량 {vehicle_id}")

    def finish_checkout(self, vehicle_id, x, y):
        # "출차 중" 상태인 Task_Log를 "출차 완료"로 업데이트
        task_logs = self.db_manager.fetch_data(
            table="Task_Log",
            columns="task_id",
            conditions=["vehicle_id = ?", "task_type = ?"],
            parameters=[vehicle_id, "출차"]
        )
        if task_logs:
            task_id = task_logs[-1][0]
            update_data = {
                "end_time": datetime.now().isoformat(timespec='seconds'),
                "status": "출차 완료"
            }
            self.db_manager.update_data(
                table="Task_Log",
                data=update_data,
                conditions=["task_id = ?"],
                parameters=[task_id]
            )
            # 출차 완료 메시지 발행
            out_msg = String()
            out_msg.data = f"{vehicle_id}, 차량 {vehicle_id}번 출차합니다."
            self.vehicle_pub.publish(out_msg)
            self.log(f"차량 {vehicle_id}번 출차 완료 및 메시지 발행", origin="nav_callback")
        else:
            self.get_logger().error(f"출차 중 상태의 작업을 찾을 수 없음: 차량 {vehicle_id}")


    def log(self, message, origin="central_control_node"):
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "origin": origin,
            "message": message
        }
        self.log_publisher.publish(String(data=json.dumps(log_data)))
        self.get_logger().info(message)

    def vehicle_detected_callback(self, msg):
        # 예: "1234, 대기 지역에 차량이 진입하였습니다."
        data_parts = msg.data.split(',', 1)
        if len(data_parts) < 2:
            self.get_logger().error("vehicle_detected_callback format invalid")
            return
        vehicle_id = data_parts[0].strip()
        message = data_parts[1].strip()

        self.log(f"Vehicle detected: {vehicle_id} - {message}")
        
        # 차량 감지 시 입차 시나리오: "주차 중" 상태로 DB 삽입
        task_data = {
            "robot_id": 1,  # robot1이 주차 담당
            "vehicle_id": vehicle_id,
            "vehicle_img": "default_img.jpg",
            "slot_id": None,
            "task_type": "주차",          # 입차 작업
            "start_time": datetime.now().isoformat(timespec='seconds'),
            "end_time": None,
            "status": "주차 중"          # 이제 주차 중 상태
        }
        self.db_manager.insert_data("Task_Log", task_data)
        self.log(f"주차 중 상태로 DB 저장: 차량 {vehicle_id}", origin="vehicle_detected_callback")

    
    def payment_confirmation_callback(self, msg):
        # 결제 완료 시 "출차 중"으로 변경
        self.get_logger().info(f"Payment confirmed: {msg.data}")
        self.log_publisher.publish(String(data=f"Payment confirmed: {msg.data}"))

        payment_info = self.parse_payment_info(msg.data)
        if payment_info:
            payment_data = {
                "vehicle_id": payment_info.get("vehicle_id"),
                "entry_time": payment_info.get("entry_time"),
                "exit_time": payment_info.get("exit_time"),
                "total_fee": payment_info.get("total_fee"),
                "payment_method": payment_info.get("payment_method"),
                "timestamp": datetime.now().isoformat()
            }
            self.db_manager.insert_data("Payment_Log", payment_data)
            self.log(f"Payment recorded for vehicle {payment_data.get('vehicle_id')}", origin="payment_confirmation")

            # 결제 후 "결제 중" 상태인 출차 Task_Log를 "출차 중"으로 업데이트
            task_logs = self.db_manager.fetch_data(
                table="Task_Log",
                columns="task_id, slot_id",
                conditions=["vehicle_id = ?", "task_type = ?", "status = ?"],
                parameters=[payment_data['vehicle_id'], "출차", "결제 중"]
            )
            if task_logs:
                task_id, slot_id = task_logs[-1]
                update_data = {
                    "end_time": payment_data["exit_time"],
                    "status": "출차 중"
                }
                self.db_manager.update_data(
                    table="Task_Log",
                    data=update_data,
                    conditions=["task_id = ?"],
                    parameters=[task_id]
                )
                self.log_publisher.publish(String(data=f"Task_Log updated for vehicle {payment_data.get('vehicle_id')}"))
                # 슬롯 비우기 (선택사항)
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

                # 출차 로봇(robot2) 작동 위해 /vehicle_detected 토픽에 출차용 메시지 발행
                # 예: "9999, 대기 지역에 차량이 진입하였습니다." 대신 출차 유도 메시지로 재활용 가능
                # 여기서는 같은 형식 유지 가정
                out_msg = String()
                out_msg.data = f"{payment_data['vehicle_id']}, 출차를 요청합니다"  # 출차를 유도하는 메시지
                self.vehicle_pub.publish(out_msg)
                self.log(f"출차 로봇 유도 메시지 발행: 차량 {payment_data['vehicle_id']}", origin="payment_confirmation")
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
        # kiosk에서 출차 요청 -> "결제 중"으로 DB 업데이트
        car_number = request.car_number
        self.get_logger().info(f"Exit request received for car number: {car_number}")
        fee = self.db_manager.calculate_fee(car_number)
        entry_time = self.get_entry_time(car_number)
        self.get_logger().info(f"fee: {fee}, entry_time: {entry_time}")

        if fee > 0 and entry_time:
            slot_id = self.get_slot_id(car_number)
            if slot_id is None:
                self.get_logger().error(f"No Parking_Slot found for vehicle_id: {car_number}")
                response.status = False
                response.entry_time = ""
                response.fee = 0
                response.log = "출차 요청 실패: 슬롯을 찾을 수 없습니다."
                self.log_publisher.publish(String(data=f"{car_number} 차량 출차 실패: 슬롯 없음"))
                self.log(f"{car_number} 차량 출차 실패: 슬롯 없음", origin="handle_exit_request")
                return response

            vehicle_img = self.db_manager.get_last_parking_image(car_number)
            if not vehicle_img:
                vehicle_img = "default_img.jpg"

            # 출차 Task_Log "결제 중" 상태 삽입
            task_data = {
                "robot_id": 1, 
                "vehicle_id": car_number,
                "vehicle_img": vehicle_img,
                "slot_id": slot_id,
                "task_type": "출차",
                "start_time": datetime.now().isoformat(timespec='seconds'),
                "end_time": None,
                "status": "결제 중"
            }
            self.db_manager.insert_data("Task_Log", task_data)
            self.log_publisher.publish(String(data=f"Task_Log created for vehicle {car_number} with status '결제 중'"))
            self.log(f"Task_Log created for vehicle {car_number} with status '결제 중'", origin="handle_exit_request")

            response.status = True
            response.entry_time = entry_time
            response.fee = fee
            response.log = "출차 요청 접수. 요금 결제 필요."
            self.log_publisher.publish(String(data=f"{car_number} 차량 출차 요청 접수. 요금: {fee}원"))
        else:
            response.status = False
            response.entry_time = ""
            response.fee = 0
            response.log = "출차 요청 실패: 차량 찾을 수 없음."
            self.log_publisher.publish(String(data=f"{car_number} 차량 출차 실패: 차량 없음"))
            self.log(f"{car_number} 차량 출차 실패: 차량 없음", origin="handle_exit_request")

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
            self.log(f"No active Task_Log found for vehicle_id: {vehicle_id}", origin="get_entry_time")
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
            self.log(f"No Parking_Slot found for vehicle_id: {vehicle_id}", origin="get_slot_id")
            return None
    
    def handle_emergency_stop(self, request, response):
        self.get_logger().info("Emergency stop requested.")
        self.log("Emergency stop requested.", origin="handle_emergency_stop")
        # 비상 정지 로직 수행
        success = self.execute_emergency_stop()
        response.success = success
        response.message = "Emergency stop executed." if success else "Emergency stop failed."
        return response
    
    def execute_emergency_stop(self):
        # 로봇 정지 로직 구현
        self.get_logger().info("Executing emergency stop.")
        self.log("Executing emergency stop.", origin="execute_emergency_stop")
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

    def update_slot_status(self, slot_id, task_type):
        # DB에서 slot_name 가져오기
        slot = self.db_manager.fetch_data(
            table="Parking_Slot",
            columns="slot_name",
            conditions=["slot_id = ?"],
            parameters=[slot_id]
        )
        if slot:
            slot_name = slot[0][0]
            slot_data = {
                "slot_name": slot_name,
                "task_type": task_type
            }
            self.slot_status_publisher.publish(String(data=json.dumps(slot_data)))
            self.log(f"Parking_Slot {slot_name} updated to {task_type}", origin="update_slot_status")
        else:
            self.log(f"No Parking_Slot found for slot_id: {slot_id}", origin="update_slot_status")

    def handle_get_system_state(self, request, response):
        # 로봇 상태 JSON 생성
        robots = self.db_manager.fetch_data(
            table="Robot_Info",
            columns="robot_id, status, last_task_id"
        )
        robot_status_list = []
        for robot in robots:
            robot_id, status, last_task_id = robot
            robot_status = {
                "robot_id": robot_id,
                "state": status,
                "last_task": last_task_id
            }
            robot_status_list.append(robot_status)
        
        # 주차 슬롯 상태 JSON 생성
        slots = self.db_manager.fetch_data(
            table="Parking_Slot",
            columns="slot_name, vehicle_id"
        )
        slot_status_list = []
        for slot in slots:
            slot_name, vehicle_id = slot
            task_type = "주차" if vehicle_id else "빈 슬롯"
            slot_status = {
                "slot_name": slot_name,
                "task_type": task_type
            }
            slot_status_list.append(slot_status)
        
        # JSON 문자열으로 변환
        response.robot_status_json = json.dumps(robot_status_list)
        response.slot_status_json = json.dumps(slot_status_list)
        
        self.log("System state requested via GetSystemState service.", origin="handle_get_system_state")
        return response

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