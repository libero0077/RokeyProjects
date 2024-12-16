# TurtleBot3 다중 로봇 주차 시스템

![프로젝트 로고](path/to/logo.png) <!-- 선택 사항: 프로젝트 로고 추가 -->

## 목차

- [개요](#개요)
- [주요 기능](#주요-기능)
- [아키텍처](#아키텍처)
- [구성 요소](#구성-요소)
  - [중앙 제어 노드](#중앙-제어-노드)
  - [카메라 뷰어](#카메라-뷰어)
  - [맵 노드](#맵-노드)
  - [데이터베이스 관리자](#데이터베이스-관리자)
- [설치](#설치)
- [사용법](#사용법)
- [토픽 및 서비스](#토픽-및-서비스)
- [스크린샷](#스크린샷)
- [기여](#기여)
- [라이선스](#라이선스)
- [연락처](#연락처)

## 개요

**TurtleBot3 다중 로봇 주차 시스템**은 ROS 2를 기반으로 여러 대의 TurtleBot3 로봇을 활용하여 주차 시설을 관리하는 종합적인 프로젝트입니다. 이 시스템은 실시간 차량 감지, 주차 슬롯 관리, 로봇 네비게이션을 통합하여 주차 및 출차 과정을 효율적으로 처리합니다. PyQt5로 구축된 사용자 친화적인 GUI는 주차 슬롯 상태, 로봇 위치, 시스템 로그에 대한 실시간 업데이트를 제공합니다.

## 주요 기능

- **실시간 차량 감지:** YOLO(You Only Look Once)를 활용하여 여러 카메라 피드를 통해 효율적인 차량 감지.
- **중앙 집중식 제어:** 중앙 제어 노드가 주차 요청, 결제 처리, 로봇 조정을 관리.
- **그래픽 사용자 인터페이스 (GUI):** PyQt5로 구축된 GUI는 라이브 카메라 피드, 주차 슬롯 상태, 맵 상의 로봇 위치 및 시스템 로그를 표시.
- **데이터베이스 통합:** SQLite를 사용하여 작업 로그, 결제 기록, 주차 슬롯 상태를 기록.
- **로봇 네비게이션:** TurtleBot3 로봇과 통합하여 차량 주차 및 출차 작업을 처리.
- **비상 정지 처리:** 비상 정지 기능을 지원하여 안전성 보장.
- **시스템 상태 모니터링:** 로봇 상태 및 전체 시스템 상태를 실시간으로 모니터링.

## 아키텍처

시스템은 여러 상호 연결된 구성 요소로 구성됩니다:

1. **중앙 제어 노드:** 주차 작업을 관리하고, 결제를 처리하며, 주차 슬롯 상태를 업데이트하고 로봇과 통신.
2. **카메라 뷰어:** 여러 카메라 피드를 구독하고, YOLO를 사용하여 차량 감지를 수행하며, GUI를 통해 라이브 이미지를 업데이트.
3. **맵 노드:** AMCL(Adaptive Monte Carlo Localization)을 사용하여 로봇 위치를 추적하고 GUI 맵을 업데이트.
4. **데이터베이스 관리자:** 작업 로그 및 결제 기록을 포함한 모든 데이터베이스 작업을 처리.
5. **GUI (PyQt5):** 주차 슬롯 상태, 로봇 위치, 시스템 로그를 실시간으로 모니터링하고 제어할 수 있는 인터페이스 제공.

![아키텍처 다이어그램](path/to/architecture_diagram.png) <!-- 선택 사항: 아키텍처 다이어그램 추가 -->

## 구성 요소

### 중앙 제어 노드

- **파일:** `central_control_node.py`
- **설명:** 주차 요청을 처리하고, 작업 로그를 업데이트하며, 결제를 처리하고, 로봇 조정을 관리.
- **주요 기능:**
  - 서비스 서버: `ExitRequest`, `GetSystemState`
  - 토픽 구독: `/vehicle_detected`, `/payment/confirmation`, `/nav_callback`
  - 토픽 발행: `/central_control/logs`, `/central_control/robot_status`, `/parking_status`, `/vehicle_detected`
  - 데이터베이스 작업: 작업 로그 및 결제 기록 삽입 및 업데이트

### 카메라 뷰어

- **파일:** `camera_viewer.py` (예상 파일명)
- **설명:** 여러 카메라 피드를 구독하고, YOLO를 사용하여 차량 감지를 수행하며, GUI에 라이브 이미지를 업데이트.
- **주요 기능:**
  - 이미지 처리: ROS Image 메시지를 OpenCV 이미지로 변환
  - 차량 감지: 지정된 관심 영역 내에서 YOLO를 사용하여 실시간 감지
  - GUI 업데이트: 라이브 카메라 피드 표시 및 이미지 확대/축소 기능

### 맵 노드

- **파일:** `map_node.py` (예상 파일명)
- **설명:** AMCL을 사용하여 여러 로봇의 위치를 추적하고 GUI 맵을 업데이트.
- **주요 기능:**
  - 포즈 구독: `/tb1/amcl_pose`, `/tb2/amcl_pose`
  - 시그널 발송: GUI 스레드로 로봇 위치 업데이트 전송

### 데이터베이스 관리자

- **파일:** `db_manager.py`
- **설명:** SQLite 데이터베이스와의 모든 상호작용을 관리하며, 데이터베이스 초기화 및 CRUD 작업 수행.
- **주요 기능:**
  - 데이터베이스 초기화: 필요한 테이블(`Task_Log`, `Payment_Log`, `Parking_Slot` 등) 설정
  - 데이터 삽입 및 업데이트: 새로운 로그 삽입 및 기존 기록 업데이트

## 설치

### 필수 사항

- **ROS 2:** 호환되는 ROS 2 배포판 설치 (예: Foxy, Galactic, Humble)
- **Python 3:** ROS 2 노드 및 GUI 실행을 위한 Python 3
- **PyQt5:** GUI 인터페이스 구축을 위해 필요
- **YOLO (Ultralytics):** 차량 감지를 위해 필요
- **OpenCV:** 이미지 처리
- **SQLite3:** 데이터베이스 관리

### 설치 단계

1. **저장소 클론:**

    ```bash
    git clone https://github.com/yourusername/turtlebot3_multi_robot_parking.git
    cd turtlebot3_multi_robot_parking
    ```

2. **종속성 설치:**

    ```bash
    sudo apt update
    sudo apt install python3-pyqt5 python3-opencv sqlite3
    ```

    `pip`을 사용하여 Python 패키지 설치:

    ```bash
    pip install rclpy PyQt5 cv_bridge ultralytics Pillow
    ```

3. **ROS 2 워크스페이스 빌드:**

    ROS 2 환경 소싱 확인:

    ```bash
    source /opt/ros/<ros-distro>/setup.bash
    ```

    워크스페이스 빌드:

    ```bash
    colcon build
    source install/setup.bash
    ```

4. **데이터베이스 설정:**

    데이터베이스 파일이 존재하고 초기화되었는지 확인. `central_control_node.py` 스크립트는 데이터베이스가 없을 경우 초기화합니다.

    ```bash
    # 예시 경로 (필요에 따라 수정)
    /home/rokey/Documents/RokeyProjects/multitb_ws/src/turtlebot3_python_nodes/parking_system.db
    ```

## 사용법

1. **중앙 제어 노드 실행:**

    ```bash
    ros2 run turtlebot3_python_nodes central_control_node
    ```

2. **카메라 뷰어 GUI 실행:**

    ```bash
    ros2 run turtlebot3_python_nodes camera_viewer
    ```

3. **시스템과 상호작용:**

    - **차량 입차:**
      - 차량이 감지되면 시스템은 입차를 기록하고 주차 슬롯을 할당.
      - GUI는 차량이 "주차 중" 상태로 표시됨을 업데이트.

    - **결제 처리:**
      - 결제가 완료되면 시스템은 작업 로그를 "출차 중"으로 업데이트.
      - GUI는 해당 슬롯이 출차 중임을 반영.

    - **차량 출차:**
      - 로봇이 출차 과정을 처리하며, 작업 로그를 "출차 완료"로 업데이트.
      - GUI는 슬롯 상태를 "빈 슬롯"으로 업데이트.

4. **비상 정지:**

    - 모든 로봇 작업을 중단하기 위해 비상 정지 서비스를 호출.

    ```bash
    ros2 service call /emergency_stop std_srvs/srv/Trigger
    ```

## 토픽 및 서비스

### 토픽

- **구독:**
  - `/vehicle_detected` (`std_msgs/String`): 차량 감지 알림.
  - `/payment/confirmation` (`std_msgs/String`): 결제 상태 확인.
  - `/nav_callback` (`std_msgs/String`): 로봇의 네비게이션 콜백 수신.

- **발행:**
  - `/central_control/logs` (`std_msgs/String`): JSON 형식의 시스템 로그 발행.
  - `/central_control/robot_status` (`std_msgs/String`): 로봇 상태 업데이트 발행.
  - `/parking_status` (`std_msgs/String`): 주차 슬롯 상태 업데이트 발행.
  - `/vehicle_detected` (`std_msgs/String`): 차량 출차 요청 발행.

### 서비스

- **`ExitRequest`**
  - **설명:** 키오스크에서 출차 요청을 처리하고, 데이터베이스를 업데이트하며, 로봇 작업을 조정.
  - **요청:** `car_number` (문자열)
  - **응답:** `status` (불리언), `entry_time` (문자열), `fee` (정수), `log` (문자열)

- **`GetSystemState`**
  - **설명:** 현재 로봇 및 주차 슬롯의 상태를 제공.
  - **요청:** 빈 요청
  - **응답:** `robot_status_json` (문자열), `slot_status_json` (문자열)

## 스크린샷

### GUI 개요

![GUI 개요](path/to/gui_overview.png)

### 라이브 카메라 피드

![카메라 피드](path/to/camera_feed.png)

### 주차 슬롯 상태

![주차 상태](path/to/parking_status.png)

### 맵 상의 로봇 위치

![로봇 위치](path/to/robot_positions.png)

## 기여
[libero0077](https://github.com/libero0077) : System Integration
[Y6HYUK](https://github.com/Y6HYUK) : 


## 라이선스

이 프로젝트는 [MIT 라이선스](LICENSE)를 따릅니다.

## 연락처

문의 사항이나 지원이 필요하시면 아래 연락처로 연락주세요:

- **이름:** jaejun ryu
- **GitHub:** [libero0077](https://github.com/libero0077)

---

