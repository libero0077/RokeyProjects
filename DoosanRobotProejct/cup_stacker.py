import rclpy
import DR_init
import logging
import math

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# for single robot
ROBOT_ID = "dsr01"
ROBOT_MODEL = "m0609"

DR_init.__dsr__id = ROBOT_ID
DR_init.__dsr__model = ROBOT_MODEL

ON, OFF = 1, 0

def main(args=None):
    rclpy.init(args=args)
    node = rclpy.create_node("rokey_simple_move", namespace=ROBOT_ID)
    DR_init.__dsr__node = node
    try:
        from DSR_ROBOT2 import (
            set_digital_output,
            wait,
            set_tool,
            set_tcp,
            movej,
            amovej,
            movel,
            movec,
            amovel,
            trans,
            DR_MV_MOD_REL,
            DR_AXIS_Z,
            DR_FC_MOD_REL,
            task_compliance_ctrl,
            set_desired_force,
            check_force_condition,
            release_compliance_ctrl,
            get_current_posx,
        )
        from DR_common2 import posx, posj
    except ImportError as e:
        print(f"Error importing DSR_ROBOT2 : {e}")
        return

    set_tool("Tool Weight_2FG")
    set_tcp("2FG_TCP")

    # 컵 사이즈
    HEIGHT = 94.7
    RADIUS = 38

    #타워 층 
    layer = 3

    # 시작 좌표
    starting_point = [707, 112.5, 5, 60, 125, 90]
    second_point = starting_point   # line 기준 좌표
    cup_position = second_point   # cup 기준 좌표

    # 이격 거리
    PADDING = 3
    Z_OFFSET = 100

    # 시간 변수
    WAIT_SHORT = 0.3
    WAIT_LONG = 1

    # 작업 위치 변수
    TRIANGLE_X = (RADIUS + PADDING) * 2
    TRIANGLE_Y = math.sqrt(3)* (RADIUS + PADDING)

    # 그리퍼 변수
    TILT_ANGLE = 120.0    # 기울임 각도

    # 속도
    VELOCITY, ACC = 500.0, 600.0    # 보통 속도
    A_VELOCITY, A_ACC = 200.0, 150.0  # 접근 속도

    # 기타 변수
    floor = 1
    line = 1
    cup = 1 
    floor_change_flag = False
    JReady = [0, 0, 90, 0, 90, 0]
    

    def ungrip():
        logging.info("언그립")
        set_digital_output(2, ON)
        set_digital_output(1, OFF)
        wait(0.3)

    def grip():
        logging.info("그립")
        set_digital_output(1, ON)
        set_digital_output(2, OFF)
        wait(0.4)

    def t_trans(a, b):
        c = list(trans(a, b))
        return c
    
    while rclpy.ok():
        logging.info("시작")
        amovej(JReady, vel=A_VELOCITY, acc=A_ACC)
        ungrip()
        wait(1)

        logging.info("초기 위치로 이동")
        movel(t_trans(starting_point, [-25, -43, 0, 0, 0, 0]), vel=A_VELOCITY, acc=A_ACC) # 접근 위치로 이동
        movel(starting_point, vel=A_VELOCITY, acc=A_ACC)    # 최종 접근
        grip()  # 그립

        high = [starting_point[0], starting_point[1], starting_point[2] + Z_OFFSET, starting_point[3], TILT_ANGLE, starting_point[5]]
        amovel(high, vel=VELOCITY, acc=ACC)  # 최종 상승 및 기울이기
        wait(WAIT_SHORT)
        # 초기화 끝

        for i in range(layer, 0, -1):  # 층 출력
            logging.info(f"{floor} 층")

            for j in range(i, 0, -1):  # 라인 출력
                logging.info(f"\t{line} 라인")

                for k in range(j, 0, -1):  # 블럭 출력
                    logging.info(f"\t\t{cup} 번째 컵")
                    if floor == 1 and line == 1 and cup == 1:   #제일 처음 컵은 패스
                        pass
                    else:
                        if floor_change_flag == True:  # 층 이동이 있을때
                            floor_change_flag = False   # 층 이동 플레그 초기화

                            logging.info("1. 기울임 해제하고 목표로 바로 이동")
                            movec([cup_position[0], cup_position[1], cup_position[2], cup_position[3], cup_position[4], cup_position[5]], t_trans(cup_position, [0, 0, -7, 0, 0, 0]), vel=VELOCITY, acc=ACC)
                            
                        else:   # 층 이동이 없을때
                            logging.info("3. 목표로 이동 중 곡선으로 하강")
                            movec([cup_position[0], cup_position[1], cup_position[2] + Z_OFFSET, cup_position[3], TILT_ANGLE, cup_position[5]], t_trans(cup_position, [0, 0, -7, 0, 0, 0]), vel=VELOCITY, acc=ACC)

                        logging.info("4. 포스 제어")
                        # 포스 제어 시작
                        task_compliance_ctrl(stx=[500, 500, 500, 100, 100, 100])
                        set_desired_force(fd=[0, 0, -20, 0, 0, 0], dir=[0, 0, 1, 0, 0, 0], mod=DR_FC_MOD_REL)
                        while not check_force_condition(DR_AXIS_Z, max=5):
                            pass
                        release_compliance_ctrl()
                        logging.debug("하단 접촉 포스 제어 종료")

                        logging.info("5. 2mm 상승")
                        amovel([0, 0, 2, 0, 0, 0], vel=A_VELOCITY, acc=A_ACC, mod=DR_MV_MOD_REL) # z2 상승
                        ungrip()    # 언 그립
                        
                        if floor == layer and line == 1 and cup == 1:
                            logging.debug("타워 마지막 동작")
                        else:
                            logging.info("6. 컵을 잡기위해 목표 위치로 이동")
                            movel(cup_position, vel=VELOCITY, acc=ACC)  # 그립 위치로 이동
                            grip()  # 그립

                            logging.info("8. 최종 상승 및 기울이기")
                            a_point = [cup_position[0], cup_position[1], cup_position[2] + Z_OFFSET, cup_position[3], TILT_ANGLE, cup_position[5]]
                            amovel(a_point, vel=VELOCITY, acc=ACC)  # 최종 상승 및 기울이기
                            wait(WAIT_SHORT)   # 어느정도 올라가는 시간 보장
                    
                    # x 좌표 업데이트
                    cup_position = t_trans(cup_position, [-TRIANGLE_X, 0, 0, 0, 0, 0])
                    logging.info(f"X 좌표 업데이트: {cup_position}")

                    cup += 1

                # XY 기준 좌표 업데이트
                logging.info("XY 기준 좌표 업데이트")
                second_point = t_trans(second_point, [-(TRIANGLE_X / 2), -TRIANGLE_Y, 0, 0, 0, 0])
                cup_position = second_point
                logging.info(f"XY 좌표 업데이트: {cup_position}")

                if floor == 1 and line == 1:
                    line_change_flag = True # 라인 변경 플레그 활성화
                
                cup = 1
                line += 1

            # XYZ 기준 좌표 업데이트
            starting_point = t_trans(starting_point, [-(TRIANGLE_X / 2), -(TRIANGLE_Y / 3), HEIGHT, 0, 0, 0])
            second_point = starting_point
            cup_position = second_point
            logging.info(f"XYZ 좌표 업데이트: {cup_position}")
            
            floor_change_flag = True # 층 변경 플레그 활성화

            line = 1
            floor += 1

        # 탑 쌓기 끝
        logging.info("맥주잔 설치 시작")
        amovel([0,0,HEIGHT / 2,0,0,0], vel=VELOCITY, acc=ACC, mod=DR_FC_MOD_REL)
        wait(0.1)

        # 90도 그립
        cup_position = [2.5 + (starting_point[0] + (TRIANGLE_X / 2)), 4.33 + (starting_point[1] + (TRIANGLE_Y / 3)), (starting_point[2] - HEIGHT) + 14, 60, 90, 90]
        movel(cup_position, vel=VELOCITY, acc=ACC)  # 그립 위치로 이동

        grip()
        logging.debug(cup_position)
        
        cup_position = t_trans(cup_position, [-2.5,-4.33,Z_OFFSET*1.8,0,0,0])
        logging.debug(f"z {Z_OFFSET*2} 상승: {cup_position}")
        amovel(cup_position, vel=VELOCITY, acc=ACC)    # z200 상승
        wait(0.2)
        
        # # 90도의 회전
        cup_position = [cup_position[0] + 2.5, cup_position[1] + 4.33, cup_position[2], 60, 90, -90]
        logging.debug(f"손목 회전: {a_point}")
        movel(cup_position, vel=A_VELOCITY*1.2, acc=A_ACC + 50) # 180도 회전

        movel([0, 0, -50, 0, 0, 0], vel=VELOCITY, acc=ACC, mod=DR_FC_MOD_REL)

        ungrip()

        movel([0,0,Z_OFFSET*2,0,0,0], vel=VELOCITY, acc=ACC, mod=DR_FC_MOD_REL)    #z 200 상승

        logging.info("종료 동작")
        movej(JReady, vel=VELOCITY, acc=ACC)
        logging.info("Done")

        # 퍼포먼스
        for i in range(3):
            movej([0, 0, 90, 0, 63, 0], vel=VELOCITY, acc=ACC)
            movej([0, 0, 90, 0, 117, 0], vel=VELOCITY, acc=ACC)

        movej([0, -50, 135, 0, 5, 0], vel=VELOCITY, acc=ACC)
        for i in range(3):
            movel(posx([250, 0, 0, 0, 0, 0]), vel=200, acc=200,mod=DR_FC_MOD_REL)
            movel(posx([-200, 0, 0, 0, 0, 0]), vel=200, acc=200,mod=DR_FC_MOD_REL)
        movej(JReady, vel=A_VELOCITY, acc=A_ACC)

        break
    rclpy.shutdown()
if __name__ == "__main__":
    main()