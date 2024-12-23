import socket
import threading
import rclpy
import DR_init
import queue
import time

# for single robot
ROBOT_ID = "dsr01"
ROBOT_MODEL = "m0609"
VELOCITY, ACC = 60, 60

DR_init.__dsr__id = ROBOT_ID
DR_init.__dsr__model = ROBOT_MODEL

# 명령 큐
command_queue = queue.Queue()

# 소켓 연결 객체 및 잠금
conn_lock = threading.Lock()
connections = []

def notify_clients(message: str):
    """모든 클라이언트에 메시지 전송"""
    with conn_lock:
        for conn in connections:
            try:
                conn.sendall(message.encode())
                print(f"Sent '{message}' to client.")
            except BrokenPipeError:
                print("Broken pipe when sending message to a client.")
            except Exception as e:
                print(f"Error sending message: {e}")

def robot_control_thread():
    """로봇 제어 스레드"""
    rclpy.init()
    node = rclpy.create_node("grip_simple", namespace=ROBOT_ID)
    DR_init.__dsr__node = node

    try:
        from DSR_ROBOT2 import (
            set_digital_output,
            get_digital_input,
            set_tool,
            set_tcp,
            movej,
            movel,
            get_current_posx,
            DR_BASE,
            wait,
        )
        from DR_common2 import posx
    except ImportError as e:
        print(f"Error importing DSR_ROBOT2 : {e}")
        return

    # 플래그
    arrived_signal_received = False
    ungrip_signal_received = False

    # 그리퍼 조작 함수
    ON, OFF = 1, 0

    def wait_digital_input(sig_num,node):
        """디지털 입력 신호를 기다리는 함수"""
        while not get_digital_input(sig_num):
            time.sleep(0.5)
            print("Waiting for digital input...")

    def release(node):
        """그리퍼 열기"""
        set_digital_output(2, ON)
        set_digital_output(1, OFF)
        # wait_digital_input(2,node)

    def grip(node):
        """그리퍼 닫기"""
        set_digital_output(1, ON)
        set_digital_output(2, OFF)
        # wait_digital_input(1,node)

    # 초기 설정
    set_tool("Tool Weight_2FG")
    set_tcp("2FG_TCP")

    # 초기, 미팅, 타겟 포지션
    JReady = [0, 0, 90, 0, 90, 0]
    meeting_position = [4.11, -27.88, -47.94, -15.47, -14.42, 106.06]
    target_position = (449.09, 50.19)

    # 여기서부터는 기존 main 함수의 로직을 소켓 명령으로 수행
    # 1. 시작 시 초기 위치로 이동 및 그리퍼 닫기
    node.get_logger().info("초기 위치로 이동 중...")
    movej(JReady, vel=VELOCITY, acc=ACC)
    grip(node)

    # 여기서 arrived_signal을 기다림
    # 기존엔 토픽이었지만 이제는 소켓 명령으로 "arrived"를 받을 때까지 대기
    # 이후 메인 루프에서 command_queue 확인

    # 로봇 제어 명령 처리 루프
    while rclpy.ok():
        try:
            command = command_queue.get(timeout=0.1)
        except queue.Empty:
            command = None

        if command == "start":
            # start 명령 처리 
            node.get_logger().info("미팅 포지션으로 이동 중...")
            movej(meeting_position, vel=VELOCITY, acc=ACC)
            notify_clients("start done")

        elif command == "arrived":
            # arrived 명령 처리
            arrived_signal_received = True
            node.get_logger().info("Arrived 신호 수신. 그리퍼를 오픈합니다.")
            release(node)

            # 막대를 받기 위해 위치로 이동
            current_pos = get_current_posx()
            movel(posx([current_pos[0][0] - 50, current_pos[0][1], current_pos[0][2],
                        current_pos[0][3], current_pos[0][4], current_pos[0][5]]),
                  vel=VELOCITY, acc=ACC, ref=DR_BASE)
            grip(node)

            # grip_completed 신호를 소켓으로 전송
            wait(1)
            notify_clients("grip_completed")

        elif command == "ungrip":
            # ungrip 명령 처리
            ungrip_signal_received = True
            node.get_logger().info("Ungrip 신호 수신. 초기 위치로 복귀 후 목표 지점으로 이동.")
            movej(JReady, vel=VELOCITY, acc=ACC)

            # 타겟 위치로 이동
            node.get_logger().info("타겟 위치로 이동 중...")
            movel(posx([target_position[0], target_position[1], 90, 20.75, 179.00, 19.09]), vel=VELOCITY, acc=ACC)
            movel(posx([target_position[0], target_position[1], 40, 20.75, 179.00, 19.09]), vel=VELOCITY, acc=ACC)
            release(node)

            node.get_logger().info("블록을 타겟 위치에 위치시켰습니다. 초기 위치로 돌아갑니다.")
            movej(JReady, vel=VELOCITY, acc=ACC)

        elif command:
            print(f"Unknown command: {command}")

        # 여기에 꼭 매번 movej([0,0,0,0,0,0])를 호출할 필요는 없음
        # 특정 명령 수행 후 원위치로 돌아가는 정도로 조정

    rclpy.shutdown()


def handle_client(conn, addr):
    """클라이언트 연결 핸들러"""
    global connections
    print(f"{addr} 로부터 연결이 되었습니다!")
    with conn_lock:
        connections.append(conn)
    try:
        while True:
            client_message = conn.recv(1024).decode()
            if not client_message or client_message.lower() == "bye":
                print(f"Client {addr}가 연결을 종료하였습니다.")
                break

            print(f"Client {addr}: {client_message}")
            # 명령 큐에 추가
            command_queue.put(client_message.lower())
    except ConnectionResetError:
        print(f"클라이언트 {addr}에 의해 연결이 리셋되었습니다.")
    except Exception as e:
        print(f"{addr}로부터 메시지 수신 중 오류 발생: {e}")
    finally:
        with conn_lock:
            connections.remove(conn)
        conn.close()
        print(f"{addr}와의 연결이 종료되었습니다.")


def socket_server_thread():
    """소켓 서버 스레드"""
    host = "0.0.0.0"
    port = 12346

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen()
    print(f"소켓 서버가{host}:{port}에서 대기중입니다...")

    try:
        while True:
            conn, addr = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            client_thread.start()
    except Exception as e:
        print(f"서버 오류 발생: {e}")
    finally:
        server_socket.close()
        print("소켓 서버가 종료되었습니다.")


if __name__ == "__main__":
    try:
        # 소켓 서버 스레드 시작
        server_thread = threading.Thread(target=socket_server_thread, daemon=True)
        server_thread.start()

        # 로봇 제어 스레드 시작
        robot_thread = threading.Thread(target=robot_control_thread, daemon=True)
        robot_thread.start()

        server_thread.join()
        robot_thread.join()

    except KeyboardInterrupt:
        print("Shutting down...")
