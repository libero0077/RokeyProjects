'''
Start position 

1 (위)     : 309.38, -75.64, 56.35, 154.05, 179.66, 153.9
2 (오른쪽)  : 377.72, -152.91, 56.32, 115.32, 179.81, 115.11 
3 (왼쪽)   : 276, -176.55, 56.26, 146.89, 179.94, 146.88
4 (가운데)  : 320.54, -133.35, 56.23, 145.74, 179.46, 145.69 

            O
            O
         O     O


Target position 

1 (오른쪽 위)     : 586.51, -104.48, 39.68, 149.04, 178.54, 149.12
2 (왼쪽 위)  :  482.32, -111.68, 39.29, 152.42, 178.41, 152.41
3 (아래)   : 540.76, -198.67, 39.6, 135.7, 178.01, 136.27
4 (가운데)  : 536.58, -139.42, 40.68, 130.51, 179.27, 129.92

          O             O 
       	      O
       	      
       	      O
'''

import rclpy
import DR_init
import time
import threading  # 추가 필요

# for single robot
ROBOT_ID = "dsr01"
ROBOT_MODEL = "m0609"
VELOCITY, ACC = 60, 60

DR_init.__dsr__id = ROBOT_ID
DR_init.__dsr__model = ROBOT_MODEL

# 그리퍼 상태
ON, OFF = 1, 0

