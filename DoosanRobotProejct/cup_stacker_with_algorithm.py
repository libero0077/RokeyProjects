#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ROS2 기반 두산 로봇을 사용하여 CUP을 TOTAL_LAYER까지 쌓는 제어 스크립트.
삼각뿔 형태로 컵을 쌓아올립니다.
"""

import rclpy
import time
import math
import DR_init

# 로봇 설정
ROBOT_ID = "dsr01"
ROBOT_MODEL = "m0609"
VELOCITY_I, ACCELERATION_I = 50, 50
VELOCITY, ACCELERATION = 150, 150

DR_init.__dsr__id = ROBOT_ID
DR_init.__dsr__model = ROBOT_MODEL

# 그리퍼 상태
ON, OFF = 1, 0

# WHAT TO DO
TOTAL_LAYER = 3

def main(args=None):
    # ROS2 초기화 및 노드 생성
    rclpy.init(args=args)
    node = rclpy.create_node("jenga_stacking", namespace=ROBOT_ID)

    # DR_init에 노드 할당
    DR_init.__dsr__node = node

    # 로봇 관련 모듈 임포트 (노드가 초기화된 후)
    try:
        from DSR_ROBOT2 import (
            release_compliance_ctrl,
            check_force_condition,
            task_compliance_ctrl,
            set_desired_force,
            get_current_posx,
            get_current_posj,
            set_digital_output,
            get_digital_input,
            set_tool,
            set_tcp,
            movej,
            movel,
            trans,
            DR_FC_MOD_REL,
            DR_FC_MOD_ABS,
            DR_MV_MOD_REL,
            DR_MV_RA_DUPLICATE,
            DR_AXIS_Z,
            DR_BASE,
            DR_TOOL,
        )
        from DR_common2 import posx

    except ImportError as e:
        node.get_logger().error(f"Error importing DSR_ROBOT2 or DR_common2: {e}")
        node.destroy_node()
        rclpy.shutdown()
        return

    # 그리퍼 설정
    set_tool("Tool Weight_2FG")
    set_tcp("2FG_TCP")

    # ABOUT CUP
    HEIGHT = 94.7
    RADIUS = 38
    
    # SAFETY
    PADDING = 6

    # TIME
    WAIT_SHORT = 0.5
    WAIT_LONG = 1

    # INITIAL JOINT
    INITIAL_JOINT = [-30, 35, 75, -130, -100, -35]

    # FIRST POINT(ABS)
    BASE_POSX = posx([569, 275, 8, 90, 127, -90])
    
    poj1= [-15.71, 16.36, 91.25, -94.44, -103.49, -18.12]
    poj2=[0,0,0,0,0,-180]
    pox1=[0,0,0,90,90,-90]
    pox2=[0,0,0,90,90,90]
    
    # OFFSETS(REL)
    RELEASE_OFFSET = 7.8
    LAY_OFFSET = 1
    
    # JOB
    TRIANGLE_BASE_LINE = (RADIUS + PADDING) * 2
    TRIANGLE_HEIGHT = math.sqrt(3)* (RADIUS + PADDING)

    def wait_digital_input(sig_num, timeout=10):
        """
        디지털 입력 신호를 대기하는 함수 (타임아웃 포함)
        """
        start_time = time.time()
        node.get_logger().info(f"디지털 입력 {sig_num} 상태. 대기 중...")
        while not get_digital_input(sig_num):
            if time.time() - start_time > timeout:
                node.get_logger().error(f"디지털 입력 신호 {sig_num} 대기 타임아웃.")
                return False
            rclpy.spin_once(node, timeout_sec=0.1)  # ROS 콜백 처리
            time.sleep(0.1)         
        return True

    def release_gripper():
        """
        그리퍼를 릴리즈하는 함수
        """
        node.get_logger().info("그리퍼 열기.")
        current_state = get_digital_input(2)
        node.get_logger().info(f"현재 그리퍼 상태 (릴리즈): {current_state}")
        if current_state:
            node.get_logger().info("그리퍼가 이미 릴리즈 상태입니다.")
            return
        set_digital_output(2, ON)
        set_digital_output(1, OFF)
        if wait_digital_input(2):
            # 릴리즈 후 상태 확인
            new_state = get_digital_input(2)
            node.get_logger().info(f"릴리즈 후 그리퍼 상태: {new_state}")
        time.sleep(WAIT_SHORT)

    def grip_gripper():
        """
        그리퍼를 그립하는 함수
        """
        node.get_logger().info("그리퍼 닫기.")
        current_state = get_digital_input(1)
        node.get_logger().info(f"현재 그리퍼 상태 (그립): {current_state}")
        if current_state:
            node.get_logger().info("그리퍼가 이미 그립 상태입니다.")
            return
        set_digital_output(1, ON)
        set_digital_output(2, OFF)
        if wait_digital_input(1):
            # 그립 후 상태 확인
            new_state = get_digital_input(1)
            node.get_logger().info(f"그립 후 그리퍼 상태: {new_state}")
        time.sleep(WAIT_SHORT)
        
    def pickup_cups(node, up=True):
        """
        CUP을 집는 함수
        현재 위치에서 GRIP_POSX만큼 내려가서 그리퍼를 그립하고, PICKUP_POSX로 이동하여 컵을 집습니다.
        """
        grip_gripper()
        node.get_logger().info("컵을 집었습니다.")
        
        node.get_logger().info("PICKUP 위치로 이동.")
        current = get_current_posx()[0]
        node.get_logger().info(f"{current}")
        H = HEIGHT
        if current[4] > 0:
            lay_offset = -1 * LAY_OFFSET
        else:
            lay_offset = LAY_OFFSET
        if up == False:
            H = 10
        lay_posx = posx([
            current[0],
            current[1],
            current[2] + H - 3,
            current[3],
            current[4] + lay_offset,
            current[5]
        ])
        node.get_logger().info(f"{lay_posx}")
        movel(lay_posx, vel=VELOCITY, acc=ACCELERATION, ref=DR_BASE)
        time.sleep(WAIT_LONG)
        
        
    def set_cups(node, layer, up=True):
        """
        CUP을 놓는 함수
        현재 위치에서 SET_POSX로 내려가면서 힘 제어를 시작하고, 힘이 감지되면 그리퍼를 릴리즈합니다.
        """
        
        node.get_logger().info("ERECT CUP.")
        current = get_current_posx()[0]
        option = 3
        H = HEIGHT
        if current[4] > 0:
            lay_offset = -1 * LAY_OFFSET
        else:
            lay_offset = LAY_OFFSET
        if up == False:
            H, option = 10, 0
        erect_posx = posx([
            current[0],
            current[1],
            current[2] - (H + option),
            current[3],
            current[4] - (lay_offset),
            current[5]
        ])
        movel(erect_posx, vel=VELOCITY, acc=ACCELERATION, ref=DR_BASE)
        time.sleep(WAIT_LONG)
        
        node.get_logger().info("컵을 놓기 위해 내려가기.")

        # 힘 제어 시작
        node.get_logger().info("힘 제어 시작 (컵 놓기).")
        task_compliance_ctrl(stx=[500, 500, 500, 100, 100, 100])
        set_desired_force(fd=[0, 0, -5, 0, 0, 0], dir=[0, 0, 1, 0, 0, 0], mod=DR_FC_MOD_REL)
        while not check_force_condition(DR_AXIS_Z, max=3):
            pass
        # 컵 릴리즈
        release_compliance_ctrl()
        time.sleep(WAIT_LONG)      
          
        release_gripper()
        node.get_logger().info("컵을 놓았습니다.")


        # 현재 위치 가져오기
        current = get_current_posx()[0]
        # RELEASE_POSX만큼 이동 (상대 좌표)
        node.get_logger().info("RELEASE POINT")
        release_posx = posx([
            current[0],
            current[1],
            H * (TOTAL_LAYER - layer) + RELEASE_OFFSET,
            current[3],
            current[4],
            current[5]
        ])
        movel(release_posx, vel=VELOCITY, acc=ACCELERATION, ref=DR_BASE)
        time.sleep(WAIT_LONG)

    def initialize_arm():
        """
        초기 위치로 이동 및 그리퍼 열기
        """
        release_gripper()
        
        node.get_logger().info("초기 위치로 이동.")
        movej(INITIAL_JOINT, vel=VELOCITY_I, acc=ACCELERATION_I)
        time.sleep(WAIT_LONG)
        
        node.get_logger().info("INITIAL GRIP 위치로 이동.")
        current = get_current_posx()[0]
        approach_posx = posx([
            BASE_POSX[0],
            current[1],
            current[2],
            current[3],
            current[4],
            current[5]
        ])
        movel(approach_posx, vel=VELOCITY, acc=ACCELERATION, ref=DR_BASE)
        time.sleep(WAIT_LONG)
        movel(BASE_POSX, vel=VELOCITY, acc=ACCELERATION, ref=DR_BASE)
        time.sleep(WAIT_LONG)

        pickup_cups(node)
        
        node.get_logger().info("초기화 완료.")


    def execute_current_layer(layer):
        """
        CUP을 적재 위치에 놓는 함수
        """
        node.get_logger().info(f"Layer {layer} 작업 시작.")
        # 층별 선(line) 생성
        for line in range(layer, 1, -1):
            node.get_logger().info(f"Layer {layer}, Line {line} 시작.")
            if (layer % 2 == 0 and line % 2 == 1) or (layer % 2 == 1 and line % 2 == 0):
                node.get_logger().info(f"{layer, line}.")            
                for _ in range(line - 1):
                    move_vector = posx([TRIANGLE_BASE_LINE, 0, 0, 0, 0, 0])
                    current = get_current_posx()[0]
                    target_posx = trans(current, move_vector, ref=DR_BASE)
                    movel(target_posx, vel=VELOCITY, acc=ACCELERATION, ref=DR_BASE)
                    time.sleep(WAIT_LONG)
                    set_cups(node, layer)
                    pickup_cups(node)
                
                move_vector = posx([-TRIANGLE_BASE_LINE/2, -TRIANGLE_HEIGHT, 0, 0, 0, 0])
                current = get_current_posx()[0]
                target_posx = trans(current, move_vector, ref=DR_BASE)
                movel(target_posx, vel=VELOCITY, acc=ACCELERATION, ref=DR_BASE)
                time.sleep(WAIT_LONG)
                set_cups(node, layer)
                pickup_cups(node)
                
            else:
                node.get_logger().info(f"{layer, line}.")
                for _ in range(line - 1):
                    move_vector = posx([-TRIANGLE_BASE_LINE, 0, 0, 0, 0, 0])
                    current = get_current_posx()[0]
                    target_posx = trans(current, move_vector, ref=DR_BASE)
                    movel(target_posx, vel=VELOCITY, acc=ACCELERATION, ref=DR_BASE)
                    time.sleep(WAIT_LONG)
                    set_cups(node, layer)
                    pickup_cups(node)
                
                move_vector = posx([TRIANGLE_BASE_LINE/2, -TRIANGLE_HEIGHT, 0, 0, 0, 0])
                current = get_current_posx()[0]
                target_posx = trans(current, move_vector, ref=DR_BASE)
                movel(target_posx, vel=VELOCITY, acc=ACCELERATION, ref=DR_BASE)
                time.sleep(WAIT_LONG)
                set_cups(node, layer)
                pickup_cups(node)
                
            node.get_logger().info(f"Layer {layer}, Line {line} 작업 완료.")

        # 층 작업 완료 후, 새로운 베이스 위치 계산
        new_base_x = (layer -2) * TRIANGLE_HEIGHT/2
        new_base_y = (layer -2) * TRIANGLE_BASE_LINE + TRIANGLE_BASE_LINE/2
        node.get_logger().info(f"Layer {layer} 작업 완료. 새로운 베이스 위치로 이동: ({new_base_x}, {new_base_y}).")
        if layer == 2:
            move_vector = posx([new_base_x, new_base_y, 0, 0, 0, 0])
            target_base_posx = trans(current, move_vector, ref=DR_BASE)
            movel(target_base_posx, vel=VELOCITY, acc=ACCELERATION, ref=DR_BASE)
                
            # 힘 제어 시작
            node.get_logger().info("힘 제어 시작 (컵 놓기).")
            task_compliance_ctrl(stx=[500, 500, 500, 100, 100, 100])
            set_desired_force(fd=[0, 0, -5, 0, 0, 0], dir=[0, 0, 1, 0, 0, 0], mod=DR_FC_MOD_REL)

            while not check_force_condition(DR_AXIS_Z, max=3):
                pass
            release_compliance_ctrl()
            time.sleep(WAIT_LONG)                  
            # 컵 릴리즈
            release_gripper()
            node.get_logger().info("컵을 놓았습니다.")

        
            pickup_cups(node)
            currentX = get_current_posx()[0]
            currentJ = get_current_posj()
            node.get_logger().info(f"x: {currentX}")
            node.get_logger().info(f"j: {currentJ}")
            return
        else: 
            move_vector = posx([new_base_x, new_base_y, 0, 0, 0, 0])
            current = get_current_posx()[0]
            target_base_posx = trans(current, move_vector, ref=DR_BASE)
            movel(target_base_posx, vel=VELOCITY, acc=ACCELERATION, ref=DR_BASE)
            time.sleep(WAIT_LONG)
            
            set_cups(node, layer, up=False)
            pickup_cups(node)
    
    def execute_tasks(total_layer):
        for layer in range(total_layer, 1, -1):
            node.get_logger().info(f"작업 시작: Layer {layer}")
            execute_current_layer(layer)
            node.get_logger().info(f"Layer {layer} 적재 완료.")
            currentx = get_current_posx()[0]
            currentj = get_current_posj()[0]
            node.get_logger().info(f"{currentx}")
            node.get_logger().info(f"{currentj}")
            time.sleep(WAIT_LONG)

        node.get_logger().info("모든 층 적재 완료.")

    # 초기화 및 작업 실행
    try:
        initialize_arm()
        execute_tasks(TOTAL_LAYER)
    except KeyboardInterrupt:
        node.get_logger().info("Keyboard Interrupt received. 종료 중.")
    finally:
        try:
            node.get_logger().info("LAST DANCE")
        except Exception as e:
            node.get_logger().error(f"LAST DANCE ERROR: {e}")
        
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()
