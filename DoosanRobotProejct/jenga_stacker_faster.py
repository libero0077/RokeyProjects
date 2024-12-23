#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ROS2 기반 두산 로봇을 사용하여 Jenga 블록을 18층까지 쌓는 제어 스크립트.
"""

import rclpy
import time
import DR_init

# 로봇 설정
ROBOT_ID = "dsr01"
ROBOT_MODEL = "m0609"
VELOCITY, ACCELERATION = 60, 60
VELOCITY_F, ACCELERATION_F = 100, 100
VELOCITY_S, ACCELERATION_S = 20, 20

DR_init.__dsr__id = ROBOT_ID
DR_init.__dsr__model = ROBOT_MODEL

# 그리퍼 상태
ON, OFF = 1, 0

# 총 층수
TOTAL_LAYERS = 6

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
            set_digital_output,
            get_digital_input,
            set_tool,
            set_tcp,
            movej,
            movel,
            DR_FC_MOD_REL,
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

    # 초기 위치(조인트)
    INITIAL_JOINT = [0, 0, 90, 0, 90, 0]

    BLOCK_FALSE_Z = 14

    # 준비 위치, 접근 위치, 적재 위치 정의 (실제 위치 값으로 수정 필요)
    PREPARE_POS = posx([569.58, 212.99, 77, 58.72, -179.99, -34.49 + 90])  # 예시 좌표
    STACK_BASE_POS = posx([448, 84, 5, 80, -179.99, 80])  # 예시 좌표
    
    APPROACH_OFFSET = posx([0, 0, 17, 0, 0, 0])

    # 현재 적재 층수
    current_layer = 0
    
    current_z_values = []
    
    grip_z = -7.2
    
    block_z = 14

    def wait_digital_input(sig_num, node, timeout=10):
        """
        디지털 입력 신호를 대기하는 함수 (타임아웃 포함)
        """
        start_time = time.time()
        while not get_digital_input(sig_num):
            if time.time() - start_time > timeout:
                node.get_logger().error(f"디지털 입력 신호 {sig_num} 대기 타임아웃.")
                return False
            rclpy.spin_once(node, timeout_sec=0.1)  # ROS 콜백 처리
            time.sleep(0.1)
            current_state = get_digital_input(sig_num)
            node.get_logger().info(f"디지털 입력 {sig_num} 상태: {current_state}. 대기 중...")
        return True

    def release(node):
        """
        그리퍼를 릴리즈하는 함수
        """
        current_state = get_digital_input(2)
        node.get_logger().info(f"현재 그리퍼 상태 (릴리즈): {current_state}")
        if current_state:
            node.get_logger().info("그리퍼가 이미 릴리즈 상태입니다.")
            return
        set_digital_output(2, ON)
        set_digital_output(1, OFF)
        if wait_digital_input(2, node):
            # 릴리즈 후 상태 확인
            new_state = get_digital_input(2)
            node.get_logger().info(f"릴리즈 후 그리퍼 상태: {new_state}")

    def grip(node):
        """
        그리퍼를 그립하는 함수
        """
        current_state = get_digital_input(1)
        node.get_logger().info(f"현재 그리퍼 상태 (그립): {current_state}")
        if current_state:
            node.get_logger().info("그리퍼가 이미 그립 상태입니다.")
            return
        set_digital_output(1, ON)
        set_digital_output(2, OFF)
        if wait_digital_input(1, node):
            # 그립 후 상태 확인
            new_state = get_digital_input(1)
            node.get_logger().info(f"그립 후 그리퍼 상태: {new_state}")

    def initialize_arm(node):
        """
        초기 위치로 이동 및 그리퍼 열기
        """
        node.get_logger().info("초기 위치로 이동.")
        movej(INITIAL_JOINT, vel=VELOCITY, acc=ACCELERATION)
        time.sleep(1)
        node.get_logger().info("그리퍼 열기.")
        release(node)
        time.sleep(0.5)
        node.get_logger().info("그리퍼 닫기.")
        grip(node)
        time.sleep(0.5)
        node.get_logger().info("초기화 완료.")

    def pick_block(node):
        """
        접근 위치로 이동 후 블록을 집는 함수
        """
        node.get_logger().info("그리퍼 닫기.")
        grip(node)
        time.sleep(0.5)
        
        node.get_logger().info("PREPARE 위치로 이동.")
        movel(PREPARE_POS, vel=VELOCITY_F, acc=ACCELERATION_F, ref=DR_BASE)
        time.sleep(1)
        
        node.get_logger().info("APPROACH 위치로 이동.")
        movel(APPROACH_OFFSET, vel=VELOCITY_F, acc=ACCELERATION_F, ref=DR_TOOL)
        time.sleep(1)
        
        # 힘 제어 시작
        node.get_logger().info("힘 제어 시작.")
        task_compliance_ctrl(stx=[500, 500, 500, 100, 100, 100])
        set_desired_force(fd=[0, 0, -10, 0, 0, 0], dir=[0, 0, 1, 0, 0, 0], mod=DR_FC_MOD_REL)

        block_gripped = False
        while not block_gripped:
            current_z = get_current_posx()[0][2]
            node.get_logger().info(f"현재 Z 위치: {current_z}")

            if check_force_condition(DR_AXIS_Z, max=5):
                node.get_logger().info("블록 감지됨. 그리퍼 열기 및 블록 집기.")
                release_compliance_ctrl()
                node.get_logger().info("그리퍼 열기.")
                release(node)
                time.sleep(0.5)
                
                movel(posx([0, 0, block_z * 4 + 1, 0, 0, 0]), vel=VELOCITY_F, acc=ACCELERATION_F, ref=DR_TOOL)
                time.sleep(1)
                node.get_logger().info("그리퍼 닫기.")
                grip(node)
                time.sleep(0.5)
                block_gripped = True
                
            elif current_z <= BLOCK_FALSE_Z * 3:
                release_compliance_ctrl()
                time.sleep(0.5)
                node.get_logger().warning("블록 감지 실패. PREPARE 위치로 재이동.")
                movel(PREPARE_POS, vel=VELOCITY_F, acc=ACCELERATION_F, ref=DR_BASE)
                time.sleep(1)
                
                node.get_logger().info("APPROACH 위치로 이동.")
                movel(APPROACH_OFFSET, vel=VELOCITY_F, acc=ACCELERATION_F, ref=DR_TOOL)
                time.sleep(1)  
        
                # Force control 다시 시작
                task_compliance_ctrl(stx=[500, 500, 500, 100, 100, 100])
                set_desired_force(fd=[0, 0, -10, 0, 0, 0], dir=[0, 0, 1, 0, 0, 0], mod=DR_FC_MOD_REL)
                
            else:
                rclpy.spin_once(node, timeout_sec=0.1)
                time.sleep(0.1)

        # 힘 제어 종료
        release_compliance_ctrl()
        node.get_logger().info("블록 집기 완료.")

    def place_block(node, layer, stack_base_pos, current_z_values):
        """
        블록을 적재 위치에 놓는 함수
        """
        stacking_pos = stack_base_pos
        
        # 스태킹 위치 계산
        stacked_z = layer * 3 * block_z
        movel(posx([0, 0, -(stacking_pos[2] + stacked_z) - 10, 0, 0, 0]), vel=VELOCITY_F, acc=ACCELERATION_F, ref=DR_TOOL)
        
        stacking_pos = posx([
            stacking_pos[0],
            stacking_pos[1],
            stacking_pos[2] + stacked_z,
            stacking_pos[3],
            stacking_pos[4],
            stacking_pos[5]
        ])

        # 짝수 층에서 조인트 6을 90도로 회전
        if layer % 2 == 0:
            stacking_pos = posx([
                stacking_pos[0],
                stacking_pos[1],
                stacking_pos[2],
                stacking_pos[3],
                stacking_pos[4],
                stacking_pos[5] + 90,
            ])
            node.get_logger().info(f"짝수 층 {layer}: 조인트 6을 {stacking_pos[4]}도로 회전.")

        current_z_values.append(stacking_pos[2])
        node.get_logger().info(f"적재 PREPARE 위치로 이동: Layer {layer}")
        movel(stacking_pos, vel=VELOCITY_F, acc=ACCELERATION_F, ref=DR_BASE)
        time.sleep(1)
        
        movel(posx([0, 0, 42, 0, 0, 0]), vel=VELOCITY_F, acc=ACCELERATION_F, ref=DR_TOOL)
        time.sleep(0.5)
        # Force control
        task_compliance_ctrl(stx=[500, 500, 500, 100, 100, 100])
        set_desired_force(fd=[0, 0, -10, 0, 0, 0], dir=[0, 0, 1, 0, 0, 0], mod=DR_FC_MOD_REL)
        while not check_force_condition(DR_AXIS_Z, max=5):
            pass
        release_compliance_ctrl()
        time.sleep(1)

        # 그리퍼 열기
        node.get_logger().info("그리퍼 열기 (블록 적재).")
        release(node)
        time.sleep(0.5)
        
        movel(posx([0, 0, -block_z, 0, 0, 0]), vel=VELOCITY_F, acc=ACCELERATION_F, ref=DR_TOOL)
        time.sleep(0.5)
        
        node.get_logger().info("그리퍼 닫기.")
        grip(node)
        time.sleep(0.5)
        
        movel(posx([0, 0, -3, 0, 0, 0]), vel=VELOCITY_F, acc=ACCELERATION_F, ref=DR_TOOL)
        movel(posx([0, 0, 0, 0, 0, 90]), vel=VELOCITY_F, acc=ACCELERATION_F, ref=DR_TOOL)
        
        # Force control
        task_compliance_ctrl(stx=[500, 500, 500, 100, 100, 100])
        set_desired_force(fd=[0, 0, -10, 0, 0, 0], dir=[0, 0, 1, 0, 0, 0], mod=DR_FC_MOD_REL)
        while not check_force_condition(DR_AXIS_Z, max=5):
            pass
        release_compliance_ctrl()
        time.sleep(1)
        
        # 그리퍼 열기
        node.get_logger().info("그리퍼 열기 (블록 적재).")
        release(node)
        time.sleep(0.5)
        
        movel(posx([0, 0, -block_z, 0, 0, 0]), vel=VELOCITY_F, acc=ACCELERATION_F, ref=DR_TOOL)
        time.sleep(0.5)
        
        node.get_logger().info("그리퍼 닫기.")
        grip(node)
        time.sleep(0.5)
        
        movel(posx([0, 0, -3, 0, 0, 0]), vel=VELOCITY_F, acc=ACCELERATION_F, ref=DR_TOOL)
        movel(posx([0, 0, 0, 0, 0, -90]), vel=VELOCITY_F, acc=ACCELERATION_F, ref=DR_TOOL)
        
        # Force control
        task_compliance_ctrl(stx=[500, 500, 500, 100, 100, 100])
        set_desired_force(fd=[0, 0, -10, 0, 0, 0], dir=[0, 0, 1, 0, 0, 0], mod=DR_FC_MOD_REL)
        while not check_force_condition(DR_AXIS_Z, max=5):
            pass
        release_compliance_ctrl()
        time.sleep(1)
        
                # 그리퍼 열기
        node.get_logger().info("그리퍼 열기 (블록 적재).")
        release(node)
        time.sleep(0.5)
        
        movel(posx([0, 0, -stacked_z/3, 0, 0, 0]), vel=VELOCITY_F, acc=ACCELERATION_F, ref=DR_TOOL)
 
        stacking_pos = posx([
            stacking_pos[0],
            stacking_pos[1] + 90,
            stacking_pos[2],
            stacking_pos[3],
            stacking_pos[4],
            stacking_pos[5]
        ])
        
        
        node.get_logger().info("move to path.")
        movel(stacking_pos, vel=VELOCITY_F, acc=ACCELERATION_F, ref=DR_BASE)
        time.sleep(1)

    def execute_tasks(node, stack_base_pos, current_z_values):
        """
        Jenga 블록을 18층까지 적재하는 함수
        """
        for layer in range(1, TOTAL_LAYERS + 1):
            node.get_logger().info(f"작업 시작: Layer {layer}")

            # 블록 집기
            pick_block(node)

            # 블록 적재
            place_block(node, layer, stack_base_pos, current_z_values)

            node.get_logger().info(f"Layer {layer} 적재 완료.")
            time.sleep(1)

        node.get_logger().info("모든 층 적재 완료.")

    # 초기화 및 작업 실행
    try:
        while rclpy.ok():
            initialize_arm(node)
            execute_tasks(node, STACK_BASE_POS, current_z_values)
            print(current_z_values)
            break  # 모든 작업을 완료한 후 루프를 종료
    except KeyboardInterrupt:
        node.get_logger().info("Keyboard Interrupt received. 종료 중.")
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()
