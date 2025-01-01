import math
import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

def mark_inflated_obstacles(map_array: np.ndarray, robot_radius: float, resolution: float) -> np.ndarray:
    """
    로봇의 반경을 고려하여 장애물 주변을 확장합니다.
    확장된 영역은 -1로 표시됩니다.
    """
    H, W = map_array.shape
    inflate_cells = int(math.ceil(robot_radius / resolution))  # 확장 셀 수 계산
    inflated_map = map_array.copy()

    for r in range(H):
        for c in range(W):
            if map_array[r, c] == 100:  # 장애물
                for rr in range(max(0, r - inflate_cells), min(H, r + inflate_cells + 1)):
                    for cc in range(max(0, c - inflate_cells), min(W, c + inflate_cells + 1)):
                        if inflated_map[rr, cc] == 0:  # 확장할 수 있는 자유 영역만
                            # 유클리드 거리 기준으로 확장
                            if math.sqrt((rr - r) ** 2 + (cc - c) ** 2) <= inflate_cells:
                                inflated_map[rr, cc] = -1  # 갈 수 없는 영역으로 설정
    return inflated_map

def world_to_map(world_x: float, world_y: float, origin_x: float, origin_y: float, resolution: float) -> tuple:
    """
    월드 좌표 (world_x, world_y)를 맵 좌표 (row, col)로 변환합니다.
    """
    col = int((world_x - origin_x) / resolution)
    row = int((world_y - origin_y) / resolution)
    return row, col

def map_to_world(map_row: int, map_col: int, origin_x: float, origin_y: float, resolution: float) -> tuple:
    """
    맵 좌표 (row, col)를 월드 좌표 (world_x, world_y)로 변환합니다.
    """
    world_x = map_col * resolution + origin_x
    world_y = map_row * resolution + origin_y
    return world_x, world_y

def find_max_vertical_point(map_array: np.ndarray, current_row: int, current_col: int, direction: str) -> tuple:
    """
    특정 방향으로 이동하여 벽을 만나는 지점의 바로 직전 위치를 반환합니다.
    """
    H, W = map_array.shape
    if direction == 'down':
        for r in range(current_row + 1, H):
            if map_array[r, current_col] == -1:
                return (r - 1, current_col) if (r - 1) >= current_row else None
        return (H - 1, current_col)
    elif direction == 'up':
        for r in range(current_row - 1, -1, -1):
            if map_array[r, current_col] == -1:
                return (r + 1, current_col) if (r + 1) <= current_row else None
        return (0, current_col)
    elif direction == 'right':
        for c in range(current_col + 1, W):
            if map_array[current_row, c] == -1:
                return (current_row, c - 1) if (c - 1) >= current_col else None
        return (current_row, W - 1)
    elif direction == 'left':
        for c in range(current_col - 1, -1, -1):
            if map_array[current_row, c] == -1:
                return (current_row, c + 1) if (c + 1) <= current_col else None
        return (current_row, 0)
    else:
        logger.error(f"Unsupported direction: {direction}")
        return None

def move_right(map_array: np.ndarray, current_row: int, current_col: int, distance_cells: int) -> tuple:
    """
    현재 위치에서 오른쪽으로 distance_cells 만큼 이동한 지점을 반환합니다.
    """
    H, W = map_array.shape
    new_col = current_col + distance_cells
    if new_col >= W:
        return None
    else:
        return (current_row, new_col)

def mark_visited(visited_map: np.ndarray, map_row: int, map_col: int, robot_radius: float, resolution: float, map_array: np.ndarray):
    """
    특정 맵 셀을 중심으로 로봇 반경 내의 모든 셀을 방문한 것으로 마킹합니다.
    단, 벽과 안전 구역은 제외합니다.
    """
    H, W = visited_map.shape
    inflate_cells = int(math.ceil((robot_radius + 0.01) / resolution))

    for rr in range(max(0, map_row - inflate_cells), min(H, map_row + inflate_cells + 1)):
        for cc in range(max(0, map_col - inflate_cells), min(W, map_col + inflate_cells + 1)):
            dist_sq = (rr - map_row)**2 + (cc - map_col)**2
            if dist_sq <= inflate_cells**2:
                if map_array[rr, cc] == 0:  # 자유 공간인 경우만 방문한 것으로 마킹
                    visited_map[rr, cc] = 1
                    # 디버깅용 로그 (필요 시 활성화)
                    # logger.debug(f"Marked visited: ({rr}, {cc})")
                
