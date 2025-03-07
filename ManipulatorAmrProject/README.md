# ArUco 마커와 로봇팔 메니퓰레이터 프로젝트

## 프로젝트 기간 : 2024.12.03 ~ 2024.12.9

---

## 목차

- [ArUco 마커와 로봇팔 메니퓰레이터 프로젝트](#aruco-마커와-로봇팔-메니퓰레이터-프로젝트)
  - [프로젝트 기간 : 2024.12.03 ~ 2024.12.9](#프로젝트-기간--20241203--2024129)
  - [목차](#목차)
  - [개요](#개요)
  - [주요 기능](#주요-기능)
  - [아키텍처](#아키텍처)
  - [구성 요소](#구성-요소)
    - [중앙 제어 노드](#중앙-제어-노드)
    - [모니터링 노드](#모니터링-노드)
    - [마커 추적 노드](#마커-추적-노드)
    - [감지 및 그립 노드](#감지-및-그립-노드)
    - [컨베이어 컨트롤 노드](#컨베이어-컨트롤-노드)
    - [학습 데이터 수집 노드](#학습-데이터-수집-노드)
  - [디렉토리 구조](#디렉토리-구조)
  - [설치](#설치)
    - [필수 사항](#필수-사항)
    - [설치 단계](#설치-단계)
  - [실행 절차](#실행-절차)
  - [개선 계획](#개선-계획)
  - [기여](#기여)
  - [연락처](#연락처)
  - [라이선스](#라이선스)
  - [추가 참고 자료](#추가-참고-자료)

## 개요

**ArUco 마커와 로봇팔 메니퓰레이터 프로젝트**는 아르코 마커를 활용하여 turtlebot3의 위치와 방향을 추정하고 작업을 수행할 위치를 안내하여 turtlebot3과 로봇팔 메니퓰레이터를 작동 시키는 것이 목표인 프로젝트입니다. 이 프로젝트는 작업 필드를 비추는 카메라를 활용하여 각 위치의 아르코 마커를 인식. 위치를 계산한 후 작업 위치로 로봇을 이동시키거나 필요한 작업을 수행 할 수 있도록 합니다. PyQt로 구축된 모니터링 대시보드를 통해 실시간 작업 상황과 경고 알림, 수행할 작업, 비상정지 등을 수행 할 수 있습니다. 또한 터틀봇 내부 카메라를 활용하여 목표 박스를 선별, 설치된 로봇팔 메니퓰레이터로 박스를 컨베이어 벨트로 옮기는 작업을 수행할 수 있습니다.

## 주요 기능

- **ArUco 마커:** 필드에 설치된 마커를 통해 turtlebot3의 현재 위치와 방향을 추정하고 작업을 위한 목표까지의 방향과 거리를 계산 합니다
- **로봇팔 메니퓰레이터:** 목표물을 ****집거나 옮기는 동작을 수행 할 수 있고, 설치된 카메라를 통해 목표물을 서치할 수 있습니다.
- **위협 탐지 및 대응:** 도주 차량 탐지 시 즉시 중앙 제어 센터로 경고 메시지를 전송합니다.
- **자동 학습 데이터 수집:** 메니퓰레이터에 설치된 카메라로 작업에 필요한 학습 데이터를 자동으로 수집할 수 있게 합니다.
- **실시간 모니터링:** 작업 상황을 실시간으로 모니터링 하거나 작업자가 목표 작업을 지정 하거나 다른 작업을 수행할 수 있는 대시보드를 제공합니다
- **보안 및 관리:** GUI를 통해 모니터링 및 작업을 수행하려면 먼저 로그인을 통과 해야 합니다. 이후 시스템에서 알람이 발생할 경우 로그인한 이메일 주소로 알람을 전송합니다.

## 아키텍처

시스템은 여러 상호 연결된 구성 요소로 구성되며, 각 구성 요소는 특정 기능을 담당하여 전체 시스템이 원활하게 동작하도록 합니다

1. **중앙 제어 모듈**: 필드 카메라 작동, 데이터 처리 및 저장, 분석 기능과 모듈 간 데이터 송수신 기능을 담당합니다
2. **Turtlebot3 모듈**: 중앙 제어 모듈에서 전송하는 데이터를 처리하고 작업을 수행합니다.
3. **ArUco 모듈**: 필드 카메라의 영상에서 ArUco 마커를 인식하고 각 마커의 좌표와 방향을 계산합니다.

## 구성 요소

### 중앙 제어 노드

- **파일:** `test_main_node.py`
- **설명:** ROS2 (Robot Operating System 2)환경에서 동작하는 중앙 제어 노드이며, 분리되어 있는 각 노드들 간 통신과 제어를 담당합니다.
- **주요 기능:**
    - 작업자의 대시보드에 표시될 내용을 결정
    - 작업 순서에 따라 컨베이어 벨트를 동작시키도록 명령하거나 작업자의 수동 동작 명령을 컨베이어 노드로 전송함

### 모니터링 노드

- **파일:** `ui_node.py`
- **설명:** 필드에 설치된 카메라를 모니터링 하거나 작업자가 작업을 선택하고 학습 데이터를 수집하는 등의 작업을 수행 할 수 있도록 PyQt로 구성된 GUI 환경을 제공합니다.
- **주요 기능:**
    - 그래픽 사용자 인터페이스(GUI): PyQt5를 통해 구성된 GUI 환경으로 작업자가 알아보기 쉽고 작업을 수행하기 쉽도록 도움을 줌
    - 작업 모니터링: 작업 필드를 비추는 카메라 피드를 대시보드에 표시하고 작업 상태 표시, 작업 소요 시간 정보, 컨베이어 조작, 학습 데이터 수집, 비상 정지 등을 포함
    - 대시보드에 표시된 카메라 영상을 클릭하는 것 만으로 쉽게 작업 필드를 캡쳐 할 수 있음

### 마커 추적 노드

- **파일:** `world_camera2_node.py`
- **설명:** 작업 필드 전체를 비추는 카메라 영상을 다른 노드에 퍼블리싱 하고, ArUco 마커를 추적하여 로봇의 현재 위치와 방향, 목표물 까지의 거리와 방향을 계산합니다.
- **주요 기능:**
    - 카메라 영상 퍼블리싱: 작업 필드 전체를 비추는 카메라의 영상을 다른 노드에게 퍼블리싱
    - 마커 추적: Turtlrbot3의 상단과 작업 목표 위치 등에 설치된 마커를 인식하고 각 마커간 방향과 거리를 계산
    - 로봇 정보 시각화: 마커를 통해 얻은 정보를 바탕으로 turtlebot3의 좌표와 방향 정보를 표시
    - 대기 시간 관리: 특정 위치(예: 두 번째 위치)에서 지정된 시간 동안 대기
    - 방향 계산: 웨이포인트 간 이동 시 로봇의 방향을 자동으로 계산하여 설정

### 감지 및 그립 노드

- **파일:** `detection_grip.py`
- **설명:** turtlebot3의 내부에서 작동하는 노드로 중앙 제어 노드의 명령을 받아 목표물을 탐지하고 로봇팔을 동작하는 작업을 수행합니다.
- **주요 기능:**
    - YOLO 객체 감지: Turtlebot3의 로봇팔 메니퓰레이터에 설치된 카메라를 구독
    - 목표 박스 추적: 구독한 영상에서 목표 객체를 학습된 YOLO 모델로 감지하여 작업 순서를 결정
    - 로봇팔 제어: 로봇팔 메니퓰레이터를 제어하여 작업 수행

### 컨베이어 컨트롤 노드

- **파일:** `conveyor_node.py`
- **설명:** 컨베이어 벨트를 제어하는 아두이노와 시리얼 통신을 수행합니다.
- **주요 기능:**
    - 시리얼 통신: 컨베이어 벨트를 작동시키는 아두이노와 시리얼 통신을 수행하여 제어 합니다

### 학습 데이터 수집 노드

- **파일:** `collect_data_node.py`
- **설명:** 모델 학습에 필요한 데이터를 수집하기 위해 로봇팔을 제어하여 다양한 각도에서 이미지를 수집합니다.
- **주요 기능:**
    - 로봇팔 제어: 로봇팔을 특정 위치로 이동하도록 명령
    - 학습 이미지 수집: 다양한 각도에서 모델 학습에 필요한 데이터(이미지)를 수집

## 디렉토리 구조

```bash
.
└── src
    └── ManipulatorAmrProject
        ├── images
        ├── ManipulatorAmrProject
        │   ├── collect_data_node.py
        │   ├── conveyor_node.py
        │   ├── detection_grip.py
        │   ├── __init__.py
        │   ├── test_main_node.py
        │   ├── ui_node.py
        │   └── world_camera2_node.py
        ├── package.xml
        ├── resource
        │   └── ManipulatorAmrProject
        ├── setup.cfg
        ├── setup.py
        └── test
            ├── test_copyright.py
            ├── test_flake8.py
            └── test_pep257.py

6 directories, 14 files
```

## 설치

### 필수 사항

- **Python 3.7 이상**
- **필수 라이브러리:**
    - `rclpy`
    - `cv2`
    - `sys`
    - `numpy`
    - `threading`
    - `math`
    - `time`
    - `PyQt5`

### 설치 단계

1. **ROS2 패키지 설치:**
    
    ```bash
    sudo apt update
    sudo apt install ros-humble-desktop
    ```
    
2. **작업 공간 설정:**
    
    ```bash
    mkdir -p ros2_ws/src
    cd ros2_ws
    ```
    
3. **저장소 클론:**
    
    ```bash
    git clone 'https://github.com/libero0077/RokeyProjects.git'
    cd ManipulatorAmrProject/ManipulatorAmrProject_ws
    ```
    
4. **프로젝트 빌드:**
    
    ```bash
    colcon build
    source install/setup.bash
    ```
    

## 실행 절차

<aside>
⚠️ 경고: 이 시스템은 7일이라는 짧은 기간 동안 개발된 프로젝트로. 현재 상태에서는 매우 불안정할 수 있습니다. 문서에 명시된 기능 중 일부는 제대로 작동하지 않을 가능성이 있습니다. 실제 환경에서 사용하기 전에 충분한 테스트와 검증이 필요합니다.

또한, 각 시스템은 아직 완전히 통합되지 않았으며, 실제 운영 환경에서의 안정적인 동작을 보장하기 어렵습니다.
</aside>

- **ui node 수정:**
    
    ui_node.py
    
    - 기본 값 “rokey” 또는 원하는 패스워드로 변경
    
    ```python
    # Line 662
    if self.pw_input.text() == "rokey":
    ```
    
    - 이메일 정보 수정
    
    ```python
    # Line 812 - 817
    def send_email(self, content):
            smtp_server = "smtp.gmail.com"
            smtp_port = 587
            sender_email = "****@*****.***" # 전송할 이메일
            sender_password = "*******" # 이메일 패스워드
            receiver_email = "******"  # 받을 이메일
            subject = "STATUS Notification"
    ```
    

- **말단 노드 작동:**
    
    ```bash
    # 메인 시스템 PC에서 실행
    ros2 run ManipulatorAmrProject conveyor_node # 컨베이어 제어
    ros2 run ManipulatorAmrProject collect_data_node # 자동 데이터 수집
    ros2 run ManipulatorAmrProject webcam_node # 필드 카메라
    ```
    
    ```bash
    # 터틀봇 내부에서 실행
    ros2 run ManipulatorAmrProject detection_grip_node # 로봇팔 메니퓰레이터 제어
    ```
    
- **모니터링 노드:**
    
    ```bash
    # 메인 시스템 PC에서 실행
    export QT_QPA_PLATFORM=wayland
    ros2 run ManipulatorAmrProject gui_node
    ```
    
    - 로그인 화면에서 이메일 알람을 받을 주소를 입력후 비밀번호에 “rokey” 입력 후 로그인
- **메인 노드:**
    
    ```bash
    # 메인 시스템 PC에서 실행
    
    # 대시보드 확인되면 실행
    ros2 run ManipulatorAmrProject main_node
    ```
    

## 개선 계획

현재 시스템은 기본적인 마커 탐지, 컨베이어 작동, 모니터링 기능을 갖추고 있지만, 다음과 같은 개선을 통해 더욱 강력하고 효율적인 시스템으로 발전시킬 수 있습니다:

1. **다중 AMR 협동:**
    - 여러 대의 AMR이 협동해 다양한 작업을 동시에 수행할 수 있습니다.
2. **직접 제어:**
    - 인간이 직접 제어하는 기능을 추가해 추가 작업을 할 수 있습니다.

## 기여

[libero0077](https://github.com/libero0077) : Manipulator 노드 개발, 학습 데이터 수집 개발, YOLO 데이터 수집 및 학습

[Y6HYUK](https://github.com/Y6HYUK) : AuRco 마커 인식, YOLO 데이터 수집 및 학습

[leesw1357](https://github.com/leesw1357) : AuRco 마커 인식, turtlebot3 제어

[juwon407](https://github.com/juwon407) : 대시보드 노드, 중앙 제어 노드, 컨베이어 노드, AuRco 마커 인식

## 연락처

문의 사항이나 지원이 필요하시면 아래 연락처로 연락주세요:

- **이름:** Juwon kim
- **Email:** wndnjs2ek@gmail.com

---

## 라이선스

이 프로젝트는 [MIT License](https://github.com/libero0077/RokeyProjects/blob/main/CleaningRobotProject/LICENSE)를 따릅니다.

---

## 추가 참고 자료

- [rclpy 공식 문서](https://docs.ros.org/en/iron/p/rclpy/rclpy.html)
- [ROS2 공식 문서](https://docs.ros.org/)
- [Turtlebot3 공식 문서](https://emanual.robotis.com/docs/en/platform/turtlebot3/overview/)
- [OpenCV 공식 문서](https://docs.opencv.org/)
- [MySQL 공식 문서](https://dev.mysql.com/doc/)
- [PyQt 공식 문서](https://doc.qt.io/qtforpython-5/contents.html)
- [YOLO 공식 문서](https://docs.ultralytics.com/ko#where-to-start)