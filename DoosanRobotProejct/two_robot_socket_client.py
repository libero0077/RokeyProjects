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

ON, OFF = 1, 0



# 로봇 제어 명령 큐
command_queue = queue.Queue()

def robot_control_thread(socket_client_thread):
    """로봇 제어 스레드"""
    rclpy.init()
    node = rclpy.create_node("robot_control", namespace=ROBOT_ID)

    DR_init.__dsr__node = node

    try:
        from DSR_ROBOT2 import (
            movej,
            movel,
            set_digital_output,
            get_digital_input,
            task_compliance_ctrl,
            set_desired_force,
            check_force_condition,
            release_compliance_ctrl,
            DR_AXIS_Z,
            DR_FC_MOD_REL,
            DR_MV_MOD_REL,
        )
        from DR_common2 import posx, posj

    except ImportError as e:
        print(f"Error importing DSR_ROBOT2 : {e}")
        return

    def movej1():
        print("Executing movej1...")
        movej([0, 0, 90, 0, 90, 0], vel=VELOCITY, acc=ACC)
        print("movej1 executed.")

    def movej2():
        print("Executing movej2...")
        JReady = posx([500.0, 160.0, 320.0, 95.0, -160.0, -75.0])
        movel(JReady, vel=VELOCITY, acc=ACC)
        print("movej2 executed.")
        grip()


    def release():
        set_digital_output(2, ON)
        set_digital_output(1, OFF)

    def grip():
        release()
        set_digital_output(1, ON)
        set_digital_output(2, OFF)

     # 로봇 초기 위치
    JReady = [0, 0, 90, 0, 90, 0]
    JEnd = [0, 0, 90, 0, 90, -90]
    movej(JReady, vel=VELOCITY, acc=ACC)

    pick = posx([350.362, 46.717, 72.676, 26.444, -179.994, 29.467])
    down = posx([0, 0, -25, 0, 0, 0])
    up = posx([0, 0, 30, 0, 0, 0])
    place = posx([939.943, -13.568, 590.571, 175.569, -89.781, 89.969])
    release()

    movel(pick, vel=VELOCITY, acc=ACC)
    grip()
    task_compliance_ctrl(stx=[500, 500, 500, 100, 100, 100])
    set_desired_force(fd=[0, 0, -10, 0, 0, 0], dir=[0, 0, 1, 0, 0, 0], mod=DR_FC_MOD_REL)
    while not check_force_condition(DR_AXIS_Z, max=5):
            pass
    release_compliance_ctrl()
    
    release()
    movel(down, vel=VELOCITY, acc=ACC, mod=DR_MV_MOD_REL)  
    grip()
    time.sleep(0.5)
    
    movel(up, vel=VELOCITY, acc=ACC, mod=DR_MV_MOD_REL)
    movel(place, vel=150, acc=150)
    
    socket_client_thread.send_message("start")
    print("start를 보냄")

    while rclpy.ok():
        try:
            command = command_queue.get(timeout=0.1)
        except queue.Empty:
            continue

        if command == "start done":
            socket_client_thread.send_message("arrived")
            print("arrived를 보냄")
            
        elif command == "grip_completed":
            release()
            socket_client_thread.send_message("ungrip")
            print("ungrip을 보냄")
            movej(JEnd, vel=VELOCITY, acc=ACC)

        rclpy.spin_once(node, timeout_sec=0.1)

    rclpy.shutdown()

class SocketClientThread:
    def __init__(self):
        self.host = "192.168.10.39"  # 서버 IP 주소
        self.port = 12346  # 서버 포트 번호
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((self.host, self.port))
            print(f"서버 {self.host}:{self.port}에 연결되었습니다.")
        except ConnectionRefusedError:
            print("서버에 연결할 수 없습니다. 서버가 실행 중인지 확인하세요.")
        except Exception as e:
            print(f"연결 중 오류 발생: {e}")

    def send_message(self, message):
        try:
            self.client_socket.send(message.encode())
        except Exception as e:
            print(f"메시지 전송 오류: {e}")

    def run(self):
        try:
            #self.send_message("start")
            response = self.client_socket.recv(1024).decode()

            if response.strip().lower() == "start done":
                print("서버로부터 'start done' 수신")
                self.send_message("arrived")

            while True:
                response = self.client_socket.recv(1024).decode()

                if not response:
                    print("서버로부터 연결이 종료되었습니다.")
                    break

                print(f"서버로부터 받은 명령: {response}")
                command_queue.put(response.strip().lower())

        except KeyboardInterrupt:
            print("\n클라이언트 종료 중...")
        except ConnectionResetError:
            print("서버와의 연결이 끊어졌습니다.")
        except Exception as e:
            print(f"클라이언트 오류: {e}")
        finally:
            self.client_socket.close()
            print("소켓 연결이 닫혔습니다.")


def main():
    try:
        client_thread = SocketClientThread()  # 소켓 클라이언트 스레드 인스턴스 먼저 생성
        robot_thread = threading.Thread(target=robot_control_thread, args=(client_thread,), daemon=True)
        robot_thread.start()

        client_thread_thread = threading.Thread(target=client_thread.run, daemon=True)
        client_thread_thread.start()

        robot_thread.join()
        client_thread_thread.join()

    except KeyboardInterrupt:
        print("프로그램 종료 중...")

if __name__ == "__main__":
    main()
