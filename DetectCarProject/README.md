# AMR 기반 음주 단속 회피 차량 추적 시스템

## 프로젝트 기간 : 2024.11.12 ~ 2024.11.18

------------------------------------------

### 데모영상

- AMR노드 실행 영상 : 추후 업로드할 예정입니다.
- GUI 실행 영상 : 추후 업로드할 예정입니다.
- AMR 복귀 영상


![Detect_car_amr_home](https://github.com/user-attachments/assets/d77e5811-1ce5-48b2-9151-6662d913404d)


------------------------------------------


### 


## 목차

- [개요](#개요)
- [주요 기능](#주요-기능)
- [아키텍처](#아키텍처)
- [구성 요소](#구성-요소)
  - [중앙 감지 노드](#중앙-감지-노드)
  - [모니터링 노드](#모니터링-노드)
  - [자율 추적 노드(AMR)](#자율-추적-노드(AMR))
- [디렉토리 구조](#디렉토리-구조)  
- [추적차량 판단 알고리즘](#추적차량-판단-알고리즘)
- [설치](#설치)
- [사용법](#사용법)
- [개선 계획](#개선-계획)
- [기여](#기여)
- [라이선스](#라이선스)
- [연락처](#연락처)
- [추가 참고 자료](#추가-참고-자료)

## 개요

**AMR 기반 음주 단속 회피 차량 추적 시스템**은 인공지능과 자율 기술을 활용하여 음주 단속 중 발생하는 도주 차량을 실시간으로 감지하고 추적하는 AMR(Autonomous Mobile Robot)기반 통합 솔루션입니다. 이 시스템은 음주운전 단속 현장에서 도주 차량을 실시간으로 감지하고 자율적으로 추적하여 음주운전 사고를 줄이고 단속의 효율성을 높입니다.PyQt로 구축된 모니터링 대시보드를 통해 실시간으로 추적 상황과 경고 알림을 모니터링할 수 있으며, YOLO 기반의 객체 탐지 알고리즘을 통해 도주 차량을 신속하고 정확하게 식별합니다. 또한 데이터를 체계적으로 기록하여 단속 프로세스의 효율성과 안전성을 향상시킵니다.

## 주요 기능

- **자율 네비게이션:** AMR은 최단 거리로 이동하며 자율적으로 순찰하고, 도주 차량 탐지 시 실시간 경로 최적화를 수행합니다
- **차량 감지 및 추적:** 도주 차량의 좌표를 실시간으로 분석하고 추적하며, 데이터를 중앙 시스템에 전송합니다.
- **위협 탐지 및 대응:** 도주 차량 탐지 시 즉시 중앙 제어 센터로 경고 메시지를 전송합니다.
- **실시간 모니터링:** 단속 화면 및 차량 추적 상황을 실시간으로 모니터링할 수 있는 대시보드를 제공합니다
- **데이터 관리:** MySQL을 사용하여 도주 차량의 추적 영상은 1주일간 보관하며 도주 차량의 신원 정보 및 도주 시각과 경과 시간 데이터는 1년간 저장합니다

## 아키텍처

시스템은 여러 상호 연결된 구성 요소로 구성되며, 각 구성 요소는 특정 기능을 담당하여 전체 시스템이 원활하게 동작하도록 합니다

1. **중앙 감지 모듈**: 카메라 작동, 실시간 데이터 처리 및 저장, 분석 기능과 모듈 간 데이터 송수신 기능을 담당합니다
2. **모니터링 모듈**: 중앙 감지 모듈에서 받은 데이터를 시각화하고, 사용자의 수동 제어(예: 추적 종료)를 중앙 감지 모듈로 전송합니다.
3. **자율 추적 모듈(AMR)**: 전달 받은 좌표로의 자율 추적, 카메라 감시를 수행하고 추적 상황과 이미지 데이터를 중앙 감지하며 모듈로 송신하는 기능을 담당합니다.

## 구성 요소

### 중앙 감지 노드

- **파일:** `dual_image_publisher.py`
- **설명:**  ROS2 (Robot Operating System 2)환경에서 동작하는 카메라 퍼블리셔 노드이며, USB 카메라로부터 이미지를 캡처하고 이를 압축하여 ROS2 토픽으로 발행합니다.
- **주요 기능:**
  - USB 카메라를 사용하여 실시간으로 이미지를 캡처
  - 캡처된 이미지는 640x480 크기로 리사이징
  - 캡처 및 압축된 이미지는 두 개의 별도 토픽으로 발행('/camera/image1/compressed', '/camera/image2/compressed')
  - JPEG 형식으로 압축되며, 압축 품질은 80으로 설정

### 모니터링 노드

- **파일:** `ui_camera_subscriber.py`
- **설명:** 중앙 감지 노드의 카메라로부터 이미지를 받아 처리하고 객체 탐지 및 추적 기능을 수행하며, 그래픽 사용자 인터페이스(GUI)를 통해 결과를 표시합니다.
- **주요 기능:**
  - 이미지 처리: 두 개의 카메라 토픽(/camera/image1/compressed, /webcam/yolo/compressed_image)을 구독
  - 객체 탐지: YOLOv8 모델을 사용하여 실시간 객체 탐지 및 추적을 수행
  - 그래픽 사용자 인터페이스(GUI): PyQt5를 사용했으며 두 개의 카메라 피드를 동시에 표시하고 상태 표시, 시간 정보, 제어 버튼 등을 포함
  - 객체 추적 및 상태 관리: 탐지된 객체## 디렉토리 구조에 고유 ID를 할당하고 추적을 진행, 객체의 상태(내부, 통과, 도주 등)를 관리
  - 좌표 변환 및 영역 설정: 이미지 좌표를 실제 맵 좌표로 변환하는 기능을 제공, 사용자가 GUI를 통해 카메라 좌표 보정 및  단속 영역을 설정
  - 시간 추적 및 로깅: 단속 시작 시간, 경과 시간, 도주 시간 등을 추적하고 표시
  
### 자율 추적 노드(AMR)

- **파일:** `random_position_publisher.py`
- **설명:** ROS2 (Robot Operating System 2)환경에서 동작하며, 로봇의 이동 경로를 제어하기 위한 웨이포인트를  단계별로 생성하고 퍼블리시합니다.
- **주요 기능:**
  - 웨이포인트 생성: 시작 위치와 최종 위치 사이에 지정된 수의 중간 웨이포인트를 생성
  - 단계별 이동 제어: 초기 위치, 중간 위치, 웨이포인트, 최종 위치로 순차적으로 이동하는 단계를 관리
  - 목표 위치 퍼블리시: 현재 단계에 따라 적절한 목표 위치를 PoseStamped 메시지 형태로 퍼블리시
  - 대기 시간 관리: 특정 위치(예: 두 번째 위치)에서 지정된 시간 동안 대기
  - 방향 계산: 웨이포인트 간 이동 시 로봇의 방향을 자동으로 계산하여 설정

- **파일:** `turtlebot_subscriber.py`
- **설명:** `random_position_publisher.py`의 로봇의 이동 경로를 제어하기 위해 퍼블리쉬한 웨이포인트를 구독하고 처리합니다.
- **주요 기능:**
  - 웨이포인트 수신: '/goal_pose' 토픽을 통해 PoseStamped 메시지 형태로 웨이포인트를 수신
  - 네비게이션 목표 퍼블리시: 수신된 웨이포인트를 '/navigate_to_pose' 토픽으로 퍼블리시하여 네비게이션 스택에 전달


## 디렉토리 구조

```bash

└── src
    ├── compressed_image
    │   ├── compressed_image
    │   │   ├── __init__.py
    │   │   ├── image_publisher_1.py
    │   │   ├── image_publisher_2.py
    │   │   └── image_subscriber_flask.py
    │   ├── package.xml
    │   ├── resource
    │   │   └── multi_image_package
    │   ├── setup.cfg
    │   ├── setup.py
    │   └── test
    │       ├── test_copyright.py
    │       ├── test_flake8.py
    │       └── test_pep257.py
    ├── monitor_test
    │   ├── config
    │   ├── monitor_test
    │   │   ├── __init__.py
    │   │   ├── camera_subscriber.py
    │   │   ├── debug_logger.py
    │   │   ├── deep_sort
    │   │   │   ├── __init__.py
    │   │   │   ├── detection.py
    │   │   │   ├── iou_matching.py
    │   │   │   ├── kalman_filter.py
    │   │   │   ├── linear_assignment.py
    │   │   │   ├── nn_matching.py
    │   │   │   ├── test.py
    │   │   │   ├── track.py
    │   │   │   └── tracker.py
    │   │   ├── dual_image_publisher.py
    │   │   ├── models
    │   │   │   ├── best.pt
    │   │   │   └── custom_tracker.yaml
    │   │   ├── ui_camera_subscriber copy.py
    │   │   └── ui_camera_subscriber.py
    │   ├── package.xml
    │   ├── resource
    │   │   └── monitor_test
    │   ├── setup.cfg
    │   ├── setup.py
    │   └── test
    │       ├── test_copyright.py
    │       ├── test_flake8.py
    │       └── test_pep257.py
    ├── multi_image_package
    │   ├── multi_image_package
    │   │   ├── __init__.py
    │   │   ├── amr_operating.py
    │   │   ├── image_publisher_1.py
    │   │   ├── image_publisher_2.py
    │   │   ├── image_subscriber.py
    │   │   ├── image_subscriber_flask.py
    │   │   ├── init_pose.py
    │   │   └── send_goal_stop.py
    │   ├── package.xml
    │   ├── resource
    │   │   └── multi_image_package
    │   ├── setup.cfg
    │   ├── setup.py
    │   └── test
    │       ├── test_copyright.py
    │       ├── test_flake8.py
    │       └── test_pep257.py
    ├── my_package
    │   ├── my_package
    │   │   ├── __init__.py
    │   │   ├── data_publisher.py
    │   │   ├── data_subscriber.py
    │   │   ├── image_publisher.py
    │   │   └── image_subscriber.py
    │   ├── package.xml
    │   ├── resource
    │   │   └── my_package
    │   ├── setup.cfg
    │   ├── setup.py
    │   └── test
    │       ├── test_copyright.py
    │       ├── test_flake8.py
    │       └── test_pep257.py
    └── random_position_controller
        ├── package.xml
        ├── random_position_controller
        │   ├── __init__.py
        │   ├── random_position_publisher.py
        │   └── turtlebot_subscriber.py
        ├── resource
        │   └── random_position_controller
        ├── setup.cfg
        ├── setup.py
        └── test
            ├── test_copyright.py
            ├── test_flake8.py
            └── test_pep257.py

158 directories, 430 files
```




## 추적차량 판단 알고리즘

**추적차량 판단 알고리즘**은 일반 차량과 추적 차량 구분함과 동시에 판단할 수 있는 핵심적인 역할을 합니다. `ui_camera_subscriber.py`에서 구현된 이 알고리즘은 다음과 같은 단계로 구성됩니다:

1. **초기 탐지:**
   - YOLOv8로 탐지된 모든 차량에 대해 초기 처리를 수행합니다.
   - 각 차량에 대해 고유 ID를 할당하고, 위치 정보를 저장합니다.

2. **추적 상태 업데이트:**
   - 이전 프레임에서 추적 중이던 차량들의 상태를 업데이트합니다.
   - 현재 프레임에서 탐지된 차량과 매칭하여 추적을 계속합니다.

3. **추적차량 분류:**
   - 각 차량에 대해 다음 조건을 검사하여 추적 대상으로 분류합니다:
   a. 차량이 단속 구역(마름모 영역) 내부에 있는지 확인
   b. 차량의 속도가 설정된 임계값을 초과하는지 확인
   c. 차량이 일정 시간 이상 추적되고 있는지 확인
   - 이는 제품의 회전이나 기울어짐에 따른 영향을 최소화하여 정확한 위치 비교를 가능하게 합니다.

4. **추적 상태 결정:**
   - 위 조건을 모두 만족하는 차량을 '추적 대상'으로 분류합니다.
   - 조건을 만족하지 않는 차량은 일반 차량으로 간주합니다.

5. **추적 정보 업데이트:**
   - 추적 대상으로 분류된 차량의 정보(위치, 속도, 추적 시간 등)를 지속적으로 업데이트합니다.

6. **추적 종료 판단:**
   - 추적 중인 차량이 화면에서 사라지거나 일정 시간 동안 탐지되지 않으면 추적을 종료합니다.


## 설치

### 필수 사항

- **Python 3.7 이상**
- **필수 라이브러리:**
  - `rclpy`
  - `cv2`
  - `sys`
  - `numpy`
  - `threading`
  - `ultralytics`
  - `math`
  - `time`
  - `PyQt5`

### 설치 단계

1. **저장소 클론:**

    ```bash
    git clone https://github.com/libero0077/RokeyProjects/tree/main/DetectCarProject
    ```

2. **ROS2 패키지 설치:**

    ```bash
    sudo apt update
    sudo apt install ros-humble-desktop
    ```

3. **Python 패키지 설치:**

    ```bash
    pip install ultralytics Pillow gradio pandas requests
    ```

4. **작업 공간 설정:**

    ```bash
    mkdir -p ~/ros2_ws/src
    cd ~/ros2_ws
    colcon build
    source install/setup.bash
    ```

## 사용법

<aside>
⚠️ 경고: 이 시스템은 7일이라는 짧은 기간 동안 개발된 프로젝트로. 현재 상태에서는 매우 불안정할 수 있습니다. 문서에 명시된 기능 중 일부는 제대로 작동하지 않을 가능성이 있습니다. 실제 환경에서 사용하기 전에 충분한 테스트와 검증이 필요합니다.

또한, 각 시스템은 아직 완전히 통합되지 않았으며, 실제 운영 환경에서의 안정적인 동작을 보장하기 어렵습니다.

그리고 차량 기반으로 진행한 프로젝트이기 때문에 차량 모델을 반영한 best.pt파일을 포함하고 있습니다. 다른 목적으로 진행하기 위해서는 다른 모델을 반영한 best.pt파일로 교체해야 합니다.
</aside>


- 밑의 예시는 python으로 실행하였지만 ros2 통신으로 진행하기 위해서는 src의 setup.py의 entry_point를 각각 정의하여 각 터미널에서 source install/setup.bash 명령어를 입력한 후, ros2 run 패키지명 정의한 entry_point로 실행하시면 됩니다.

1. **중앙 감지 노드 실행:**

    ```bash
    python3 dual_image_publisher.py
    ```

2. **모니터링 노드:**

    ```bash모델 학습이 완료된 후 생성되는 가중치 파일
    python3 ui_camera_subscriber.py

    ```

3. **자율 추적 노드:**

    ```bash
    python3 turtlebot_subscriber.py
    ```
    
    ```bash
    python3 random_position_publisher.py
    ```


## 개선 계획

현재 시스템은 기본적인 차량 탐지, 추적 차량 판단 알고리즘, 자동 추적, 모니터링 기능을 갖추고 있지만, 다음과 같은 개선을 통해 더욱 강력하고 효율적인 시스템으로 발전시킬 수 있습니다:

1. **다중 AMR 협동:**
   - 여러 대의 AMR이 협동해 넓은 지역을 효과적으로 감시하고 추적합니다.

2. **열화상 카메라 사용:**
   - 야간이나 가시거리 짧은 상황(눈, 비)에서의 탐지 능력을 보존할 수 있습니다.

3. **경로 예측 알고리즘:**
   - 추적 차량의 예상 경로로 접근하여 감속을 유도하고 차단하는 기능을 통해 추적차량에 대해 빠른 저지를 실행합니다.

4. **직접 제어:**
   - 인간이 직접 제어하는 기능(추적 차량 판단, AMR 직접 제어 등)을 추가해 효율을 높일 수 있습니다.



## 기여

[libero0077](https://github.com/libero0077) : DB 및 Logging 기능 통합, Object Detection 기능 정확도 향상, 문서 작성, 중앙 감지 모듈 개발  
[Y6HYUK](https://github.com/Y6HYUK) : 터틀봇 실행 및 네비게이션 기능 구현, Object Detection 기능 구현 및 중앙 감지 모듈 개발, 문서작성  
[leesw1357](https://github.com/leesw1357) : 시간 관련 기능 구현, 문서 작성, Object Detection 기능 정확도 향상  
[juwon407](https://github.com/juwon407) : 모니터링 모듈 개발, 모듈 간 통합 총괄, 알림 기능 구현 및 통합


## 연락처

문의 사항이나 지원이 필요하시면 아래 연락처로 연락주세요:

- **이름:** Sangwoo Lee
- **GitHub:** [leesw1357](https://github.com/leesw1357)

---

## 추가 참고 자료

- [rclpy 공식 문서](https://docs.ros.org/en/iron/p/rclpy/rclpy.html)
- [ROS2 공식 문서](https://docs.ros.org/)
- [Turtlebot3 공식 문서](https://emanual.robotis.com/docs/en/platform/turtlebot3/overview/)
- [OpenCV 공식 문서](https://docs.opencv.org/)
- [MySQL 공식 문서](https://dev.mysql.com/doc/)
- [PyQt 공식 문서](https://doc.qt.io/qtforpython-5/contents.html)
- [YOLO 공식 문서](https://docs.ultralytics.com/ko#where-to-start)