def bresenham_line(row0, col0, row1, col1):
    """
    두 점 사이의 Bresenham 선 알고리즘을 사용하여 셀 좌표를 반환합니다.
    """
    cells = []
    d_row = abs(row1 - row0)
    d_col = abs(col1 - col0)
    s_row = 1 if row0 < row1 else -1
    s_col = 1 if col0 < col1 else -1
    err = d_col - d_row

    current_row, current_col = row0, col0

    while True:
        cells.append((current_row, current_col))
        if current_row == row1 and current_col == col1:
            break
        e2 = 2 * err
        if e2 > -d_row:
            err -= d_row
            current_col += s_col
        if e2 < d_col:
            err += d_col
            current_row += s_row

    return cells

def interpolate_points(start: tuple, end: tuple, resolution: float, origin_x: float, origin_y: float) -> list:
    """
    두 점 사이를 선형 보간하여 중간 지점을 생성합니다.
    반환값: List of (x, y) tuples
    """
    x1, y1 = start
    x2, y2 = end
    num_steps = int(math.ceil(math.hypot(x2 - x1, y2 - y1) / resolution)) * 100
    if num_steps == 0:
        return [start]
    step_x = (x2 - x1) / num_steps
    step_y = (y2 - y1) / num_steps
    return [(x1 + i * step_x, y1 + i * step_y) for i in range(1, num_steps + 1)]

def extract_region(map_array: np.ndarray, start_row: int, start_col: int) -> np.ndarray:
    """
    시작 위치에서 0으로 연결된 영역만을 추출하여 나머지는 -1로 표시한 새로운 맵을 생성합니다.
    """
    H, W = map_array.shape
    region_map = -np.ones_like(map_array, dtype=np.int8)  # 모든 셀을 -1로 초기화
    visited = np.zeros_like(map_array, dtype=np.uint8)    # 방문 여부를 기록

    if map_array[start_row, start_col] != 0:
        raise ValueError("시작 위치는 반드시 0이어야 합니다.")

    # BFS를 사용한 Flood Fill
    queue = [(start_row, start_col)]
    visited[start_row, start_col] = 1
    region_map[start_row, start_col] = 0

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 상, 하, 좌, 우

    while queue:
        row, col = queue.pop(0)

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc

            if 0 <= new_row < H and 0 <= new_col < W:  # 맵 경계를 벗어나지 않고
                if not visited[new_row, new_col] and map_array[new_row, new_col] == 0:
                    visited[new_row, new_col] = 1
                    region_map[new_row, new_col] = 0  # 연결된 영역을 유지
                    queue.append((new_row, new_col))

    return region_map

def find_corner(map_array, current_row, current_col, priority_directions, visited_map):
    """
    우선 순위 방향에 따라 가장 구석 위치를 탐색합니다.
    방문되지 않은 구석만 반환합니다.
    """
    logger.info(f"Finding corner starting at ({current_row}, {current_col}) with priority {priority_directions}")
    H, W = map_array.shape
    corner_row, corner_col = current_row, current_col

    for direction in priority_directions:
        while True:
            next_point = find_max_vertical_point(map_array, corner_row, corner_col, direction)
            if next_point is None:
                logger.debug(f"No further movement in direction {direction} from ({corner_row}, {corner_col}).")
                break

            next_row, next_col = next_point
            if (next_row < 0 or next_row >= H or next_col < 0 or next_col >= W or
                map_array[next_row, next_col] == -1 or visited_map[next_row, next_col] == 1):
                logger.debug(f"Invalid or already visited corner at ({next_row}, {next_col}) in direction {direction}.")
                break

            if (next_row, next_col) == (corner_row, corner_col):
                break

            corner_row, corner_col = next_row, next_col
            logger.debug(f"Moved to corner ({corner_row}, {corner_col}) in direction {direction}.")

    if visited_map[corner_row, corner_col] == 1:
        logger.warning(f"Corner at ({corner_row}, {corner_col}) already visited.")
        return None, None

    logger.info(f"Corner found at ({corner_row}, {corner_col}).")
    return corner_row, corner_col

