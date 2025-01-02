# 제목 없음

# TurtleBot3 다중 로봇 주차 시스템

## 프로젝트 기간 : 2024.12.09 ~ 2024.12.16

### 스크린샷

### 

## 목차

- [개요](https://www.notion.so/16fddb6cc9d2802ea2e8f14db96c897a?pvs=21)
- [주요 기능](https://www.notion.so/16fddb6cc9d2802ea2e8f14db96c897a?pvs=21)
- [아키텍처](https://www.notion.so/16fddb6cc9d2802ea2e8f14db96c897a?pvs=21)
- [구성 요소](https://www.notion.so/16fddb6cc9d2802ea2e8f14db96c897a?pvs=21)
    - [테이블 오더 (키오스크)](https://www.notion.so/16fddb6cc9d2802ea2e8f14db96c897a?pvs=21)
    - [주방 디스플레이](https://www.notion.so/16fddb6cc9d2802ea2e8f14db96c897a?pvs=21)
    - [서빙 로봇](https://www.notion.so/16fddb6cc9d2802ea2e8f14db96c897a?pvs=21)
    - [로봇 모니터링](https://www.notion.so/16fddb6cc9d2802ea2e8f14db96c897a?pvs=21)
    - [데이터베이스 관리자](https://www.notion.so/16fddb6cc9d2802ea2e8f14db96c897a?pvs=21)
- [디렉토리 구조](https://www.notion.so/16fddb6cc9d2802ea2e8f14db96c897a?pvs=21)
- [설치](https://www.notion.so/16fddb6cc9d2802ea2e8f14db96c897a?pvs=21)
- [사용법](https://www.notion.so/16fddb6cc9d2802ea2e8f14db96c897a?pvs=21)
- [개선 계획](https://www.notion.so/16fddb6cc9d2802ea2e8f14db96c897a?pvs=21)
- [기여](https://www.notion.so/16fddb6cc9d2802ea2e8f14db96c897a?pvs=21)
- [라이선스](https://www.notion.so/16fddb6cc9d2802ea2e8f14db96c897a?pvs=21)
- [연락처](https://www.notion.so/16fddb6cc9d2802ea2e8f14db96c897a?pvs=21)
- [추가 참고 자료](https://www.notion.so/16fddb6cc9d2802ea2e8f14db96c897a?pvs=21)

## 개요

**TurtleBot3 다중 로봇 주차 시스템**은 ROS 2를 기반으로 여러 대의 TurtleBot3 로봇을 활용하여 주차 시설을 관리하는 종합적인 프로젝트입니다. 이 시스템은 실시간 차량 감지, 주차 슬롯 관리, 로봇 네비게이션을 통합하여 주차 및 출차 과정을 효율적으로 처리합니다. PyQt5로 구축된 사용자 친화적인 GUI는 주차 슬롯 상태, 로봇 위치, 시스템 로그에 대한 실시간 업데이트를 제공합니다.

## 주요 기능

- **실시간 차량 감지:** YOLO를 활용하여 여러 카메라 피드를 통해 효율적인 차량 감지.
- **중앙 집중식 제어:** 중앙 제어 노드가 주차 요청, 결제 처리, 로봇 조정을 관리.
- **그래픽 사용자 인터페이스 (GUI):** PyQt5로 구축된 GUI는 라이브 카메라 피드, 주차 슬롯 상태, 맵 상의 로봇 위치 및 시스템 로그를 표시.
- **데이터베이스 통합:** SQLite를 사용하여 작업 로그, 결제 기록, 주차 슬롯 상태를 기록.
- **로봇 네비게이션:** TurtleBot3 로봇과 통합하여 차량 주차 및 출차 작업을 처리.
- **비상 정지 처리:** 비상 정지 기능을 지원하여 안전성 보장.
- **시스템 상태 모니터링:** 로봇 상태 및 전체 시스템 상태를 실시간으로 모니터링.

## 아키텍처

시스템은 여러 상호 연결된 구성 요소로 구성되며, 각 구성 요소는 특정 기능을 담당하여 전체 시스템이 원활하게 동작하도록 합니다.

1. **중앙 제어:** 주차 작업을 관리하고 결제를 처리하며, 주차 슬롯 상태를 업데이트 하고 로봇과 통신합니다.
2. **미니맵:** AMCL(Adaptive Monte Carlo Localization)을 사용하여 로봇 위치를 추적하고 GUI 맵을 업데이트 합니다
3. **데이터베이스 관리자: 작업 로드 및 결제 기록을 포함한 모든 데이터베이스 작업을 처리합니다.**
4. **키오스크:** 출차할 차량의 번호를 입력하여 차량을 출차합니다.
5. **주차 로봇 네비게이션:** 주차 로봇과 출차 로봇의 작업을 처리하며 목표로 이동하는 경로를 생성하고 충돌을 방지하기 위한 회피 동작을 계산합니다.

## 구성 요소

### **중앙 제어 노드**

- **파일:** `central_control_node.py`
- **설명:** 주차장 제어 시스템에서 차량 입출차, 주차 슬롯 관리, 로봇 상태 관리 등의 역할을 담당합니다.
- **주요 기능:**
    - 로봇 작업 관리
    - 주차 슬롯 상태 업데이트
    - 로그 관리

### 미니맵

- **파일:** `gui_minimap.py`
- **설명:** ROS2와 PyQt5를 결합하여 주차장 시스템의 실시간 데이터와 카메라 피드를 시각적으로 보여주는 GUI 응용 프로그램입니다.
- **주요 기능:**
    - 로봇 위치 시각화
    - 카메라 피드 관리
    - 로그 및 시스템 상태 표시
    - 카메라 모니터링

### **데이터베이스 관리자**

- **파일:** `db_manager.py`
- **설명:** SQLite3를 사용하여 주차장 시스템에서 필요한 데이터베이스를 관리하기 위한 DBManager 클래스입니다.
- **주요 기능:**
    - 데이터베이스 초기화
    - 데이터 삽입
    - 데이터 업데이트
    - 데이터 삭제
    - 데이터 조회
    - 요금 계산

### 키오스크

- **파일:** `kiosk_gui.py`
- **설명:** 사용자가 차량 번호를 입력하면, 출차 요청 및 결제 프로세스를 처리할 수 있도록 합니다.
- **주요 기능:**
    - 차량 번호 입력
    - 출차 요청 처리
    - 요금 결제

### **주차 로봇 네비게이션**

- **파일:** `nav_node.py`
- **설명:** 주차장에서 차량의 입차 및 출차를 담당하는 로봇의 행동을 제어하고, 경로를 계획하며, 충돌을 방지합니다.
- **주요 기능:**
    - 로봇 관리 및 초기화
    - 입차(in) 및 출차(out) 작업을 처리
    - 경로 생성 및 충돌 방지
    - 상태 시각화

## 디렉토리 구조

```bash
src
├── nav_node
│   ├── nav_node
│   │   ├── __init__.py
│   │   ├── nav_node.py
│   │   ├── send_.py
│   │   └── test_node.py
│   ├── package.xml
│   ├── resource
│   │   └── nav_node
│   ├── setup.cfg
│   ├── setup.py
│   └── test
│       ├── test_copyright.py
│       ├── test_flake8.py
│       └── test_pep257.py
├── turtlebot3_interfaces
│   ├── CMakeLists.txt
│   ├── package.xml
│   └── srv
│       ├── ExitRequest.srv
│       └── GetSystemState.srv
├── turtlebot3_multi_robot
│   ├── env-hooks
│   │   └── multi_robot.dsv.in
│   ├── launch
│   │   ├── gazebo_multi_nav2_world.launch.py
│   │   ├── gazebo_multi_world.launch.py
│   │   └── nav2_bringup
│   │       ├── bringup_launch.py
│   │       ├── localization_launch.py
│   │       ├── navigation_launch.py
│   │       ├── rviz_launch.py
│   │       └── slam_launch.py
│   ├── models
│   │   ├── turtlebot3_burger
│   │   │   ├── meshes
│   │   │   │   ├── burger_base.dae
│   │   │   │   ├── lds.dae
│   │   │   │   └── tire.dae
│   │   │   ├── model-1_4.sdf
│   │   │   ├── model.config
│   │   │   └── model.sdf
│   │   └── turtlebot3_waffle
│   │       ├── meshes
│   │       │   ├── lds.dae
│   │       │   ├── r200.dae
│   │       │   ├── tire.dae
│   │       │   └── waffle_base.dae
│   │       ├── model-1_4.sdf
│   │       ├── model.config
│   │       ├── model copy.sdf
│   │       ├── model_nocamera.sdf
│   │       └── model.sdf
│   ├── package.xml
│   ├── params
│   │   └── nav2_params.yaml
│   ├── resource
│   │   └── turtlebot3_multi_robot
│   ├── rviz
│   │   ├── multi_nav2_default_view.rviz
│   │   └── nav2_default_view.rviz
│   ├── setup.cfg
│   ├── setup.py
│   ├── test
│   │   ├── test_copyright.py
│   │   ├── test_flake8.py
│   │   └── test_pep257.py
│   ├── turtlebot3_multi_robot
│   │   ├── __init__.py
│   │   └── lifting_car.py
│   ├── urdf
│   │   ├── common_properties.urdf
│   │   ├── turtlebot3_burger.urdf
│   │   ├── turtlebot3_waffle copy.urdf
│   │   └── turtlebot3_waffle.urdf
│   └── worlds
│       ├── multi_empty_world.world
│       └── multi_robot_world.world
└── turtlebot3_python_nodes
    ├── db
    │   ├── img
    │   │   └── car_1111.jpeg
    │   └── parking_system.db
    ├── map
    │   ├── map.pgm
    │   └── map.yaml
    ├── package.xml
    ├── parking_system.db
    ├── resource
    │   └── turtlebot3_python_nodes
    ├── setup.cfg
    ├── setup.py
    ├── test
    │   ├── test_copyright.py
    │   ├── test_flake8.py
    │   └── test_pep257.py
    └── turtlebot3_python_nodes
        ├── central_control_node.py
        ├── db_init.txt
        ├── db_manager.py
        ├── gui_minimap.py
        ├── gui_monitor.py
        ├── gui_test.py
        ├── __init__.py
        ├── kiosk_gui.py
        ├── monitoring_node.py
        ├── __pycache__
        │   ├── central_control_node.cpython-310.pyc
        │   ├── db_manager.cpython-310.pyc
        │   ├── gui_minimap.cpython-310.pyc
        │   ├── __init__.cpython-310.pyc
        │   ├── kiosk_gui.cpython-310.pyc
        │   └── monitoring_node.cpython-310.pyc
        └── tempCodeRunnerFile.py

30 directories, 84 files
```

## 설치

### 필수 사항

- **운영체제:** Ubuntu 22.04
- **Python 버전:** Python 3.7 이상
- **필수 라이브러리:**
    - `ros2 (humble)`
    - `rclpy`
    - `PyQt5`
    - `sqlite3`
    - `nav2_msgs`
    - `geometry_msgs`
    - `std_msgs`
    - `gazebo`
    - 기타 프로젝트에 필요한 Python 패키지

### 설치 단계

1. **ROS2 워크스페이스 설정 및 저장소 클론:**
    
    ```bash
    mkdir ~/ros2_ws
    cd ~/ros2_ws
    git clone <https://github.com/libero0077/RokeyProjects>
    cd RokeyProjects/ParkingLotProject/B5
    ```
    
2. **파일 위치 정의:**
    - `gui_minimap.py` 파일의 `image_path`와 `yaml_path`를 프로젝트의 `map` 폴더 내 파일 경로로 변경합니다.
    - `central_control_node.py` 파일의 `db_path`를 프로젝트의 `db` 폴더 내 데이터베이스 파일 경로로 변경합니다.
        
        ```python
        # gui_minimap.py
        image_path = '/home/juwon/git/RokeyProjects/ParkingLotProject/multitb_ws/src/turtlebot3_python_nodes/map/map.pgm'
        yaml_path = '/home/juwon/git/RokeyProjects/ParkingLotProject/multitb_ws/src/turtlebot3_python_nodes/map/map.yaml'
        
        # central_control_node.py
        db_path = "/home/juwon/git/RokeyProjects/ParkingLotProject/multitb_ws/src/turtlebot3_python_nodes/db/parking_system.db"
        ```
        
3. **패키지 빌드:**
    
    ```bash
    colcon build
    source install/setup.bash
    ```
    

## 사용법

<aside>
⚠️ 경고: 이 시스템은 7일이라는 짧은 기간 동안 개발된 프로젝트이며. 현재 상태에서는 매우 불안정할 수 있으며, 문서에 명시된 기능들 중 일부는 제대로 작동하지 않을 수 있습니다. 실제 환경에서 사용하기 전에 충분한 테스트와 검증이 필요합니다.

또한, 현재 각 시스템은 완전히 통합되지 않은 상태이며, 실제 운영 환경에서의 안정적인 동작을 보장할 수 없습니다.

</aside>

1. **ROS2 노드 실행:**
    
    각각의 노드를 별도의 터미널에서 실행해야 합니다. ROS2 환경이 설정되어 있는지 확인하세요.
    
    - **모니터링 시스템 실행:**
        
        ```bash
        ros2 run turtlebot3_python_nodes central_control_node
        ros2 run turtlebot3_python_nodes kiosk_gui
        ros2 run turtlebot3_python_nodes gui_minimap
        ```
        
    - **GAZEBO를 사용하여 가상 시뮬레이션에서 터틀봇을 움직이기 위해 런치파일 실행:**
        
        ```bash
        ros2 launch  turtlebot3_multi_robot gazebo_multi_nav2_world.launch.py 
        ```
        
    - **주차로봇의 경로 생성과 이동 명령을 위해 nav노드 실행**
        
        ```bash
        ros2 run nav_node test_node 
        ros2 run nav_node nav_node 
        ```
        
    
2. **프로젝트 실행:**
    
    모니터링 시스템으로 주차장 현황을 확인할 수 있습니다, 네비게이션 노드를 통해 로봇이 이동할 경로를 생성하고 시각화 할 수 있습니다.
    
3. **데이터베이스:**
    
    주차 내역과 로그는 `parking_system.db` 파일에 저장됩니다.
    

## 개선 계획

현재 시스템은 기본적인 주차 관리 시스템이지만 다음과 같은 개선을 통해 더욱 강력하고 효율적인 시스템으로 발전시킬 수 있습니다:

1. **모니터링 시스템과 로봇 제어 시스템 통합:**
    - 현재 모니터링 시스템과 로봇 제어 시스템이 통합되지 않은 상태로 최소한의 시연만 가능하지만 추후 시스템 통합으로 하나의 시스템으로 만들어 배포를 쉽게 합니다.
2. **데이터 보안 및 접근 제어:**
    - **데이터베이스 보안 강화:** 데이터베이스 보안을 강화하고, 사용자 인증 및 권한 관리를 통해 데이터 접근을 제어합니다.
    - **실시간 데이터 암호화:** 실시간 데이터 암호화 및 백업 시스템을 도입하여 데이터의 무결성과 보안을 확보합니다.
3. **사용자 경험 향상:**
    - **직관적 GUI 개선:** GUI 인터페이스를 더욱 직관적이고 사용자 친화적으로 개선합니다.
    - **모바일 지원:** 모바일 디바이스 지원을 통해 언제 어디서나 차량을 출차 할 수 있게 합니다.

## 기여

이 프로젝트를 같이 진행한 팀원들의 기여도입니다.:

- 류재준 [libero0077](https://github.com/libero0077) : 데이터베이스 설계, 시스템 통합, 중앙 노드
- 양준혁 [Y6HYUK](https://github.com/Y6HYUK) : 맵핑, 키오스크 노드, 미니맵 노드
- 이상우 [leesw1357](https://github.com/leesw1357) : 워드, 미니맵 노드
- 김주원 [juwon407](https://github.com/juwon407) : 주차 로봇 경로 계획 알고리즘, 맵핑

## 라이선스

이 프로젝트는 [MIT 라이선스](https://www.notion.so/LICENSE)를 따릅니다.

## 연락처

문의 사항이나 지원이 필요하시면 아래 연락처로 연락주세요:

- **이름:** 김주원
- **GitHub:** [juwon407](https://github.com/juwon407)

---

## 추가 참고 자료

- [ROS2 공식 문서](https://docs.ros.org/en/foxy/index.html)
- [NAV2 공식 문서](https://navigation.ros.org/)
- [PyQt5 공식 문서](https://www.riverbankcomputing.com/static/Docs/PyQt5/)
- [SQLite 공식 문서](https://www.sqlite.org/docs.html)
- [GitHub Actions](https://github.com/features/actions)
