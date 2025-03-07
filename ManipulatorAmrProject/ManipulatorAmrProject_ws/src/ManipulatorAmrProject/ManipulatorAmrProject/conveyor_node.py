import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import serial
import threading
import time


class ConveyorNode(Node):
    def __init__(self):
        super().__init__('conveyor_node')
        self.get_logger().info("Conveyor Node가 시작되었습니다.")

        # Publisherconveyor_commend
        self.conveyor_commend_publisher = self.create_publisher(String, 'conveyor_commend', 10)
        self.get_logger().info(" 토픽 퍼블리셔 생성 완료")

        # Subscriber
        self.conveyor_control_subscriber = self.create_subscription(
            String, 'conveyor_control', self.conveyor_control_callback, 10
        )

        # 상태 변수
        self.arduino_port = None
        self.baudrate = 115200
        self.current_port_index = 0
        self.max_port_index = 15
        self.is_connected = False  # 현재 연결 상태
        self.setup_received = False  # [SETUP] 메시지 응답 여부
        self.running = True  # 스레드 동작 플래그

        # 스레드로 연결 및 [SETUP] 관리
        self.connection_thread = threading.Thread(target=self.connection_worker, daemon=True)
        self.connection_thread.start()

        self.setup_thread = threading.Thread(target=self.setup_message_worker, daemon=True)
        self.setup_thread.start()

    def connection_worker(self):
        """컨베이어 연결 상태 확인 및 연결 관리"""
        while self.running:
            if not self.arduino_port or not self.arduino_port.is_open:
                self.find_and_connect_arduino()
            else:
                try:
                    # 연결 상태 확인
                    self.arduino_port.write(b'\n')
                    time.sleep(0.1)
                except serial.SerialException:
                    self.handle_disconnection()
            time.sleep(0.2)

    def setup_message_worker(self):
        """[SETUP] 메시지 전송 관리"""
        while self.running:
            if self.is_connected and not self.setup_received:
                self.send_setup_message()
            time.sleep(0.5)

    def send_setup_message(self):
        """[SETUP] 메시지를 conveyor_commend 토픽으로 퍼블리시"""
        setup_msg = String()
        setup_msg.data = "[SETUP]"
        self.conveyor_commend_publisher.publish(setup_msg)
        self.get_logger().info("[SETUP] 메시지를 conveyor_commend로 퍼블리시했습니다.")

    def handle_disconnection(self):
        """연결이 끊어졌을 때 처리"""
        if self.is_connected:
            self.is_connected = False
            self.setup_received = False
            self.get_logger().warning("컨베이어와 연결이 끊어졌습니다.")
            self.publish_log_message("[EMAIL][WARN] 컨베이어와 연결이 끊어졌습니다.")
        self.arduino_port = None

    def find_and_connect_arduino(self):
        """포트 범위 내에서 순차적으로 연결 시도"""
        target_port = f"/dev/ttyACM{self.current_port_index}"
        self.get_logger().info(f"포트 시도: {target_port}")

        try:
            ser = serial.Serial(target_port, baudrate=self.baudrate, timeout=2)
            time.sleep(2)  # 포트 초기화 시간
            self.get_logger().info(f"포트 {target_port} 연결 성공")
            self.arduino_port = ser

            if not self.is_connected:  # 새로 연결된 경우
                self.is_connected = True
                self.get_logger().info("컨베이어와 연결 되었습니다.")
                self.publish_log_message("[INFO] 컨베이어와 연결 되었습니다.")
        except serial.SerialException as e:
            self.get_logger().error(f"포트 {target_port} 연결 실패 (SerialException): {e}")
        except Exception as e:
            self.get_logger().error(f"포트 {target_port} 연결 실패: {e}")

        # 다음 포트로 이동
        self.current_port_index = (self.current_port_index + 1) % (self.max_port_index + 1)

    def conveyor_control_callback(self, msg):
        """conveyor_control 토픽 콜백"""
        self.get_logger().info(f"conveyor_control에서 메시지 수신: {msg.data}")
        if msg.data == "[SETUP]":
            self.get_logger().info("[SETUP] 메시지를 conveyor_control에서 수신했습니다.")
            self.setup_received = True
        elif msg.data.startswith("[CONVEYOR]"):
            value_str = msg.data[len("[CONVEYOR]"):].strip()
            if value_str.isdigit():
                self.send_conveyor_command(int(value_str))
            else:
                self.get_logger().warning("[CONVEYOR] 뒤에 유효한 숫자가 없습니다.")

    def send_conveyor_command(self, value):
        """숫자를 시리얼 포트로 전송"""
        if self.arduino_port and self.arduino_port.is_open:
            command = f"{value}\n"
            try:
                self.arduino_port.write(command.encode('utf-8'))
                self.get_logger().info(f"[CONVEYOR] 명령 {value}을(를) 시리얼로 전송했습니다.")
            except Exception as e:
                self.get_logger().error(f"[CONVEYOR] 명령 전송 실패: {e}")
        else:
            self.get_logger().warning("아두이노 포트가 연결되지 않았거나 닫혀있습니다.")

    def publish_log_message(self, message):
        """로그 메시지 퍼블리시"""
        msg = String()
        msg.data = message
        self.conveyor_commend_publisher.publish(msg)
        self.get_logger().info(f"로그 메시지 발행: {message}")

    def destroy_node(self):
        """노드 종료 시 스레드 종료"""
        self.running = False
        if self.arduino_port:
            self.arduino_port.close()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = ConveyorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Conveyor Node가 종료됩니다.")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
