import yaml
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import logging
import math
from coverage_algorithm import (
    mark_inflated_obstacles,
    generate_coverage_path,
    extract_region,
    world_to_map,
    map_to_world,
    mark_visited,
    bresenham_line
)

def visualize_coverage(map_array: np.ndarray, inflated_map: np.ndarray,
                      path: list, goal_points: list,
                      resolution: float, origin_x: float, origin_y: float,
                      start_x: float, start_y: float,
                      robot_radius: float, visited_map: np.ndarray):
    """
    맵, 커버리지 경로, 목표 지점을 애니메이션으로 시각화합니다.
    """
    logger = logging.getLogger('visualization')

    # 색상 매핑 설정
    # 0: 자유 공간 (흰색), 100: 장애물 (검정색), -1: 확장된 장애물 (하늘색), 1: 방문 영역 (회색)
    color_array = np.zeros((map_array.shape[0], map_array.shape[1], 3), dtype=np.uint8)
    color_array[map_array == 0] = [255, 255, 255]      # 자유 공간 - 흰색
    color_array[map_array == 100] = [0, 0, 0]          # 장애물 - 검정색
    color_array[inflated_map == -1] = [135, 206, 235]  # 확장된 장애물 - 하늘색

    logger.info("Color array for visualization prepared.")

    # 애니메이션 설정
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.set_xlim(origin_x, origin_x + map_array.shape[1] * resolution)
    ax.set_ylim(origin_y, origin_y + map_array.shape[0] * resolution)
    ax.set_xlabel('X (meters)')
    ax.set_ylabel('Y (meters)')
    ax.set_title('Coverage Path Animation with Visited Areas and Goal Points')

    # 배경 이미지 설정
    background = ax.imshow(color_array, origin='lower', extent=[
        origin_x, origin_x + map_array.shape[1] * resolution,
        origin_y, origin_y + map_array.shape[0] * resolution
    ])
    logger.info("Background image set for visualization.")

    # 로봇 경로를 그릴 선과 포인트 초기화
    path_line, = ax.plot([], [], color='red', linewidth=2, label='Robot Path')
    robot_point, = ax.plot([], [], marker='o', color='blue', markersize=5, label='Robot')

    # 시작점 표시
    ax.scatter(start_x, start_y, color='green', label='Start Point', s=100)
    logger.info("Start point marked on visualization.")

    # 현재 목표 지점 표시 (애니메이션 동작 중 변경됨)
    current_goal_scatter = ax.scatter([], [], color='yellow', label='Current Goal', s=100, marker='*')

    ax.legend()

    # 애니메이션을 위한 데이터 준비
    path_x = [p[0] for p in path]
    path_y = [p[1] for p in path]
    num_frames = len(path_x)

    # 각 컬럼의 끝단 목표지점을 계산
    goal_per_column = {}
    for goal_x, goal_y in goal_points:
        col = world_to_map(goal_x, goal_y, origin_x, origin_y, resolution)[1]
        if col not in goal_per_column or goal_y > goal_per_column[col][1]:
            goal_per_column[col] = (goal_x, goal_y)

    logger.info(f"Starting animation with {num_frames} frames.")

    # 동적으로 방문 맵을 업데이트하기 위한 초기화
    visited_map_dynamic = np.zeros_like(map_array, dtype=np.uint8)

    # 로봇 반경에 해당하는 셀 수 계산
    robot_radius_cells = int(math.ceil(robot_radius / resolution))
    logger.info(f"Robot radius in cells: {robot_radius_cells}")

    # 로봇 반경 마스크 미리 생성
    y, x = np.ogrid[-robot_radius_cells:robot_radius_cells+1, -robot_radius_cells:robot_radius_cells+1]
    mask = x**2 + y**2 <= robot_radius_cells**2

    def init():
        path_line.set_data([], [])
        robot_point.set_data([], [])
        current_goal_scatter.set_offsets(np.empty((0, 2)))
        background.set_data(color_array)
        return path_line, robot_point, current_goal_scatter, background

    def animate(i):
        if i >= num_frames:
            i = num_frames - 1

        # 현재 로봇 위치
        current_x = path_x[i]
        current_y = path_y[i]

        # 경로 선 업데이트
        path_line.set_data(path_x[:i+1], path_y[:i+1])
        robot_point.set_data([current_x], [current_y])

        # 현재 컬럼에 해당하는 목표 지점 계산
        current_col = world_to_map(current_x, current_y, origin_x, origin_y, resolution)[1]
        if current_col in goal_per_column:
            current_goal_x, current_goal_y = goal_per_column[current_col]
            current_goal_scatter.set_offsets([[current_goal_x, current_goal_y]])
        else:
            current_goal_scatter.set_offsets(np.empty((0, 2)))

        # 현재 위치를 방문 지점으로 표시 (로봇 반경 고려)
        row, col = world_to_map(current_x, current_y, origin_x, origin_y, resolution)

        # 마스크를 맵에 적용하여 방문 지점 업데이트
        row_min = max(row - robot_radius_cells, 0)
        row_max = min(row + robot_radius_cells + 1, map_array.shape[0])
        col_min = max(col - robot_radius_cells, 0)
        col_max = min(col + robot_radius_cells + 1, map_array.shape[1])

        # 마스크의 해당 부분 추출
        mask_subset = mask[
            (row_min - (row - robot_radius_cells)) : (mask.shape[0] - (row + robot_radius_cells + 1 - row_max)),
            (col_min - (col - robot_radius_cells)) : (mask.shape[1] - (col + robot_radius_cells + 1 - col_max))
        ]

        # 방문 맵 업데이트
        visited_map_dynamic[row_min:row_max, col_min:col_max] |= mask_subset.astype(np.uint8)

        # 업데이트된 방문 영역 색상 반영
        color_array_dynamic = color_array.copy()
        color_array_dynamic[visited_map_dynamic == 1] = [200, 200, 200]  # 방문 영역 - 회색
        background.set_data(color_array_dynamic)

        return path_line, robot_point, current_goal_scatter, background

    # 애니메이션 생성
    ani = animation.FuncAnimation(
        fig, animate, init_func=init,
        frames=num_frames, interval=30, blit=True, repeat=False
    )
    logger.info("Animation object created.")

    plt.show()
    logger.info("Visualization completed.")

