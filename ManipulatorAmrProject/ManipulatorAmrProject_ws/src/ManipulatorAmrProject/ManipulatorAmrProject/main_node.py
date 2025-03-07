import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped  # PoseStamped 메시지 타입 추가

import time


class TestMainNode(Node):
    def __init__(self):
        super().__init__('test_main_node')
        self.get_logger().info("TestMainNode가 시작됩니다.")

        # Publisher for main_commend
        self.main_commend_publisher = self.create_publisher(String, 'main_commend', 10)
        self.conveyor_control_publisher = self.create_publisher(String, 'conveyor_control', 10)
        self.worldcam_control_publisher = self.create_publisher(String, 'worldcam_control', 10)
        self.collect_data_control_publisher = self.create_publisher(String, 'collect_data_control', 10)

        # Subscriber for ui_commend
        self.ui_commend_subscriber = self.create_subscription(String,'ui_commend',self.ui_commend_callback,10)
        self.conveyor_commend_subscriber = self.create_subscription(String, 'conveyor_commend', self.conveyor_commend_callback, 10)
        self.worldcam_commend_subscriber = self.create_subscription(String, 'worldcam_commend', self.worldcam_commend_callback, 10)
        self.collect_commend_subscriber = self.create_subscription(String, 'collect_commend', self.collect_commend_callback, 10)

        self.turtle_pose_subscriber = self.create_subscription(PoseStamped, '/turtle_pose', self.turtle_pose_callback, 10)

        # 상태 변수 추가
        self.setup_status = {
            "conveyor_node": True,  # Conveyor Node의 SETUP 상태
            "world_camera_node": True,
            # 추가적인 노드를 여기에 추가 가능
        }

        # 상태 변수 추가
        self.estop_status = "NONE"
        self.conveyor_status = "auto"  # conveyor 상태 변수 추가
        self.active_job = None  # 현재 활성화된 작업 번호 저장
        self.job_status = "IDLE"  # 작업 상태: IDLE, RUNNING, PAUSED, STOPPED
        self.current_status = "대기 중"  # 현재 상태 메시지
        self.collecting_data = False  # 학습 데이터 수집 상태

        # 타이머 관련 변수
        self.start_time = None  # 작업 시작 시간
        self.elapsed_time = 0  # 기록된 경과 시간
        self.job_timer = None  # 타이머 객체


        self.ui_status = {
            "collect_data": {"state": "활성화", "checked": "미체크"},
            "start": {"state": "활성화", "checked": "미체크"},
            "stop": {"state": "비활성화", "checked": "미체크"},
            "reset": {"state": "활성화", "checked": "미체크"},
            "pause": {"state": "비활성화", "checked": "미체크"},
            "resume": {"state": "비활성화", "checked": "미체크"},
            "conveyor_status": {"state": "활성화", "checked": "미체크"}
        }

    def turtle_pose_callback(self, msg: PoseStamped):
        """ /turtle_pose 토픽 콜백 함수 """
        # PoseStamped 메시지에서 위치와 방향 정보를 로그로 출력
        position = msg.pose.position
        orientation = msg.pose.orientation
        self.get_logger().info(f"POS : "
    f"위치(x={position.x:.2f}, y={position.y:.2f}, z={position.z:.2f}), "
    f"방향(x={orientation.x:.2f}, y={orientation.y:.2f}, z={orientation.z:.2f}, w={orientation.w:.2f})")
        self.update_status(f"POS : "
    f"위치(x={position.x:.2f}, y={position.y:.2f}, z={position.z:.2f}), "
    f"방향(x={orientation.x:.2f}, y={orientation.y:.2f}, z={orientation.z:.2f}, w={orientation.w:.2f})")
        
    def collect_commend_callback(self, msg):
        """collect_commend 토픽 콜백."""
        self.get_logger().info(f"collect_commend에서 메시지 수신: {msg.data}")

        # start 명령에 대한 응답 처리
        if msg.data.lower() == "start":
            self.get_logger().info("collect_commend에서 start 응답을 수신했습니다.")

            # UI 상태 업데이트
            self.update_ui_status({
                "collect_data": {"state": "활성화"},
                "start": {"state": "비활성화"},
                "stop": {"state": "비활성화"},
                "pause": {"state": "비활성화"},
                "resume": {"state": "비활성화"},
                "reset": {"state": "비활성화"},
                "conveyor_status": {"state": "비활성화", "checked": "미체크"}
            })
            self.send_ui_status()

            resend_msg = String()
            resend_msg.data = "[학습데이터수집]START"
            self.main_commend_publisher.publish(resend_msg)

            # 상태 메시지 업데이트
            self.update_status("[INFO]학습 데이터 수집이 시작되었습니다.")

        # stop 명령에 대한 응답 처리
        elif msg.data.lower() == "stop":
            self.get_logger().info("collect_commend에서 stop 응답을 수신했습니다.")

            # UI 상태 업데이트
            self.update_ui_status({
                "collect_data": {"state": "활성화"},
                "start": {"state": "활성화"},
                "stop": {"state": "비활성화"},
                "pause": {"state": "비활성화"},
                "resume": {"state": "비활성화"},
                "reset": {"state": "활성화"},
                "conveyor_status": {"state": "활성화", "checked": "미체크"}
            })
            self.send_ui_status()

            resend_msg = String()
            resend_msg.data = "[학습데이터수집]STOP"
            self.main_commend_publisher.publish(resend_msg)

            # 상태 메시지 업데이트
            self.update_status("[INFO]학습 데이터 수집이 중단되었습니다.")




    def worldcam_commend_callback(self, msg):
        """worldcam_commend 토픽 콜백 함수"""
        self.get_logger().info(f"worldcam_commend에서 메시지 수신: {msg.data}")

        if msg.data == "[SETUP]":
            self.setup_status["world_camera_node"] = True
            self.get_logger().info("world_camera_node 상태가 True로 설정되었습니다.")

            if self.check_all_setup():
                self.send_setup_response()
        
        # 메시지가 [EMAIL], [INFO], [WARN]인 경우 처리
        elif "[EMAIL]" in msg.data:
            # 이메일 관련 메시지 처리
            self.update_status(msg.data)

        elif "[INFO]" in msg.data:
            # 정보 관련 메시지 처리
            self.update_status(msg.data)

        elif "[WARN]" in msg.data:
            # 경고 관련 메시지 처리
            self.update_status(msg.data)


    def conveyor_commend_callback(self, msg):
        """conveyor_commend 토픽 콜백 함수"""
        self.get_logger().info(f"conveyor_commend에서 메시지 수신: {msg.data}")

        if msg.data == "[SETUP]":
            # Conveyor Node의 SETUP 상태 업데이트
            self.setup_status["conveyor_node"] = True
            self.get_logger().info("conveyor_node 상태가 True로 설정되었습니다.")

            if self.check_all_setup():
                self.send_setup_response()

        # 메시지가 [EMAIL], [INFO], [WARN]인 경우 처리
        elif "[EMAIL]" in msg.data:
            # 이메일 관련 메시지 처리
            self.update_status(msg.data)

        elif "[INFO]" in msg.data:
            # 정보 관련 메시지 처리
            self.update_status(msg.data)

        elif "[WARN]" in msg.data:
            # 경고 관련 메시지 처리
            self.update_status(msg.data)


    def send_setup_response(self):
        """[SETUP] 메시지를 conveyor_control로 발행"""
        setup_msg = String()
        setup_msg.data = "[SETUP]"
        self.main_commend_publisher.publish(setup_msg) 
        self.conveyor_control_publisher.publish(setup_msg)  
        self.worldcam_control_publisher.publish(setup_msg)
        self.get_logger().info("모든 노드가 준비됨. [SETUP] 메시지를 conveyor_control로 발행했습니다.")