def coverage_pass(current_row, current_col, direction_priority, origin_x, origin_y, resolution, 
                  inflated_map, visited_map, coverage_path, goal_points, robot_radius, map_array):
    """
    주어진 방향 우선순위에 따라 경로를 탐색하며 커버리지 패스를 수행합니다.
    """
    logger.info(f"Starting coverage pass at ({current_row}, {current_col}) with priority {direction_priority}")
    local_path = []
    current_x, current_y = map_to_world(current_row, current_col, origin_x, origin_y, resolution)
    local_path.append((current_x, current_y))
    coverage_path.append((current_x, current_y))
    mark_visited(visited_map, current_row, current_col, robot_radius, resolution, map_array)

    robot_diameter = 2 * robot_radius
    distance_cells = int(math.ceil(robot_diameter / resolution))

    while True:
        max_point = find_max_vertical_point(inflated_map, current_row, current_col, direction_priority)
        if max_point is None or inflated_map[max_point[0], max_point[1]] == -1:
            logger.info(f"No further valid points in direction {direction_priority} from ({current_row}, {current_col}).")
            break

        goal_row, goal_col = max_point
        if visited_map[goal_row, goal_col] == 1:
            logger.info(f"Goal point ({goal_row}, {goal_col}) already visited.")
            break

        goal_x, goal_y = map_to_world(goal_row, goal_col, origin_x, origin_y, resolution)
        goal_points.append((goal_x, goal_y))
        logger.debug(f"Goal point added at ({goal_x}, {goal_y}).")

        # 이전 위치와 목표 위치 사이의 모든 셀을 계산
        path_cells = bresenham_line(current_row, current_col, goal_row, goal_col)

        for cell_row, cell_col in path_cells:
            # 각 셀을 방문한 것으로 마킹
            mark_visited(visited_map, cell_row, cell_col, robot_radius, resolution, map_array)
            # 커버리지 경로에 추가
            world_x, world_y = map_to_world(cell_row, cell_col, origin_x, origin_y, resolution)
            if (world_x, world_y) not in coverage_path:
                coverage_path.append((world_x, world_y))

        # 현재 위치를 목표 위치로 업데이트
        current_row, current_col = goal_row, goal_col
        current_x, current_y = goal_x, goal_y
        local_path.append((current_x, current_y))
        logger.debug(f"Updated current position to ({current_row}, {current_col}).")

    logger.info("Coverage pass completed.")
    return local_path


def generate_coverage_path(map_array: np.ndarray, inflated_map: np.ndarray,
                          start_x: float, start_y: float,
                          robot_radius: float, resolution: float,
                          origin_x: float, origin_y: float) -> tuple:
    """
    지정된 로직에 따라 커버리지 경로를 생성합니다.
    """
    coverage_path = []
    goal_points = []
    visited_map = np.zeros_like(map_array, dtype=np.uint8)

    initial_row, initial_col = world_to_map(start_x, start_y, origin_x, origin_y, resolution)

    # 왼쪽 위 코너인지 확인 (예: 맵의 상단 근처)
    if initial_row <= int(map_array.shape[0] * 0.1) and initial_col <= int(map_array.shape[1] * 0.1):
        priority_dirs = ['up']
    else:
        priority_dirs = ['up', 'left']

    corner_row, corner_col = find_corner(inflated_map, initial_row, initial_col, priority_dirs, visited_map)
    if corner_row is not None and corner_col is not None:
        coverage_pass_path = coverage_pass(
            corner_row, corner_col, 'down', origin_x, origin_y, resolution, 
            inflated_map, visited_map, coverage_path, goal_points, robot_radius, map_array
        )
        coverage_path.extend(coverage_pass_path)

    # 초기 방향 설정
    current_direction = 'up'  # 첫 번째 패스 후 다음 패스는 'up'으로 설정

    while True:
        unvisited = np.argwhere((visited_map == 0) & (inflated_map == 0))
        if unvisited.size == 0:
            logger.info("No unvisited cells remaining.")
            break

        first_unvisited_row, first_unvisited_col = unvisited[0]
        
        # 특정 조건에서 방향 제한 (예: 맵의 왼쪽 위 근처)
        if first_unvisited_row <= int(map_array.shape[0] * 0.1) and first_unvisited_col <= int(map_array.shape[1] * 0.1):
            priority_dirs = ['up']
        else:
            if current_direction == 'up':
                priority_dirs = ['down', 'right']
            else:
                priority_dirs = ['up', 'right']

        corner_row, corner_col = find_corner(inflated_map, first_unvisited_row, first_unvisited_col, priority_dirs, visited_map)
        if corner_row is None or corner_col is None:
            logger.warning(f"No valid corner found starting from ({first_unvisited_row}, {first_unvisited_col}).")
            break

        coverage_pass_path = coverage_pass(
            corner_row, corner_col, current_direction, origin_x, origin_y, resolution, 
            inflated_map, visited_map, coverage_path, goal_points, robot_radius, map_array
        )
        coverage_path.extend(coverage_pass_path)

        # 방향 전환
        current_direction = 'up' if current_direction == 'down' else 'down'

    coverage_path = list(dict.fromkeys(coverage_path))  # 중복 제거
    logger.info("Coverage path generation completed.")
    return coverage_path, goal_points, visited_map

