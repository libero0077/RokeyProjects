# **SLAM 모델 기반 다중이용시설 로봇 주행 환경 장애물 인식 모델 개발**
## 프로젝트 기간 : 2024.12.24 ~ 2024.12.31

---

### 데모영상

*데모 영상을 추가해주세요.*

---

## 목차

- [개요](#개요)
- [주요 기능](#주요-기능)
- [아키텍처](#아키텍처)
- [구성 요소](#구성-요소)
  - [자율 탐색 및 맵핑 노드](#자율-탐색-및-맵핑-노드)
  - [자동 청소 알고리즘 노드](#자동-청소-알고리즘-노드)
  - [Visual Tracking 노드](#visual-tracking-노드)
- [디렉토리 구조](#디렉토리-구조)
- [설치](#설치)
- [사용법](#사용법)
- [개선 계획](#개선-계획)
- [기여](#기여)
- [라이선스](#라이선스)
- [연락처](#연락처)
- [추가 참고 자료](#추가-참고-자료)

---

## 개요

**"SLAM 모델 기반 다중이용시설 로봇 주행 환경 장애물 인식 모델 개발"** 프로젝트는 로봇 청소기의 자율 탐색, 맵핑, 청소, 및 Visual Tracking 기능을 통합적으로 구현하기 위해 진행되었습니다. 이 프로젝트는 ROS2를 기반으로 설계되었으며, 다음과 같은 주요 목표를 설정했습니다:

1. **자율 탐색 및 맵 작성**: 로봇(turtlebot4)이 환경을 탐색하며 실시간으로 Occupancy Grid 맵을 생성.
2. **자동 청소**: 탐색이 완료된 맵에서 최적의 경로를 따라 자율적으로 청소 작업 수행.
3. **Visual Tracking**: ORB 알고리즘과 BFMatcher를 활용하여 카메라로 주변 환경을 실시간으로 추적.

---

## 주요 기능

- **자율 탐색 및 맵핑**:
  - Frontier 탐색 알고리즘을 사용하여 로봇(turtlebot4)이 자율적으로 미탐색 영역(Frontier)을 탐지하고 이동.
  - Occupancy Grid 데이터를 활용하여 안전한 탐색 경로 생성.
  
- **자동 청소 알고리즘**:
  - 맵에서 방문하지 않은 셀을 탐색하고 경로를 생성하여 효율적인 청소 수행.
  - Bresenham 알고리즘을 사용하여 두 지점 간의 최적 경로 계산.

- **Visual Tracking**:
  - ORB 알고리즘으로 특징점 검출 및 매칭 수행.
  - Brute-Force (BF) 매처를 사용하여 실시간 환경 추적.
  - OpenCV를 통해 실시간 Tracking 결과를 오버레이 형태로 표시.
  - 잔상(페이드) 효과를 통해 이전 매칭 결과를 유지하면서 새로운 매칭 시각화.

---

## 아키텍처

시스템은 여러 상호 연결된 구성 요소로 구성되며, 각 구성 요소는 특정 기능을 담당하여 전체 시스템이 원활하게 동작하도록 합니다:

1. **자율 탐색 및 맵핑 노드**: 로봇이 환경을 탐색하고 Occupancy Grid 맵을 생성합니다.
2. **자동 청소 알고리즘 노드**: 생성된 맵을 기반으로 최적의 청소 경로를 계획하고 실행합니다.
3. **Visual Tracking 노드**: 로봇에 장착된 카메라를 통해 실시간으로 주변 환경을 추적합니다.

---

## 구성 요소

### 자율 탐색 및 맵핑 노드

- **파일**: `algorithm.py`
- **설명**: 터틀봇4가 자율탐색하며 맵핑을 수행할 수 있도록 구현한 노드입니다. Frontier 탐색 알고리즘을 사용하여 미탐색 영역을 탐지하고 목표 지점을 설정하여 이동합니다.
- **주요 기능**:
  - Occupancy Grid 토픽 데이터를 구독(subscribe)하여 맵 정보 업데이트
  - Goal 상태 모니터링 및 목표 도달 여부 확인
  - Frontier 탐지 및 유효한 목표 지점 선택
  - 목표 지점을 퍼블리시하여 로봇 이동 유도

### 자동 청소 알고리즘 노드

- **파일**: `coverage_algorithm.py`
- **설명**: 터틀봇4의 매핑이 완료된 후 자율 청소를 수행하기 위한 알고리즘을 구현한 노드입니다. 장애물 확장 처리, 경로 탐색, 방문 표시 등을 포함하여 효율적인 청소 경로를 생성합니다.
- **주요 기능**:
  - 로봇의 반경을 고려한 장애물 확장 처리
  - 월드 좌표와 맵 좌표 간 변환
  - Bresenham 알고리즘을 사용한 경로 탐색 및 방문 마킹
  - 커버리지 패스를 통한 전체 맵 커버

### Visual Tracking 노드

- **파일**: `visual_tracking_node.py`
- **설명**: 터틀봇4의 카메라 토픽을 구독하여 비주얼 트래킹을 수행하는 노드입니다. ORB 알고리즘과 BFMatcher 매처를 사용하여 실시간으로 주변 환경을 추적하고 시각화합니다.
- **주요 기능**:
  - 카메라 이미지 구독(subscribe) 및 OpenCV 이미지 변환
  - ORB 특징점 검출 및 디스크립터 생성
  - BFMatcher 매처를 사용한 특징점 매칭
  - 실시간 매칭 결과 오버레이 및 시각화

---

## 디렉토리 구조
```bash
self_cleaning_robot_ws
├── src
│   └── self_cleaning_robot
│       ├── package.xml
│       ├── resource
│       │   └── self_cleaning_robot
│       ├── self_cleaning_robot
│       │   ├── algorithm.py
│       │   ├── coverage_algorithm.py
│       │   ├── visual_tracking_node.py
│       │   ├── map.pgm
│       │   ├── map.yaml
│       │   ├── slam.yaml
│       │   ├── simul_auto_cleaning.py
│       │   └── temp_map.yaml
│       ├── setup.cfg
│       ├── setup.py
│       └── test
│           ├── test_copyright.py
│           ├── test_flake8.py
│           └── test_pep257.py
└── [summary]CleaningRobotProject.pdf
```
## 설치

### 필수 사항

- **운영체제**: Ubuntu 22.04  
- **Python 버전**: Python 3.7 이상  
- **필수 라이브러리**:
  - `ros2 (humble)`
  - `rclpy`
  - `PyQt5`
  - `sqlite3`
  - `nav2_msgs`
  - `geometry_msgs`
  - `std_msgs`
  - `rviz`
  - 기타 프로젝트에 필요한 Python 패키지

### 설치 단계

1. **워크스페이스 생성 및 의존성 설치:**
    ```bash
    mkdir ~/ros2_ws
    git clone https://github.com/libero0077/RokeyProjects
    cd RokeyProjects/CleaningRobotProject/self_cleaning_robot_ws
    colcon build
    source install/setup.bash
    ```

2. **시스템 종속성 설치:**
    ```bash
    sudo apt update
    sudo apt install python3-pyqt5 python3-rosdep python3-rosinstall python3-rosinstall-generator python3-wstool build-essential
    sudo apt install ros-humble-turtlebot4* ros-humble-nav2-bringup
    ```

3. **필수 Python 패키지 설치:**
    ```bash
    pip install opencv-python numpy
    ```

---

## 사용법

### 1. **ROS2 노드 및 런치 파일 실행**

각각의 노드를 별도의 터미널에서 실행해야 합니다. ROS2 환경이 설정되어 있는지 확인하세요.

- **로봇 시각화 노드 실행** :
    ```bash
    ros2 launch turtlebot4_viz view_robot.launch.py
    ```

- **SLAM 노드 실행** :
  - turtlebot4를 자율 mapping할 공간에 적합하게 slam.yaml 파일을 수정해주세요.

    ```bash
    ros2 launch turtlebot4_navigation slam.launch.py params:={parameter file}
    ```

- **네비게이션 노드 실행** :
  - turtlebot4를 자율 mapping할 공간에 적합하게 nav2.yaml 파일을 수정해주세요.

    ```bash
    ros2 launch turtlebot4_navigation nav2.launch.py params_file:='{parameter file}'
    ```

- **맵핑 노드 실행** (`algorithm.py`):
    ```bash
    ros2 run self_cleaning_robot explorer
    ```

- **Visual Tracking 노드 실행** (`visual_tracking_node.py`):
    ```bash
    ros2 run self_cleaning_robot visual_tracking_node
    ```

- **청소 알고리즘 노드 실행** (`coverage_algorithm.py`):
  - 알고리즘 시뮬레이션 파일은 "coverage_visualization.py" 파일을 실행해주셔야 합니다.
    ```bash
    python3 coverage_visualization.py
    ```

### 2. **실행 절차**

1. `view_robot.launch.py`를 실행하여 로봇의 상태를 시각화합니다.
2. `slam.launch.py`를 실행하여 SLAM을 통해 맵핑 작업을 수행하기 위한 준비를 합니다.
3. `nav2.launch.py`를 실행하여 네비게이션 작업을 수행하며 최적 경로를 따라 이동하기 위한 준비를 합니다.
4. `algorithm.py` 를 실행하여 프론티어(미탐지 지역)를 계산하고 필터링을 통해 최적의 프론티어를 저장합니다. 저장된 프론티어들에서 랜덤으로 목표지점으로 설정하여 로봇(turtlebot4)이 해당 지점으로 이동하도록 제어합니다. 
5. `visual_tracking_node.py`를 실행하여 실시간 Visual Tracking 결과를 모니터링 합니다.
6. `coverage_algorithm.py`를 실행하여 자율 청소를 수행합니다.

---

## 개선 계획

현재 시스템은 기본적인 자율 탐색, 맵핑, 청소 및 Visual Tracking 기능을 갖추고 있지만, 다음과 같은 개선을 통해 더욱 강력하고 효율적인 시스템으로 발전시킬 수 있습니다:

1. **청소 알고리즘 통합**:
   - **실제 청소 알고리즘 적용 부족**: 현재 청소 경로 알고리즘은 시뮬레이션 환경에서만 검증되었으며, 실제 로봇 하드웨어에서 통합적으로 적용되지 못한 상태입니다. 이를 보완하기 위해 청소 알고리즘을 실제 로봇 제어 시스템과 완전하게 통합하고, 하드웨어 기반 테스트를 통해 성능을 검증할 필요가 있습니다.
   - 
2. **청소 효율성 향상**:
   - **청소 경로 최적화**: 청소 경로 최적화 알고리즘을 추가 구현하여 에너지 효율을 높이고 청소 시간을 단축합니다.

3. **Visual Tracking 강화**:
   - **동적 키포인트 조정**: 다양한 환경에서 정확도를 향상시키기 위해 키포인트 수를 동적으로 조정합니다.
   - **추가 매칭 알고리즘 도입**: BFMatcher 외의 매칭 알고리즘을 도입하여 매칭 정확도를 높입니다.


---

## 기여

이 프로젝트를 함께 진행한 팀원들의 기여도는 다음과 같습니다:

- 류재준 [libero0077](https://github.com/libero0077) : 청소 알고리즘 개발 / 자율 탐색 튜닝 전략 검토
- 양준혁 [Y6HYUK](https://github.com/Y6HYUK) : Visual Tracking 알고리즘 개발 / 자율 탐색 알고리즘 개발 및 튜닝
- 이상우 [leesw1357](https://github.com/leesw1357) : 청소 알고리즘 개발
- 김주원 [juwon407](https://github.com/juwon407) : 자율 탐색 알고리즘 개발 및 튜닝 / 청소 알고리즘 개발 

---

## 라이선스

이 프로젝트는 [MIT License](LICENSE)를 따릅니다.

---

## 연락처

문의 사항이나 지원이 필요하시면 아래 연락처로 연락주세요:

- **이름**: 양준혁
- **GitHub**: [Y6HYUK](https://github.com/Y6HYUK)

---

## 추가 참고 자료

- [ROS2 공식 문서](https://docs.ros.org/en/humble/index.html)
- [NAV2 공식 문서](https://navigation.ros.org/)
- [PyQt5 공식 문서](https://www.riverbankcomputing.com/static/Docs/PyQt5/)
- [SQLite 공식 문서](https://www.sqlite.org/docs.html)
- [OpenCV 공식 문서](https://docs.opencv.org/)
- [GitHub Actions](https://github.com/features/actions)

---