#------------------ui 콜백 처리
    def ui_commend_callback(self, msg):
        """Callback for ui_commend topic."""
        self.get_logger().info(f"ui_commend에서 수신됨: {msg.data}")


        # [학습데이터수집]START 메시지 처리
        if msg.data == "[학습데이터수집]START":
            self.get_logger().info("[학습데이터수집]START 메시지 수신.")

            self.collect_data_control_publisher.publish(String(data="start"))
            self.get_logger().info("collect_data_control로 start 메시지를 발행했습니다.")

            # UI 상태를 바로 업데이트하지 않고 응답을 기다릴 준비
            self.update_status("[INFO]학습 데이터 수집 시작 명령이 전송되었습니다.")
        
        elif msg.data == "[학습데이터수집]STOP":
            self.get_logger().info("[학습데이터수집]STOP 메시지 수신.")

            # collect_data_control로 stop 메시지 전송
            self.collect_data_control_publisher.publish(String(data="stop"))
            self.get_logger().info("collect_data_control로 stop 메시지를 발행했습니다.")

            # UI 상태를 바로 업데이트하지 않고 응답을 기다릴 준비
            self.update_status("[INFO]학습 데이터 수집 중단 명령이 전송되었습니다.")

        elif msg.data.startswith("[JOB]"):
            command = msg.data[len("[JOB]"):].strip()  # [JOB] 뒤의 명령어 추출
            self.get_logger().info(f"[JOB] 명령어 수신: {command}")

            if command.startswith("JOB"):  # 예: [JOB]JOB3
                self.start_new_job(command)
            elif command == "STOP":
                self.stop_job()
            elif command == "PAUSE":
                self.pause_job()
            elif command == "RESUME":
                self.resume_job()
            elif command == "RESET":
                self.reset_job()

        # [ESTOP] 메시지 처리
        elif msg.data == "[ESTOP]STOP":
            self.estop_status = "STOP"
            self.get_logger().info(f"estop_status가 {self.estop_status}로 설정되었습니다.")
            self.handle_estop_stop()

            # [ESTOP]STOP 메시지 재발행
            resend_msg = String()
            resend_msg.data = "[ESTOP]STOP"
            self.main_commend_publisher.publish(resend_msg)
            self.get_logger().info(f"main_commend로 [ESTOP]STOP 메시지가 발행되었습니다.")
            self.update_status("[EMAIL][WARN]비상 정지 버튼이 작동 되었습니다")  # 상태 업데이트

            # collect_data_control로 stop 메시지 전송
            self.collect_data_control_publisher.publish(String(data="stop"))
            self.get_logger().info("collect_data_control로 stop 메시지를 발행했습니다.")
        
        # [ESTOP]NONE 메시지 처리
        elif msg.data == "[ESTOP]NONE":
            self.estop_status = "NONE"
            self.get_logger().info(f"estop_status가 {self.estop_status}로 설정되었습니다.")
            self.handle_estop_none()

            # [ESTOP]NONE 메시지 발행
            resend_msg = String()
            resend_msg.data = "[ESTOP]NONE"
            self.main_commend_publisher.publish(resend_msg)
            self.get_logger().info(f"main_commend로 [ESTOP]NONE 메시지가 발행되었습니다.")

            # [UI_STATUS] 메시지 발행
            self.send_ui_status()

            self.update_status("[EMAIL][INFO]비상 정지 버튼이 복구 되었습니다")  # 상태 업데이트

        # [CONVEYOR]auto 메시지 처리
        elif msg.data == "[CONVEYOR]auto":
            self.conveyor_status = "auto"
            self.update_status("[INFO]컨베이어의 작동 모드가 \"AUTO\"로 변경 되었습니다.")  # 상태 업데이트
            self.get_logger().info(f"conveyor_status가 {self.conveyor_status}로 설정되었습니다.")

        # [CONVEYOR]manual 메시지 처리
        elif msg.data == "[CONVEYOR]manual":
            self.conveyor_status = "manual"
            self.update_status("[INFO]컨베이어의 작동 모드가 \"MANUAL\"로 변경 되었습니다.")  # 상태 업데이트
            self.get_logger().info(f"conveyor_status가 {self.conveyor_status}로 설정되었습니다.")

        # [CONVEYOR]MOVE 메시지 처리
        elif msg.data == "[CONVEYOR]MOVE":
            self.get_logger().info("[CONVEYOR]MOVE 메시지 수신.")
            self.publish_conveyor_command("MOVE")

        # [CONVEYOR]STOP 메시지 처리
        elif msg.data == "[CONVEYOR]STOP":
            self.get_logger().info("[CONVEYOR]STOP 메시지 수신.")
            self.publish_conveyor_command("STOP")

        # 다른 메시지 처리
        elif msg.data.startswith("[SETUP]"):
            self.get_logger().info("[SETUP] 요청 수신")

            # 모든 SETUP 상태가 True인지 확인
            if self.check_all_setup():
                self.send_ui_status()
            else:
                self.get_logger().warning("[SETUP] 요청에 대해 응답하지 않음. 모든 노드가 준비되지 않음.")

        else:
            self.get_logger().info(f"알 수 없는 메시지: {msg.data}")


    def check_all_setup(self):
        """모든 노드의 SETUP 상태가 True인지 확인"""
        return all(self.setup_status.values())


