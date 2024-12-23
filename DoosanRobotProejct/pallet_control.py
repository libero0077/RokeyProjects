#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
3*3 팔레트에 랜덤하게 배치된 블록을 높이에 따라 정렬하는 ROS2 기반 두산 로봇 제어 스크립트.
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

def main(args=None):
    # ROS2 초기화 및 노드 생성
    rclpy.init(args=args)
    node = rclpy.create_node("force_control", namespace=ROBOT_ID)

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

    # 오프셋
    OFFSET_READY = posx([0, 0, -5, 0, 0, 0])
    OFFSET_GRIP = posx([0, 0, 25, 0, 0, 0])
    OFFSET_DETECT = posx([0, 0, 50, 0, 0, 0])

    # 목표 팔레트 위치 설정 (실제 위치 값으로 수정 필요)

    Z = 130

    RX, RY, RZ = 20.75, 179.00, 19.09

    TARGET_POSITIONS = {
        1: posx([349.7, 100.7, Z, RX, RY, RZ]),
        2: posx([350.23, 49.69, Z, RX, RY, RZ]),
        3: posx([350.81, -1.20, Z, RX, RY, RZ]),
        4: posx([299.78, 99.96, Z, RX, RY, RZ]),
        5: posx([299.14, 48.93, Z, RX, RY, RZ]),
        6: posx([299.65, -1.73, Z, RX, RY, RZ]),
        7: posx([247.7, 99.56, Z, RX, RY, RZ]),
        8: posx([248.10, 48.68, Z, RX, RY, RZ]),
        9: posx([248.43, -2.55, Z, RX, RY, RZ]),
    }

    # 홈 포지션을 레벨별로 그룹화하고 Y값이 높은 순으로 정렬
    HOME_POSITIONS = {
        1: sorted([
            {"position": posx([500.62, -0.66, Z, RX, RY, RZ]), "used": False},
            {"position": posx([500.3, 50.33, Z, RX, RY, RZ]), "used": False},
            {"position": posx([499.81, 101.43, Z, RX, RY, RZ]), "used": False},
        ], key=lambda x: x['position'][1], reverse=True),
        2: sorted([
            {"position": posx([449.5, -0.96, Z, RX, RY, RZ]), "used": False},
            {"position": posx([449.09, 50.19, Z, RX, RY, RZ]), "used": False},
            {"position": posx([448.55, 101.01, Z, RX, RY, RZ]), "used": False},
        ], key=lambda x: x['position'][1], reverse=True),
        3: sorted([
            {"position": posx([398.42, -1.44, Z, RX, RY, RZ]), "used": False},
            {"position": posx([397.85, 49.61, Z, RX, RY, RZ]), "used": False},
            {"position": posx([397.5, 100.71, Z, RX, RY, RZ]), "used": False},
        ], key=lambda x: x['position'][1], reverse=True),
    }

    def wait_digital_input(sig_num, node, timeout=10):
        """
        디지털 입력 신호를 대기하는 함수 (타임아웃 포함)
        """
        start_time = time.time()
        while not get_digital_input(sig_num):
            if time.time() - start_time > timeout:
                node.get_logger().error(f"디지털 입력 신호 {sig_num} 대기 타임아웃.")
                return
            rclpy.spin_once(node, timeout_sec=0.1)  # ROS 콜백 처리
            time.sleep(0.1)
            current_state = get_digital_input(sig_num)
            node.get_logger().info(f"디지털 입력 {sig_num} 상태: {current_state}. 대기 중...")

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
        wait_digital_input(2, node)
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
        wait_digital_input(1, node)
        # 그립 후 상태 확인
        new_state = get_digital_input(1)
        node.get_logger().info(f"그립 후 그리퍼 상태: {new_state}")

    def find_available_home_position(home_level, HOME_POSITIONS, node):
        """
        주어진 레벨에서 사용 가능한 첫 번째 홈 위치를 찾는 함수 (Y값이 높은 순)
        """
        if home_level not in HOME_POSITIONS:
            node.get_logger().error(f"존재하지 않는 레벨: {home_level}")
            return None, None

        for idx, home in enumerate(HOME_POSITIONS[home_level]):
            if not home["used"]:
                node.get_logger().info(f"사용 가능한 홈 위치 찾음: 레벨 {home_level}, 포지션 {idx + 1}")
                return idx, home["position"]
        node.get_logger().warning(f"레벨 {home_level}에 사용 가능한 홈 위치가 없습니다.")
        return None, None

    def mark_home_position_used(home_level, index, HOME_POSITIONS, node):
        """
        특정 레벨의 홈 위치를 사용 완료로 표시하는 함수
        """
        if home_level in HOME_POSITIONS and 0 <= index < len(HOME_POSITIONS[home_level]):
            HOME_POSITIONS[home_level][index]["used"] = True
            node.get_logger().info(f"레벨 {home_level}의 홈 위치 {index + 1}을(를) 사용 완료로 표시.")
        else:
            node.get_logger().error(f"잘못된 레벨 또는 인덱스: 레벨 {home_level}, 인덱스 {index}")

    def task(num, TARGET_POSITIONS, HOME_POSITIONS, node):
        """
        특정 번호의 목표 위치에서 블록을 집고 정렬하는 작업
        """
        node.get_logger().info(f"작업 시작: 목표 위치 번호 {num}")

        target_pos = TARGET_POSITIONS.get(num)
        if not target_pos:
            node.get_logger().error(f"잘못된 목표 위치 번호: {num}")
            return

        # 목표 위치로 이동
        node.get_logger().info(f"목표 위치로 이동: {target_pos}")
        movel(target_pos, vel=VELOCITY_F, acc=ACCELERATION_F, ref=DR_BASE)
        time.sleep(1)

        # 감지 위치로 하강
        movel(OFFSET_DETECT, vel=VELOCITY, acc=ACCELERATION, ref=DR_TOOL)
        time.sleep(1)

        # 힘 제어 시작
        node.get_logger().info("힘 제어 시작.")
        task_compliance_ctrl(stx=[500, 500, 500, 100, 100, 100])
        set_desired_force(fd=[0, 0, -20, 0, 0, 0], dir=[0, 0, 1, 0, 0, 0], mod=DR_FC_MOD_REL)
        while not check_force_condition(DR_AXIS_Z, max=5):
            rclpy.spin_once(node, timeout_sec=0.1)  # ROS 콜백 처리
            time.sleep(0.1)
        
        node.get_logger().info("그리퍼 열기.")
        release(node)
        time.sleep(0.5)
        
        # 힘 제어 종료
        release_compliance_ctrl()
        time.sleep(2)
        node.get_logger().info("release")
        print(get_current_posx())
        current_z = get_current_posx()[0][2]
        print(current_z)

        # 높이에 따른 홈 레벨 결정
        if current_z >= 61.5:
            home_level = 3
        elif current_z >= 51.9:
            home_level = 2
        elif current_z >= 39.2:
            home_level = 1
        else:
            node.get_logger().info("블록 높이 기준 미달. 초기 위치로 복귀.")
            movej(INITIAL_JOINT, vel=VELOCITY, acc=ACCELERATION)
            time.sleep(1)
            return

        node.get_logger().info(f"힘 제어 종료. 현재 Z 위치: {current_z}. 블록 레벨: Level {home_level}")

        # 사용 가능한 홈 위치 찾기
        home_index, home_pos = find_available_home_position(home_level, HOME_POSITIONS, node)
        if home_pos is None:
            node.get_logger().error(f"Level {home_level} 블록에 대한 사용 가능한 홈 위치가 없습니다.")
            movej(INITIAL_JOINT, vel=VELOCITY, acc=ACCELERATION)
            time.sleep(1)
            return

        # 그리퍼 열기
        # movel(OFFSET_READY, vel=VELOCITY, acc=ACCELERATION, ref=DR_TOOL)
        
        # 그립 위치로 이동
        node.get_logger().info("그립 위치로 이동")
        movel(OFFSET_GRIP, vel=VELOCITY, acc=ACCELERATION, ref=DR_TOOL)

        # 그리퍼 닫기
        node.get_logger().info("그리퍼 닫기")
        grip(node)
        time.sleep(1)
        
        # 집어올리기
        node.get_logger().info("집어올리기")
        movel(target_pos, vel=VELOCITY, acc=ACCELERATION, ref=DR_BASE)

        # 홈 위치로 이동 및 블록 놓기
        node.get_logger().info(f"홈 위치로 이동: 레벨 {home_level}, 포지션 {home_index + 1}")
        movel(home_pos, vel=VELOCITY, acc=ACCELERATION, ref=DR_BASE)
        time.sleep(1)
        
        # 감지 위치로 하강
        movel(OFFSET_DETECT, vel=VELOCITY, acc=ACCELERATION, ref=DR_TOOL)
        time.sleep(1)
        
        # 드롭 위치로 이동
        movel([0, 0, current_z - 5, 0, 0, 0], vel=VELOCITY_S, acc=ACCELERATION_S, ref=DR_TOOL)
        time.sleep(1)

        # 그리퍼 열기
        node.get_logger().info("그리퍼 열기.")
        release(node)
        time.sleep(0.5)

        # 홈 위치를 사용 완료로 표시
        mark_home_position_used(home_level, home_index, HOME_POSITIONS, node)
        node.get_logger().info(f"포지션 {home_index + 1} 에 Level {home_level} 블록이 배치되었습니다.")
        
        # 다시 위쪽 위치로 복귀
        movel(home_pos, vel=VELOCITY, acc=ACCELERATION, ref=DR_BASE)
        node.get_logger().info(f"작업 완료: 목표 위치 번호 {num}")
        
        # 그리퍼 초기화(감지)
        grip(node)
        time.sleep(0.5)

    def execute_tasks(TARGET_POSITIONS, HOME_POSITIONS, node):
        """
        1부터 9까지의 작업을 순차적으로 수행
        """
        node.get_logger().info("모든 작업 시작.")
        for num in range(1, 10):
            task(num, TARGET_POSITIONS, HOME_POSITIONS, node)
        node.get_logger().info("모든 작업 완료.")
        
    def initialize_arm(node):    
        # 초기 위치로 이동 및 그리퍼 닫기
        movej(INITIAL_JOINT, vel=VELOCITY, acc=ACCELERATION)
        time.sleep(1)
        grip(node)
        time.sleep(0.5)
        node.get_logger().info("초기화 완료.")

    # 초기화 및 작업 실행
    try:
        while rclpy.ok():
            initialize_arm(node)
            execute_tasks(TARGET_POSITIONS, HOME_POSITIONS, node)
            break  # 모든 작업을 완료한 후 루프를 종료
    except KeyboardInterrupt:
        node.get_logger().info("Keyboard Interrupt received. 종료 중.")
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()