def main(args=None):
    rclpy.init(args=args)
    node = rclpy.create_node("force_control", namespace=ROBOT_ID)
    DR_init.__dsr__node = node

    try:
        from DSR_ROBOT2 import (
            release_compliance_ctrl,
            check_force_condition,
            task_compliance_ctrl,
            set_desired_force,
            set_tool,
            set_tcp,
            movej,
            movel,
            get_current_posx,
            DR_FC_MOD_REL,
            DR_AXIS_Z,
            DR_BASE,
            DR_TOOL, # 그리퍼 관련
            get_digital_input, # 그리퍼 관련
            set_digital_output, # 그리퍼 관련
            move_periodic,
            amovel,
            amove_periodic,
            DR_QSTOP, # periodic 관련
            get_tool_force,

        )

        from DR_common2 import posx

    except ImportError as e:
        print(f"Error importing DSR_ROBOT2 : {e}")
        return

    # 기어 좌표
    '''
    1 (위)     : 309.38, -75.64, 56.35, 154.05, 179.66, 153.9
    2 (오른쪽)  : 377.72, -152.91, 56.32, 115.32, 179.81, 115.11 
    3 (왼쪽)   : 276, -176.55, 56.26, 146.89, 179.94, 146.88
    4 (가운데)  : 320.54, -133.35, 56.23, 145.74, 179.46, 145.69
    '''
    start_positions = [
        (309.38, -75.64, 56.35, 154.05, 179.66, 153.9), 
        (377.72, -152.91, 56.32, 115.32, 179.81, 115.11 ), 
        (276, -176.55, 56.26, 146.89, 179.94, 146.886),
        (320.54, -133.35, 56.23, 145.74, 179.46, 145.69 )
    ]

    # 타겟 좌표
    '''
    1 (오른쪽 위)     : 586.51, -104.48, 39.68, 149.04, 178.54, 149.12
    2 (왼쪽 위)  :  482.32, -111.68, 39.29, 152.42, 178.41, 152.41
    3 (아래)   : 540.76, -198.67, 39.6, 135.7, 178.01, 136.27
    4 (가운데)  : 536.58, -139.42, 40.68, 130.51, 179.27, 129.92
    '''

    target_positions = [
        (586.51, -104.48, 39.68, 149.04, 178.54, 149.12), 
        (482.32, -111.68, 39.29, 152.42, 178.41, 152.41), 
        (544.17, -198.19, 39.6, 135.7, 178.01, 136.27),
        (536.58, -139.42, 40.68, 130.51, 179.27, 129.92)
    ]

    # 초기 위치
    JReady = [0, 0, 90, 0, 90, 0]
    set_tool("Tool Weight_2FG")
    set_tcp("2FG_TCP")

    def wait_digital_input(sig_num, node):
        while not get_digital_input(sig_num):
            time.sleep(0.5)
            print("Wait for digital input")
            pass

    def release(node):
        set_digital_output(2, ON)
        set_digital_output(1, OFF)
        wait_digital_input(2, node)

    def grip(node):
        # release()
        set_digital_output(1, ON)
        set_digital_output(2, OFF)
        wait_digital_input(1, node)

    OFFSET_GRIP_READY = 10 # 그리퍼로 막대를 잡기 위해서 위로 상승
    OFFSET_GRIP = 10 # 그리퍼를 열고 하강하여 막대를 집기 위한 오프셋
    OFFSET_GRIP_SUCCESS = 70 # 막대를 잡으면 위로 상승하여 움직여야 함

    if rclpy.ok():
        ### 1. 프로젝트 시작 전에 초기 위치로 이동 ###
        movej(JReady, vel=VELOCITY, acc=ACC)
        # move_periodic(amp=[0, 0, 0, 0, 0, 30], period=1.0, atime=0.02, repeat=10, ref=DR_TOOL)
        grip(node)

        ### 2. 시작 좌표에서 기어 잡고 목표 좌표로 옮기기 ###
        for i in range(len(start_positions)):
            start_pos = start_positions[i]
            target_pos = target_positions[i]

            # 2-1. Start Position으로 이동
            node.get_logger().info(f"Start Position {i+1}로 이동 중...")
            movel(posx([start_pos[0], start_pos[1], start_pos[2] + OFFSET_GRIP_READY, start_pos[3], start_pos[4], start_pos[5]]), vel=VELOCITY, acc=ACC)

            # 2-2. 힘 제어
            node.get_logger().info("힘 제어를 시작합니다.")
            # Force Control (Z축에 -10N의 힘을 적용)
            task_compliance_ctrl(stx=[500, 500, 500, 100, 100, 100])
            set_desired_force(fd=[0, 0, -10, 0, 0, 0], dir=[0, 0, 1, 0, 0, 0], mod=DR_FC_MOD_REL) 

            while not check_force_condition(DR_AXIS_Z, max=5):
                pass

            release_compliance_ctrl()
            time.sleep(1)
            node.get_logger().info("기어 감지")
            
            # 2-3. 블록을 잡기 위한 상승
            movel(posx([start_pos[0], start_pos[1], start_pos[2] + OFFSET_GRIP_READY, start_pos[3], start_pos[4], start_pos[5]]), vel=VELOCITY, acc=ACC)
            release(node)  # 그리퍼 열기
            
            # 2-4. 블록을 잡기 위해 하강
            movel(posx([start_pos[0], start_pos[1], start_pos[2] - OFFSET_GRIP, start_pos[3], start_pos[4], start_pos[5]]), vel=VELOCITY, acc=ACC)
            time.sleep(1)
            grip(node)  # 블록 잡기

            # 2-5. 블록 들어올리기
            movel(posx([start_pos[0], start_pos[1], start_pos[2] + OFFSET_GRIP_SUCCESS, start_pos[3], start_pos[4], start_pos[5]]), vel=VELOCITY, acc=ACC)

            # 2-6. Target Position으로 이동
            node.get_logger().info(f"Target Position {i+1}로 이동 중...")
            movel(posx([target_pos[0], target_pos[1], target_pos[2] + 40, target_pos[3], target_pos[4], target_pos[5]]), vel=90, acc=90) # 속도 빠르게
            # 기어가 박혀있는 기준의 z 값이기 때문에 여유롭게 20정도 위에 위치시킨다

            # 2-7. 4번째 작업 (가운데 기어를 이동시킬때)
            if i == 3:  # 4번째 작업에만 힘 제어와 periodic 동작 추가
                movel(posx([target_pos[0], target_pos[1], target_pos[2] + 25, target_pos[3], target_pos[4], target_pos[5]]), vel=90, acc=90)
                fd=[0, 0, -10, 0, 0, 0]
                dir=[0, 0, 1, 0, 0, 0]
                '''
                task_compliance_ctrl: 특정 축에 대한 힘 제어를 활성화
                여기서는 모든 축에 대해 비교적 높은 힘 설정을 적용하여, 로봇이 안정적으로 움직이도록 함
                
                set_desired_force: Z축 방향으로 -10N의 힘을 설정하여, 로봇이 목표 물체와 접촉할 때 필요한 힘을 제공
                '''
                task_compliance_ctrl(stx=[500, 500, 500, 100, 100, 100])
                set_desired_force(fd, dir, mod=DR_FC_MOD_REL) 

                while True:
                    # get_tool_force(DR_BASE)[2]: Z축 방향의 외력을 가져옴. 이 값이 <= 0이 되면, 즉 힘이 충분히 감지되면 주기적 동작을 시작
                    force_ext = get_tool_force(DR_BASE)[2]
                    node.get_logger().info(f"force_ext 값 : {force_ext}")
                    if force_ext <= 0:
                        amove_periodic(amp=[0, 0, 0, 0, 0, 30], period=2, atime=0.02, repeat=3, ref=DR_TOOL)
                        break

                while True:
                    position_check = get_current_posx()[0][2]
                    node.get_logger().info(f"현재 position 위치 : {position_check}")
                    #Z축 위치가 62mm 이하로 내려가면, 힘 제어를 해제하고 그리퍼를 열어줌
                    if position_check <= 62:
                        # stop(DR_QSTOP)
                        release_compliance_ctrl()
                        release(node)
                        break
                        
                    # 2-8. TCP 상승 (초기 위치로 복귀하기 위함) : z + 30
                movel(posx([target_pos[0], target_pos[1], target_pos[2] + 30, target_pos[3], target_pos[4], target_pos[5]]), vel=VELOCITY, acc=ACC)
                grip(node) 

                ''' 
                issue : 
                periodic과 movel이 동시에 진행될 수 없음 
                이 부분을 어떻게 해결해야할지 생각해봐야함
                -> V1 : 비동기 방식으로 내려가며서 periodic을 하도록 설정해봤음 -> 구현이 잘 안됨
                -> V2 : 쓰레딩 추가 : 여전히 동시에 작업이 되지 않음
                -> V3 : 힘 제어를 하는 동안에 periodic을 진행시키고, 특정 높이까지 하강하면 release를 하는 구조로 코드 변경
                '''
                '''movel(posx([target_pos[0], target_pos[1], target_pos[2] + 25, target_pos[3], target_pos[4], target_pos[5]]), vel=90, acc=90)
                
                ########################## `move_periodic`을 별도의 쓰레드로 실행 ###############################
                def periodic_motion():
                    move_periodic(
                        amp=[0, 0, 0, 0, 0, 30],
                        period=3.0,
                        atime=0.02,
                        repeat=5,
                        ref=DR_TOOL
                    )
                # 쓰레드 생성 및 시작
                periodic_thread = threading.Thread(target=periodic_motion)
                periodic_thread.start()

                amovel(posx([target_pos[0], target_pos[1], target_pos[2] + 8, target_pos[3], target_pos[4], target_pos[5]]), vel=VELOCITY, acc=ACC)
                ################ `move_periodic` 쓰레드 종료 대기 #####################
                periodic_thread.join()
                release(node)'''
                
            else: # 타겟 위치의 z 값이 기어가 들어갔을 때 기준이므로 여유를 주고 release를 해야함 : z + 9
                movel(posx([target_pos[0], target_pos[1], target_pos[2] + 9, target_pos[3], target_pos[4], target_pos[5]]), vel=VELOCITY, acc=ACC)
                release(node)

            # 2-8. TCP 상승 (초기 위치로 복귀하기 위함) : z + 30
            movel(posx([target_pos[0], target_pos[1], target_pos[2] + 30, target_pos[3], target_pos[4], target_pos[5]]), vel=VELOCITY, acc=ACC)
            grip(node) 
            
        # 종료 시 초기 위치로 복귀
        movej(JReady, vel=VELOCITY, acc=ACC)

    rclpy.shutdown()


if __name__ == "__main__":
    main()