#------------------ui 콜백 처리
    """ESTOP 상태가 STOP일 때 처리."""
    def handle_estop_stop(self):
        self.get_logger().info("ESTOP 상태가 STOP으로 설정되었습니다. 모든 작업 초기화 중.")

        # 모든 작업 상태 초기화
        if self.job_timer:
            self.job_timer.cancel()
            self.job_timer = None

        self.start_time = None
        self.elapsed_time = 0
        self.job_status = "IDLE"

        # UI 상태 업데이트
        self.update_ui_status({
            "collect_data": {"state": "활성화"},
            "start": {"state": "활성화"},
            "stop": {"state": "비활성화"},
            "pause": {"state": "비활성화"},
            "resume": {"state": "비활성화"},
            "reset": {"state": "활성화"}
        })

        # ESTOP 상태에 따른 초기화 메시지 발행
        reset_msg = String()
        reset_msg.data = "[JOB]RESET"
        self.main_commend_publisher.publish(reset_msg)
        self.get_logger().info(f"작업 초기화 메시지 발행: {reset_msg.data}")

        # 00:00:00 시간 메시지 발행
        zero_time_msg = String()
        zero_time_msg.data = "[JOB]time=00:00:00"
        self.main_commend_publisher.publish(zero_time_msg)
        self.get_logger().info(f"초기화된 시간 메시지 발행: {zero_time_msg.data}")

        self.send_ui_status()

    """ESTOP 상태가 NONE일 때 처리."""
    def handle_estop_none(self):
        """ESTOP 상태가 NONE일 때 처리."""
        self.get_logger().info("ESTOP 상태가 NONE으로 설정되었습니다. 대기 상태로 복귀.")
        # ESTOP 해제 후 작업을 재개하지 않고 초기 상태로 유지
        self.job_status = "IDLE"
        self.start_time = None
        self.elapsed_time = 0

        # UI 상태 업데이트
        self.update_ui_status({
            "collect_data": {"state": "활성화"},
            "start": {"state": "활성화"},
            "stop": {"state": "비활성화"},
            "pause": {"state": "비활성화"},
            "resume": {"state": "비활성화"},
            "reset": {"state": "활성화"},
            "conveyor_status": {"state": "활성화", "checked": "미체크"}
        })

        self.send_ui_status()

    """새로운 작업을 시작합니다."""
    def start_new_job(self, job_number):
        self.get_logger().info(f"새 작업 시작: {job_number}")

        # 작업 초기화 및 시작
        self.start_time = time.time()  # 작업 시작 시간 기록
        self.elapsed_time = 0  # 경과 시간 초기화
        self.job_status = "RUNNING"

        # 기존 타이머가 있으면 취소
        if self.job_timer:
            self.job_timer.cancel()

        # 새 타이머 시작
        self.job_timer = self.create_timer(1.0, self.publish_elapsed_time)

        # UI 상태 업데이트
        self.update_ui_status({
            "collect_data": {"state": "비활성화"},
            "start": {"state": "비활성화"},
            "stop": {"state": "활성화"},
            "pause": {"state": "활성화"},
            "resume": {"state": "비활성화"},
            "reset": {"state": "활성화"}
        })

        # 작업 시작 메시지 재발행
        msg = String()
        msg.data = f"[JOB]{job_number} started"
        self.main_commend_publisher.publish(msg)
        self.get_logger().info(f"작업 시작 메시지 발행: {msg.data}")

        self.update_status("[INFO]JOB이 시작 되었습니다")  # 상태 업데이트

        self.send_ui_status()

    """현재 작업을 중지합니다."""
    def stop_job(self):
        self.get_logger().info(f"작업 중지: {self.active_job}")

        # 타이머 취소
        if self.job_timer:
            self.job_timer.cancel()
            self.job_timer = None

        # 작업 상태 업데이트
        self.job_status = "STOPPED"
        elapsed_time = self.calculate_elapsed_time()

        # UI 상태 업데이트
        self.update_ui_status({
            "collect_data": {"state": "활성화"},
            "start": {"state": "활성화"},
            "stop": {"state": "비활성화"},
            "pause": {"state": "비활성화"},
            "resume": {"state": "비활성화"},
            "reset": {"state": "활성화"}
        })

        # 작업 종료 메시지 재발행
        msg = String()
        msg.data = f"[JOB]STOP time={elapsed_time}"
        self.main_commend_publisher.publish(msg)
        self.get_logger().info(f"작업 종료 메시지 발행: {msg.data}")

        self.update_status("[INFO]JOB이 중지 되었습니다")  # 상태 업데이트

        self.start_time = None
        self.elapsed_time = 0

        self.send_ui_status()

        # 상태 초기화
        self.active_job = None
        self.start_time = None

    """현재 작업을 일시 정지합니다."""
    def pause_job(self):
        if self.job_status != "RUNNING":
            self.get_logger().warning("작업이 실행 중이 아니므로 일시 정지할 수 없습니다.")
            return
        
        self.get_logger().info("작업 일시 정지")

        # 현재까지의 경과 시간 기록
        self.elapsed_time += time.time() - self.start_time
        self.start_time = None  # 일시 정지 동안 작업 시작 시간 초기화
        self.job_status = "PAUSED"

        # 타이머 취소
        if self.job_timer:
            self.job_timer.cancel()

        # UI 상태 업데이트
        self.update_ui_status({
            "start": {"state": "비활성화"},
            "stop": {"state": "활성화"},
            "pause": {"state": "비활성화"},
            "resume": {"state": "활성화"},
            "reset": {"state": "활성화"}
        })

        # 작업 일시 정지 메시지 재발행
        msg = String()
        msg.data = "[JOB]PAUSED"
        self.main_commend_publisher.publish(msg)
        self.get_logger().info(f"작업 일시 정지 메시지 발행: {msg.data}")

        self.update_status("[INFO]JOB이 일시정지 되었습니다")  # 상태 업데이트

        self.send_ui_status()

    """일시 정지된 작업을 재개합니다."""
    def resume_job(self):
        if self.job_status != "PAUSED":
            self.get_logger().warning("작업이 일시 정지 상태가 아니므로 재개할 수 없습니다.")
            return

        self.get_logger().info(f"작업 재개: {self.active_job}")

        # 재개하면서 작업 시작 시간 기록
        self.start_time = time.time()
        self.job_status = "RUNNING"

        # 타이머 재시작
        self.job_timer = self.create_timer(1.0, self.publish_elapsed_time)

        # UI 상태 업데이트
        self.update_ui_status({
            "collect_data": {"state": "비활성화"},
            "start": {"state": "비활성화"},
            "stop": {"state": "활성화"},
            "pause": {"state": "활성화"},
            "resume": {"state": "비활성화"},
            "reset": {"state": "활성화"}
        })

        # 작업 재개 메시지 재발행
        msg = String()
        msg.data = "[JOB]RESUMED"
        self.main_commend_publisher.publish(msg)
        self.get_logger().info(f"작업 재개 메시지 발행: {msg.data}")

        self.update_status("[INFO]JOB이 재개 되었습니다")  # 상태 업데이트

        self.send_ui_status()

    """현재 작업을 초기화합니다."""
    def reset_job(self):
        self.get_logger().info(f"작업 초기화: {self.active_job}")

        # 타이머 취소
        if self.job_timer:
            self.job_timer.cancel()
            self.job_timer = None

        self.start_time = None
        self.elapsed_time = 0
        self.job_status = "IDLE"

        # UI 상태 업데이트
        self.update_ui_status({
            "collect_data": {"state": "활성화"},
            "start": {"state": "활성화"},
            "stop": {"state": "비활성화"},
            "pause": {"state": "비활성화"},
            "resume": {"state": "비활성화"},
            "reset": {"state": "활성화"}
        })

        # 작업 초기화 메시지 재발행
        msg = String()
        msg.data = "[JOB]RESET"
        self.main_commend_publisher.publish(msg)
        self.get_logger().info(f"작업 초기화 메시지 발행: {msg.data}")

        self.update_status("[INFO]JOB이 초기화 되었습니다")  # 상태 업데이트

        # 00:00:00 시간 메시지 발행
        zero_time_msg = String()
        zero_time_msg.data = "[JOB]time=00:00:00"
        self.main_commend_publisher.publish(zero_time_msg)
        self.get_logger().info(f"초기화된 시간 메시지 발행: {zero_time_msg.data}")

        self.send_ui_status()

    """경과 시간을 계산하고 발행합니다."""
    def publish_elapsed_time(self):
        elapsed_time = self.calculate_elapsed_time()
        msg = String()
        msg.data = f"[JOB]time={elapsed_time}"
        self.main_commend_publisher.publish(msg)
        self.get_logger().info(f"경과 시간 발행: {msg.data}")

    """경과 시간을 계산하여 반환합니다."""
    def calculate_elapsed_time(self):
        if self.job_status == "RUNNING" and self.start_time:
            current_elapsed = time.time() - self.start_time
            total_elapsed = self.elapsed_time + current_elapsed
        else:
            total_elapsed = self.elapsed_time

        hours, remainder = divmod(int(total_elapsed), 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"

   

#------------------main > ui    메세지 처리
    def send_ui_status(self):
        """
        현재 UI 상태를 ROS 메시지로 발행합니다.
        """
        status_message = ', '.join(
            [f"({key}, {value['state']}, {value['checked']})" for key, value in self.ui_status.items()]
        )
        message = f"[UI_STATUS] {status_message}"
        #self.get_logger().info(f"발행할 [UI_STATUS] 메시지: {message}")

        # ROS 메시지 발행
        msg = String()
        msg.data = message
        self.main_commend_publisher.publish(msg)

    """현재 상태를 업데이트하고 [STATUS] 메시지를 발행합니다."""
    def update_status(self, new_status):
        if self.current_status != new_status:
            self.current_status = new_status
            status_msg = String()
            status_msg.data = f"[STATUS]{new_status}"
            self.main_commend_publisher.publish(status_msg)
            self.get_logger().info(f"상태 업데이트: {status_msg.data}")
#------------------main > ui    메세지 처리


#------------------main_order 처리 함수
    def publish_conveyor_command(self, command):
        """
        특정 조건에 따라 main_order 토픽에 메시지를 발행.
        :param command: str - 'move1', 'move2', 'move', 'STOP' 등의 명령
        """
        if self.conveyor_status == "auto":
            if command == "move1":
                message = "[CONVEYOR]500"
                status_msg = String()
                status_msg.data = "[STATUS][INFO]컨베이어 자동 동작 중"
                self.main_commend_publisher.publish(status_msg)
                self.get_logger().info(f"main_commend로 {status_msg.data} 메시지가 발행되었습니다.")
            elif command == "move2":
                message = "[CONVEYOR]2000"
                status_msg = String()
                status_msg.data = "[STATUS]컨베이어 자동 동작 중"
                self.main_commend_publisher.publish(status_msg)
                self.get_logger().info(f"main_commend로 {status_msg.data} 메시지가 발행되었습니다.")
            else:
                self.get_logger().error("auto 상태에서는 move1 또는 move2만 사용할 수 있습니다.")
                return
        elif self.conveyor_status == "manual":
            if command == "MOVE":
                message = "[CONVEYOR]10000"
                status_msg = String()
                status_msg.data = "[STATUS][INFO]컨베이어 수동 조작 중"
                self.main_commend_publisher.publish(status_msg)
                self.get_logger().info(f"main_commend로 {status_msg.data} 메시지가 발행되었습니다.")
            elif command == "STOP":
                message = "[CONVEYOR]1"
                status_msg = String()
                status_msg.data = "[STATUS][INFO]컨베이어가 정지 했습니다"
                self.main_commend_publisher.publish(status_msg)
                self.get_logger().info(f"main_commend로 {status_msg.data} 메시지가 발행되었습니다.")
            else:
                self.get_logger().error("manual 상태에서는 move 또는 STOP만 사용할 수 있습니다.")
                return
        else:
            self.get_logger().error("conveyor_status가 설정되지 않았습니다.")
            return

        # 메시지 발행
        msg = String()
        msg.data = message
        self.conveyor_control_publisher.publish(msg)
        self.get_logger().info(f"conveyor_control로 {message} 메시지가 발행되었습니다.")

#------------------main_order 처리 함수 끝
    def update_ui_status(self, updates):
        """
        UI 상태를 업데이트합니다.
        :param updates: dict - 업데이트할 UI 상태의 딕셔너리. {key: {"state": state, "checked": checked}}
        """
        self.get_logger().info(f"updates 데이터: {updates}")
        # self.get_logger().info(f"기존 ui_status: {self.ui_status}")

        for key, value in updates.items():
            self.get_logger().info(f"key: {key}, value: {value}")  # 루프 내부로 이동
            if key in self.ui_status:
                if isinstance(self.ui_status[key], dict):
                    # self.get_logger().info(f"업데이트 전 상태 ({key}): {self.ui_status[key]}")
                    self.ui_status[key].update(value)
                    # self.get_logger().info(f"업데이트 후 상태 ({key}): {self.ui_status[key]}")
                else:
                    self.get_logger().error(f"{key}는 딕셔너리가 아닙니다: {self.ui_status[key]}")
            else:
                self.get_logger().warning(f"{key}는 ui_status에 존재하지 않습니다.")
        
        self.get_logger().info(f"최종 업데이트된 ui_status: {self.ui_status}")




def main(args=None):
    rclpy.init(args=args)
    node = TestMainNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("TestMainNode가 종료됩니다.")
    finally:
        rclpy.shutdown()


if __name__ == "__main__":
    main()
