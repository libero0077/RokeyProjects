import math
import cv2
import numpy as np
import itertools

import os

class DefectDetector:
    def __init__(self, data):
        # 데이터 유효성 확인 및 초기화
        if 'objects' not in data or not isinstance(data['objects'], list):
            raise ValueError("데이터 형식이 잘못되었습니다. 'objects' 키가 존재하고 리스트 형태여야 합니다.")
        self.data = data
        self.coordinates_by_class = {}  # 그룹화 된 좌표들
        self.center_coordinates_by_class = {}   # 중심좌표로 변환된 좌표
        self.sorted_dhole_coordinates = []  # 정렬된 중심 좌표
        self.pcb_orientation = ""
        self.distances = [] 
        self.homography_matrix = None   # 계산된 호모그래피 행렬
        self.transformed_coordinates = []   # 호모그래피 변환된 중심 좌표들
        self.__main__()

    def __main__(self):
        # 데이터 처리
        self.process_data() # 데이터 처리 - 클래스별 좌표 그룹화, 각 좌표를 중심 좌표로 변환
        # 피코를 감지 했는지 확인
        # if 'RASPBERRY PICO' not in self.coordinates_by_class or len(self.coordinates_by_class['RASPBERRY PICO']) == 0:
        #     print("결과: 불량 (RASPBERRY PICO를 찾을 수 없음)")
        #     return  False
        # DHOLE의 수 확인
        if 'DHOLE' not in self.coordinates_by_class or len(self.coordinates_by_class['DHOLE']) < 4:
            print("홀의 갯수가 4개 미만입니다. 불량 처리합니다.")
            return False, ["HOLE FAILE"]
        
        self.sorted_dhole_coordinates = self.sort_coordinates() # 중심 좌표를 시계방향 순으로 정렬
        print(f"정렬된 홀 좌표 : {self.sorted_dhole_coordinates}")

        self.pcb_orientation = self.check_orientation() # 홀 좌표를 바탕으로 pcb의 회전을 확인
        print(f"PCB 방향: {self.pcb_orientation}")

        if self.pcb_orientation == "horizontal":    # 방향이 가로이면
            self.sorted_dhole_coordinates = self.convert_to_vertical(self.sorted_dhole_coordinates)
            print(f"pcb의 방향이 가로입니다. \n 회전된 좌표 : {self.sorted_dhole_coordinates}")

        self.calculate_homography() # 호모그래피 행렬을 계산
        self.transformed_coordinates = self.transform_all_class_coordinates() # 모든 클래스의 중심 좌표를 호모그래피 변환
        print(self.transformed_coordinates)

        # 필수 클래스 확인
        if not self.check_class_counts():
            print("클래스 확인 실패: 불량 처리합니다.")
            return False, ["CLASS CHECK FAILE"]

        # 거리 계산 및 조건 확인
        result = self.calculate_distances_between_classes(self.transformed_coordinates)
        if not result:
            print("거리 계산 실패: 불량 처리합니다.")
            return False, ["DISTANCE CHECK FAILE"]
        
        # 정상 처리
        print("모든 조건을 만족했습니다. 정상 처리합니다.")
        return True, ["-"]

    def process_data(self):
        # 데이터 처리 - 클래스별 좌표 그룹화, 각 좌표를 중심 좌표로 변환
        self.extract_coordinates_by_class() # 클래스별 좌표 그룹화
        print(f"그룹화된 클래스 좌표 : {self.coordinates_by_class}")
        self.convert_to_center_coordinates()    # 각 좌표를 중심 좌표로 변환
        print(f"객체 중심 좌표 : {self.center_coordinates_by_class}")

    def extract_coordinates_by_class(self): # 클래스별 좌표 그룹화
        # 결과를 저장할 딕셔너리 초기화
        self.coordinates_by_class = {}

        # 데이터를 순회하면서 클래스별로 좌표 저장
        for obj in self.data['objects']:
            # 각 객체에 필요한 키가 모두 있는지 확인
            if 'class' not in obj or 'box' not in obj:
                raise ValueError("각 객체는 'class'와 'box' 키를 포함해야 합니다.")

            class_name = obj['class']
            box_coordinates = obj['box']
            score = obj['score']

            # box가 리스트 형태이고 정확히 4개의 요소를 가지고 있는지 확인
            if not isinstance(box_coordinates, list) or len(box_coordinates) != 4:
                raise ValueError("'box'는 4개의 요소를 가진 리스트여야 합니다.")
            
            # DHOLE 클래스의 score를 필터링 (DHOLE 개수가 5 이상인 경우만)
            if class_name == 'DHOLE' and len([obj for obj in self.data['objects'] if obj['class'] == 'DHOLE']) >= 5:
                if score < 0.75:
                    print(f"무시됨: {class_name} 객체의 점수가 0.8 미만입니다. 점수: {score:.2f}")
                    continue

            self.filter_dholes()

            # 해당 클래스가 딕셔너리에 없으면 리스트 초기화
            if class_name not in self.coordinates_by_class:
                self.coordinates_by_class[class_name] = []

            # 클래스 이름에 해당하는 리스트에 좌표 추가
            self.coordinates_by_class[class_name].append(box_coordinates)

    def filter_dholes(self):
        """
        HOLE이 5개 이상일 때, 일정 위치에 몰려있는 경우 가장 높은 score를 가진 HOLE 하나만 남김.
        """
        if 'DHOLE' not in self.coordinates_by_class or len(self.coordinates_by_class['DHOLE']) < 5:
            return  # HOLE이 6개 미만이면 작업하지 않음

        print(f"HOLE이 5개 이상 감지되었습니다. 필터링을 시작합니다.")

        # 거리 기준 (예: 50 픽셀 이내를 동일 그룹으로 간주)
        threshold = 50  

        # DHOLE 좌표와 scores를 가져옴
        dholes = self.coordinates_by_class['DHOLE']
        scores = [obj['score'] for obj in self.data['objects'] if obj['class'] == 'DHOLE']

        # 그룹화: 가까운 좌표끼리 묶음
        groups = []
        for i, hole in enumerate(dholes):
            added = False
            for group in groups:
                if any(self.calculate_distance(hole, member) <= threshold for member in group):
                    group.append((hole, scores[i]))
                    added = True
                    break
            if not added:
                groups.append([(hole, scores[i])])

        print(f"그룹화된 DHOLE: {groups}")

        # 각 그룹에서 가장 높은 score를 가진 HOLE만 남김
        filtered_dholes = []
        for group in groups:
            best_hole = max(group, key=lambda x: x[1])  # score 기준으로 최고점 선택
            filtered_dholes.append(best_hole[0])  # 좌표만 저장

        print(f"필터링된 DHOLE 좌표: {filtered_dholes}")

        # 필터링된 DHOLE로 갱신
        self.coordinates_by_class['DHOLE'] = filtered_dholes

    def convert_to_center_coordinates(self):    # 중심 좌표 계산
        # 중심 좌표를 저장할 딕셔너리 초기화
        self.center_coordinates_by_class = {}

        # 클래스별로 좌표를 순회하며 중심 좌표 계산
        for class_name, boxes in self.coordinates_by_class.items():
            self.center_coordinates_by_class[class_name] = []
            for box in boxes:
                x_min, y_min, x_max, y_max = box
                # 중심 좌표 계산
                x_center = (x_min + x_max) / 2
                y_center = (y_min + y_max) / 2
                self.center_coordinates_by_class[class_name].append([x_center, y_center])

    def sort_coordinates(self): # 홀 좌표 시계 방향 정렬
        # DHOLE 클래스의 중심 좌표를 왼쪽 위부터 시계 방향으로 정렬
        if 'DHOLE' not in self.center_coordinates_by_class:
            return []

        dholes = self.center_coordinates_by_class['DHOLE']
        # 1. y값 기준 정렬 (y값이 같으면 x값 기준으로 정렬)
        sorted_coords = sorted(dholes, key=lambda p: (p[1], p[0]))
        # 2. 위쪽 그룹 (y값이 작은 2개)와 아래쪽 그룹 (y값이 큰 2개) 분리
        top_coords = sorted_coords[:2]  # 위쪽 그룹
        bottom_coords = sorted_coords[2:]  # 아래쪽 그룹
        # 3. 각 그룹에서 x값 기준 정렬
        top_coords = sorted(top_coords, key=lambda p: p[0])  # 왼쪽 → 오른쪽
        bottom_coords = sorted(bottom_coords, key=lambda p: p[0], reverse=True)  # 오른쪽 → 왼쪽
        # 4. 순서: 왼쪽 위, 오른쪽 위, 오른쪽 아래, 왼쪽 아래
        return [top_coords[0], top_coords[1], bottom_coords[0], bottom_coords[1]]
    
    def check_orientation(self):    # pcb의 방향을 확인
        if len(self.sorted_dhole_coordinates) != 4:
            raise ValueError("PCB 방향을 확인하려면 4개의 정렬된 DHOLE 좌표가 필요합니다.")
        left_top = self.sorted_dhole_coordinates[0]
        right_top = self.sorted_dhole_coordinates[1]
        left_bottom = self.sorted_dhole_coordinates[3]
        width = abs(right_top[0] - left_top[0])
        height = abs(left_bottom[1] - left_top[1])
        return "horizontal" if width > height else "vertical"
    
    def convert_to_vertical(self, sorted_coordinates):    # 홀 정렬을 가로에서 세로로 변경
        # 순서 변경: [왼쪽 아래, 왼쪽 위, 오른쪽 위, 오른쪽 아래]
        return [
            sorted_coordinates[3],  # 왼쪽 아래
            sorted_coordinates[0],  # 왼쪽 위
            sorted_coordinates[1],  # 오른쪽 위
            sorted_coordinates[2]   # 오른쪽 아래
        ]

    def calculate_homography(self):
        """호모그래피 변환을 계산"""
        if len(self.sorted_dhole_coordinates) != 4:
            raise ValueError("호모그래피 변환을 위해서는 정확히 4개의 좌표가 필요합니다.")

        # 원본 좌표 (예: DHOLE의 중심 좌표)
        src_points = np.array(self.sorted_dhole_coordinates, dtype=np.float32)

        # 목적 좌표 (예: 변환하고자 하는 좌표)
        dst_points = np.array([[0, 50], [20, 50], [20, 0], [0, 0]], dtype=np.float32)

        # 호모그래피 행렬 계산
        self.homography_matrix, _ = cv2.findHomography(src_points, dst_points)
        print(f"Homography Matrix : {self.homography_matrix}")

    def transform_point(self, point):
        """호모그래피 변환을 사용하여 주어진 좌표를 변환"""
        if self.homography_matrix is None:
            raise ValueError("호모그래피 행렬이 계산되지 않았습니다. 먼저 calculate_homography를 호출하세요.")

        # 입력 좌표를 변환을 위해 호모그래피 변환 행렬에 맞게 배열로 변환
        point_array = np.array([[point]], dtype=np.float32)
        # 호모그래피 변환 적용
        transformed_point = cv2.perspectiveTransform(point_array, self.homography_matrix)
        # 변환된 좌표 반환 (소수점 셋째 자리에서 반올림하고 정수형으로 변환)
        return [int(round(transformed_point[0][0][0], 3) * 1000), int(round(transformed_point[0][0][1], 3) * 1000)]

    def transform_all_class_coordinates(self):
        """모든 클래스의 중심 좌표들을 변환하여 반환"""
        transformed_coordinates = {}
        for class_name, coordinates in self.center_coordinates_by_class.items():
            transformed_coordinates[class_name] = []
            for point in coordinates:
                transformed_point = self.transform_point(point)
                transformed_coordinates[class_name].append(transformed_point)
        return transformed_coordinates

    def check_class_counts(self):
        required_classes = ['BOOTSEL', 'OSCILLATOR', 'USB', 'CHIPSET']
        missing_classes = []

        # 필요한 클래스 중 누락된 클래스 찾기
        for class_name in required_classes:
            if class_name not in self.coordinates_by_class or len(self.coordinates_by_class[class_name]) < 1:
                print(f"{class_name} 클래스가 감지되지 않았습니다.")
                missing_classes.append(class_name)

        # 누락된 클래스가 있으면 대체 객체 탐색
        if missing_classes:
            print("누락된 클래스를 대체할 객체를 탐색합니다...")
            self.find_replacement_for_missing_classes(missing_classes)

        # 다시 모든 클래스 확인
        for class_name in required_classes:
            if class_name not in self.coordinates_by_class or len(self.coordinates_by_class[class_name]) < 1:
                print(f"결과: 불량 ({class_name} 클래스가 없거나 개수가 1 미만)")
                return False

        print("결과: 정상 (모든 클래스가 1개 이상 존재)")
        return True
    
    def find_replacement_for_missing_classes(self, missing_classes):
        """
        누락된 클래스에 대해 대체 객체를 탐색.
        """
        # 정방향 예상 범위
        upright_ranges = {
            'BOOTSEL': ([3113, 4079], [39103, 40066]),
            'OSCILLATOR': ([5377, 6652], [15129, 15925]),
            'USB': ([8932, 10680], [50137, 51234]),
            'CHIPSET': ([9354, 10611], [23970, 25098])
        }

        # 역방향 예상 범위
        upside_down_ranges = {
            'BOOTSEL': ([15698, 16690], [10064, 11062]),
            'OSCILLATOR': ([13306, 14817], [34176, 35027]),
            'USB': ([8951, 10690], [-1016, -105]),
            'CHIPSET': ([9355, 10776], [24979, 26036])
        }

        # 제외할 클래스
        excluded_classes = {'DHOLE', 'RASPBERRY PICO'}

        for missing_class in missing_classes:
            print(f"=== {missing_class} 대체 탐색 시작 ===")

            # 예상 범위 가져오기
            upright_ll, upright_ul = upright_ranges.get(missing_class, (None, None))
            upside_down_ll, upside_down_ul = upside_down_ranges.get(missing_class, (None, None))

            candidate_object = None
            min_distance = float('inf')

            # 감지된 객체를 처리
            for obj in self.data['objects']:
                class_name = obj.get('class')
                if class_name in excluded_classes:
                    print(f"{class_name} 클래스는 대체 탐색에서 제외됩니다.")
                    continue  # 제외 클래스 건너뜀

                # if class_name != missing_class:
                #     print(f"{class_name}: 다른 클래스이므로 건너뜁니다.")
                #     continue

                # 'score' 키 확인
                if 'score' not in obj:
                    print(f"건너뜀: {class_name} - 'score' 키가 없음. 객체 데이터: {obj}")
                    continue

                score = obj['score']
                if score > 0.7:
                    print(f"건너뜀: {class_name} - 점수가 0.7 초과. 점수: {score:.2f}")
                    continue

                # 감지된 객체가 2개 이상인 경우만 검사
                detected_objects = [o for o in self.data['objects'] if o.get('class') == class_name]
                if len(detected_objects) < 2:
                    print(f"{class_name}: 감지된 객체가 2개 미만입니다. 건너뜁니다.")
                    continue

                # 변환된 좌표 계산
                if 'box' not in obj:
                    print(f"{class_name}: 'box' 정보가 없어 건너뜁니다.")
                    continue
                x_min, y_min, x_max, y_max = obj['box']
                center_x, center_y = (x_min + x_max) / 2, (y_min + y_max) / 2
                transformed_point = self.transform_point([center_x, center_y])
                print(f"{class_name}: 원본 좌표 [{center_x}, {center_y}] → 변환된 좌표 {transformed_point}")


                # 정방향 범위 확인
                if upright_ll and upright_ll[0] <= transformed_point[0] <= upright_ul[0] and upright_ll[1] <= transformed_point[1] <= upright_ul[1]:
                    direction = "정방향"
                    print(f"{class_name}: 정방향 범위 내 객체 발견. 좌표: {transformed_point}")
                # 역방향 범위 확인
                elif upside_down_ll and upside_down_ll[0] <= transformed_point[0] <= upside_down_ul[0] and upside_down_ll[1] <= transformed_point[1] <= upside_down_ul[1]:
                    direction = "역방향"
                    print(f"{class_name}: 역방향 범위 내 객체 발견. 좌표: {transformed_point}")
                else:
                    print(f"건너뜀: {class_name} - 좌표가 범위 밖. 변환된 좌표: {transformed_point}")
                    continue  # 범위 내에 없으면 건너뜁니다.

                # PCB 중심 좌표 계산
                pcb_center_x = (self.sorted_dhole_coordinates[0][0] + self.sorted_dhole_coordinates[2][0]) / 2
                pcb_center_y = (self.sorted_dhole_coordinates[0][1] + self.sorted_dhole_coordinates[2][1]) / 2
                pcb_center = [pcb_center_x, pcb_center_y]

                # PCB 중심과의 거리 계산
                distance = math.sqrt((pcb_center[0] - transformed_point[0])**2 + (pcb_center[1] - transformed_point[1])**2)
                print(f"범위 내 객체 발견: {class_name}, 방향: {direction}, 좌표: {transformed_point}, 중심 거리: {distance}")

                if distance < min_distance:
                    print(f"가장 적합한 객체 갱신: {class_name}, 방향: {direction}, 변환된 좌표: {transformed_point}, 점수: {score:.2f}")
                    min_distance = distance
                    candidate_object = transformed_point

            # 대체 객체 추가
            if candidate_object:
                print(f"대체 객체로 {missing_class} 추가: {candidate_object}")
                if missing_class not in self.coordinates_by_class:
                    self.coordinates_by_class[missing_class] = []
                self.coordinates_by_class[missing_class].append(candidate_object)
            else:
                print(f"{missing_class}의 대체 객체를 찾을 수 없습니다.")

    def calculate_distances_between_classes(self, transformed_coordinates, output_folder="class_distances"):
        print("\n=== 클래스 간 거리 계산 ===")
        distance_criteria = {
            tuple(sorted(['BOOTSEL', 'USB'])): {'LL': 11877, 'UL': 13632},
            tuple(sorted(['CHIPSET', 'BOOTSEL'])): {'LL': 15190, 'UL': 17323},
            tuple(sorted(['CHIPSET', 'OSCILLATOR'])): {'LL': 8639, 'UL': 11217},
            tuple(sorted(['CHIPSET', 'USB'])): {'LL': 25084, 'UL': 27132},
            tuple(sorted(['OSCILLATOR', 'BOOTSEL'])): {'LL': 23289, 'UL': 25047},
            tuple(sorted(['OSCILLATOR', 'USB'])): {'LL': 34296, 'UL': 36464},
        }

        # 모든 쌍을 검사하여 최종적으로 통과 여부를 결정
        all_within_threshold = True

        for (class1, coords1), (class2, coords2) in itertools.combinations(transformed_coordinates.items(), 2):
            key = tuple(sorted([class1, class2]))  # 정렬된 키 생성
            if key in distance_criteria:
                LL, UL = distance_criteria[key]['LL'], distance_criteria[key]['UL']
                pair_within_threshold = False  # 특정 클래스 쌍의 조건 만족 여부

                # 두 클래스의 좌표를 모두 비교
                for point1 in coords1:
                    for point2 in coords2:
                        distance = self.calculate_distance(point1, point2)
                        if LL <= distance <= UL:
                            pair_within_threshold = True
                            print(f"{class1} ({point1}) ↔ {class2} ({point2}): 거리 = {distance:.2f}, 기준 = {LL} ~ {UL} (정상)")
                            break  # 하나라도 조건을 만족하면 다른 비교는 건너뜀
                    if pair_within_threshold:
                        break  # 이미 조건을 만족했으므로 더 이상 비교하지 않음
                
                if not pair_within_threshold:
                    print(f"{class1} ↔ {class2}: 기준 미달 (이상) 거리 = {distance:.2f}, 기준 = {LL} ~ {UL}")
                    all_within_threshold = False
            else:
                print(f"{class1} ↔ {class2}: 기준 없음 (검사 생략)")

        if all_within_threshold:
            print("결과: 정상 (모든 클래스 간 조건 만족)")
            return True  # 정상인 경우 True 반환
        else:
            print("결과: 불량 (일부 클래스 간 조건 미달)")
            return False  # 불량인 경우 False 반환
    
    def calculate_distance(self, point1, point2):
        return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)