def main():
    # 로그 레벨 설정
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger('main')
    logger.info("Starting visualization script.")

    # YAML 파일 경로 설정
    yaml_file_path = '/home/yjh/Doosan/Real_project_ws/Week8/self_cleaning_robot_ws/src/self_cleaning_robot/self_cleaning_robot/new_map.yaml'

    # YAML 파일 로드
    logger.info(f"Loading YAML file from {yaml_file_path}")
    with open(yaml_file_path, 'r') as file:
        map_data = yaml.safe_load(file)
    logger.info("YAML file loaded successfully.")

    # 맵 데이터 로드
    height = map_data['height']
    width = map_data['width']
    resolution = map_data['resolution']
    origin_x = map_data['origin']['position']['x']
    origin_y = map_data['origin']['position']['y']
    data = map_data['data']

    map_array = np.array(data).reshape(height, width)
    logger.info(f"Map array created with shape {map_array.shape}.")

    # 로봇 파라미터
    robot_radius = 0.175  # 로봇 반지름 (17.5 cm)
    start_x = 17.134  # 로봇 시작 X 좌표 (미터 단위)
    start_y = 1.320   # 로봇 시작 Y 좌표 (미터 단위)

    # Start Point를 맵 좌표로 변환
    start_row, start_col = world_to_map(start_x, start_y, origin_x, origin_y, resolution)
    logger.info(f"Start position converted to map coordinates ({start_row}, {start_col}).")

    # 시작점이 맵 범위 내에 있는지 검사
    if not (0 <= start_row < map_array.shape[0] and 0 <= start_col < map_array.shape[1]):
        logger.error(f"Start point ({start_x}, {start_y}) is outside the map boundaries.")
        raise ValueError(f"Start point ({start_x}, {start_y}) is outside the map boundaries.")

    # 시작점이 유효한 자유 공간인지 검사
    if map_array[start_row, start_col] != 0:
        logger.error(f"Start point ({start_x}, {start_y}) is not in a free space!")
        raise ValueError(f"Start point ({start_x}, {start_y}) is not in a free space!")

    # 연결된 자유 영역만 추출
    logger.info("Extracting connected region from start point.")
    region_map = extract_region(map_array, start_row, start_col)

    # `map_array` 업데이트 (벽 정보는 유지)
    updated_map_array = np.where(region_map == 0, 0, -1)  # 연결되지 않은 자유 공간은 -1
    updated_map_array[map_array == 100] = 100            # 벽 정보 유지

    # 장애물 확장 (Inflation) - 업데이트된 맵 기준
    logger.info("Marking inflated obstacles on updated map.")
    inflated_map = mark_inflated_obstacles(updated_map_array, robot_radius, resolution)

    # 영역 확인
    if np.sum(region_map == 0) == 0:
        logger.error("No reachable region found from the start point.")
        raise ValueError("No reachable region found from the start point.")

    # 커버리지 경로 생성
    logger.info("Generating coverage path on extracted region.")
    coverage_path, goal_points, visited_map = generate_coverage_path(
        map_array=updated_map_array,  # 업데이트된 맵 사용
        inflated_map=inflated_map,
        start_x=start_x,
        start_y=start_y,
        robot_radius=robot_radius,
        resolution=resolution,
        origin_x=origin_x,
        origin_y=origin_y
    )
    logger.info("Coverage path generated successfully.")

    # 시각화를 위한 `visited_map` 전달
    logger.info("Starting visualization.")
    visualize_coverage(
        map_array=updated_map_array,  # 최종 업데이트된 맵 사용
        inflated_map=inflated_map,
        path=coverage_path,
        goal_points=goal_points,
        resolution=resolution,
        origin_x=origin_x,
        origin_y=origin_y,
        start_x=start_x,
        start_y=start_y,
        robot_radius=robot_radius,
        visited_map=visited_map.copy()  # 실제 `visited_map`을 전달 (수정된 visualize_coverage에서 사용되지 않음)
    )
    logger.info("Visualization script completed.")

if __name__ == "__main__":
    main()
