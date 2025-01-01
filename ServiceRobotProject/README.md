# 서비스(음식배달) 로봇 및 관제 시스템 개발

### 데모영상



### 통계창 예시
- 하루 매출 및 메뉴별 판매량, 월 별 매출 및 메뉴별 판매량, 서빙 로봇의 배달 로그 등 다양한 통계를 확인할 수 있음

![Screenshot from 2024-12-23 18-00-48](https://github.com/user-attachments/assets/84ff5a77-18cf-440d-856b-5e9a222b06d0)


![Screenshot from 2024-12-23 18-01-01](https://github.com/user-attachments/assets/77440edb-eda0-475c-aade-5a9b0a693252)


![Screenshot from 2024-12-23 18-01-10](https://github.com/user-attachments/assets/7c4e9ed6-e674-4cbd-9c9e-23036a56e4b1)


![Screenshot from 2024-12-23 18-01-17](https://github.com/user-attachments/assets/aa8b11ec-215c-4095-aac0-c61f57cb4cf3)


![Screenshot from 2024-12-23 18-01-24](https://github.com/user-attachments/assets/2c705c0d-3c09-40cb-9cd9-be54d2c78e51)


![Screenshot from 2024-12-23 18-01-34](https://github.com/user-attachments/assets/ff6afc1a-5e6b-48f6-ae49-b79bd87ced3c)

## 목차

- [개요](#개요)
- [주요 기능](#주요-기능)
- [아키텍처](#아키텍처)
- [구성 요소](#구성-요소)
  - [테이블 오더 (키오스크)](#테이블-오더-키오스크)
  - [주방 디스플레이](#주방-디스플레이)
  - [서빙 로봇](#서빙-로봇)
  - [로봇 모니터링](#로봇-모니터링)
  - [데이터베이스 관리자](#데이터베이스-관리자)
- [디렉토리 구조](#디렉토리-구조)
- [설치](#설치)
- [사용법](#사용법)
- [개선 계획](#개선-계획)
- [기여](#기여)
- [라이선스](#라이선스)
- [연락처](#연락처)
- [추가 참고 자료](#추가-참고-자료)

## 개요

**서비스(음식배달) 로봇 및 관제 시스템 개발** 프로젝트는 음식점의 주문 관리, 주방 운영, 음식 배달 과정을 자동화하기 위한 목적으로 진행되었습니다. ROS2 (Robot Operating System)를 활용하여 구성 요소 간의 원활한 통신을 구현하였으며, 고객의 주문이 주방으로 전달되고 서빙 로봇이 자율적으로 지정된 테이블로 음식을 배달하는 과정을 효율적으로 설계하였습니다. 이 프로젝트는 실제 음식점의 워크플로우를 모델링하여 기술 학습과 문제 해결 능력을 향상시키기 위해 기획되었습니다.

## 주요 기능

- **테이블 오더:** PyQt를 사용한 GUI를 통해 각 테이블에서 주문을 손쉽게 입력하고 확인할 수 있습니다.
- **주방 디스플레이:** 실시간으로 접수된 주문을 확인하고, 서빙 로봇을 통해 음식을 배달할 수 있습니다.
- **서빙 로봇 제어:** ROS2와 NAV2를 사용하여 서빙 로봇을 작동하고, 지정된 테이블로 정확하게 음식을 배달합니다.
- **로봇 상태 모니터링:** 실시간으로 로봇의 상태를 확인하고, 필요한 경우 복귀 명령을 보내어 로봇을 제어할 수 있습니다.
- **데이터베이스 관리:** SQLite를 사용하여 주문 내역, 메뉴 정보, 배달 로그 등을 체계적으로 관리하고, 다양한 통계를 제공합니다.
- **통계 분석:** 일일 매출, 메뉴별 판매량, 로봇의 배달 로그 등 다양한 통계를 시각화하여 운영 효율성을 분석할 수 있습니다.
- **메시지 통신:** ROS2의 토픽, 서비스, 액션을 활용하여 각 노드 간의 원활한 통신을 구현합니다.
- **로깅 및 QoS 설정:** 다양한 로깅 레벨을 사용하여 시스템 상태를 기록하고, QoS 설정을 통해 메시지의 신뢰성을 보장합니다.

## 아키텍처

시스템은 여러 상호 연결된 구성 요소로 구성되며, 각 구성 요소는 특정 기능을 담당하여 전체 시스템이 원활하게 동작하도록 합니다:

1. **테이블 오더 (키오스크):** 고객의 주문을 입력하고, 주문 정보를 주방 디스플레이로 전달합니다.
2. **주방 디스플레이:** 주문을 수신하고, 서빙 로봇을 제어하여 음식을 배달합니다.
3. **서빙 로봇:** 음식을 지정된 테이블로 배달하며, 배달 상태를 모니터링합니다.
4. **로봇 모니터링:** 서빙 로봇의 상태를 실시간으로 모니터링하고, 필요 시 복귀 명령을 보냅니다.
5. **데이터베이스 관리자:** 모든 주문, 메뉴, 배달 로그를 관리하고, 통계 데이터를 제공합니다.

## 구성 요소

### 테이블 오더 (키오스크)

- **파일:** `test_order.py`
- **설명:** 9개의 테이블에서 주문을 입력받아 주문 정보를 ROS2 토픽을 통해 주방 디스플레이로 전달합니다.
- **주요 기능:**
  - 주문 입력 GUI 제공
  - 주문 데이터를 퍼블리시
  - 메뉴 업데이트 요청을 서비스 클라이언트를 통해 처리

### 주방 디스플레이

- **파일:** `test_sub.py`
- **설명:** 접수된 주문을 확인하고, 서빙 로봇을 제어하여 음식을 배달합니다.
- **주요 기능:**
  - 주문을 구독(subscribe)하여 실시간으로 수신
  - 메뉴 업데이트를 서비스 서버를 통해 제공
  - 서빙 로봇에게 명령을 토픽으로 퍼블리시하여 로봇을 제어
  - 주문 처리 결과를 서비스 클라이언트를 통해 테이블 오더 노드에 전달

### 서빙 로봇

- **파일:** `test_robot_controll.py`
- **설명:** ROS2와 NAV2를 사용하여 서빙 로봇을 시뮬레이션하고, 지정된 위치로 정확하게 이동합니다.
- **주요 기능:**
  - 로봇 명령 수신 및 처리
  - 지정된 위치로 로봇 이동
  - 로봇의 현재 위치 및 상태를 피드백으로 제공

### 로봇 모니터링

- **파일:** `test_robot_monitor.py`
- **설명:** 서빙 로봇의 상태를 실시간으로 모니터링하고, GUI를 통해 상태를 시각화합니다.
- **주요 기능:**
  - 로봇 상태 구독 및 GUI 업데이트
  - 로봇의 상태에 따른 시각적 피드백 제공
  - 복귀 명령을 퍼블리시하여 로봇을 제어

### 데이터베이스 관리자

- **파일:** `db_manager.py`
- **설명:** SQLite 데이터베이스와의 모든 상호작용을 관리하며, 데이터베이스 초기화 및 CRUD(Create, Read, Update, Delete) 작업을 수행합니다.
- **주요 기능:**
  - 데이터베이스 초기화: 필요한 테이블(`tables`, `menu`, `orders`, `order_items`, `deliver_log`) 생성 및 초기화
  - 데이터 삽입 및 업데이트: 새로운 주문, 메뉴 항목, 배달 로그 삽입 및 기존 기록 업데이트
  - 데이터 조회: 다양한 쿼리를 통해 주문 내역 및 통계 데이터를 조회

## 디렉토리 구조
```bash
├── restaurant.db
├── restaurant_db.db
└── src
    ├── menu_order_interfaces
    │   ├── action
    │   │   └── Serve.action
    │   ├── CMakeLists.txt
    │   ├── msg
    │   │   └── Order.msg
    │   ├── package.xml
    │   └── srv
    │       ├── MenuTable.srv
    │       └── MenuUpdate.srv
    └── menu_order_project
        ├── menu_order_project
        │   ├── check_data_pyqt5.py
        │   ├── db_manager.py
        │   ├── __init__.py
        │   ├── kitchen_monitoring.py
        │   ├── menu_order.py
        │   ├── __pycache__
        │   │   ├── check_data_pyqt5.cpython-310.pyc
        │   │   ├── db_manager.cpython-310.pyc
        │   │   ├── __init__.cpython-310.pyc
        │   │   ├── test_order.cpython-310.pyc
        │   │   ├── test_robot_controll.cpython-310.pyc
        │   │   └── test_sub.cpython-310.pyc
        │   ├── Robot.png
        │   ├── table_order.py
        │   ├── temp_update_db.py
        │   ├── test_order.py
        │   ├── test_robot_controll.py
        │   ├── test_robot_monitor.py
        │   └── test_sub.py
        ├── package.xml
        ├── resource
        │   └── menu_order_project
        ├── setup.cfg
        ├── setup.py
        └── test
            ├── test_copyright.py
            ├── test_flake8.py
            └── test_pep257.py

10 directories, 33 files

```
## 설치

### 필수 사항

- **운영체제:** Ubuntu 22.04
- **Python 버전:** Python 3.7 이상
- **필수 라이브러리:**
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
    git clone https://github.com/libero0077/RokeyProjects
    cd RokeyProjects/ServiceRobotProject/B5
    colcon build
    source install/setup.bash
    ```

2. **시스템 종속성 설치:**

    ```bash
    sudo apt update
    sudo apt install python3-pyqt5 python3-rosdep python3-rosinstall python3-rosinstall-generator python3-wstool build-essential
    ```


3. **데이터베이스 초기화:**

    데이터베이스 파일이 존재하지 않으면 `db_manager.py` 스크립트를 실행하여 자동으로 초기화합니다.

    ```bash
    python src/menu_order_project/db_manager.py
    ```

## 사용법

1. **ROS2 노드 실행:**

    각각의 노드를 별도의 터미널에서 실행해야 합니다. ROS2 환경이 설정되어 있는지 확인하세요.

    - **테이블 오더 노드 실행:**

        ```bash
        python src/menu_order_project/table_order.py
        ```

    - **주방 디스플레이 노드 실행:**

        ```bash
        python src/menu_order_project/menu_order.py
        ```

    - **서빙 로봇 노드 실행:**

        ```bash
        python src/menu_order_project/robot_controller.py
        ```

    - **로봇 모니터링 노드 실행:**

        ```bash
        python src/menu_order_project/robot_monitor.py
        ```

2. **프로젝트 실행:**

    각 노드를 실행한 후, PyQt GUI를 통해 주문을 입력하고, 주방 디스플레이에서 주문을 확인하여 로봇을 제어할 수 있습니다. 로봇 모니터링 GUI를 통해 로봇의 현재 상태를 실시간으로 확인할 수 있습니다.

3. **데이터베이스 확인:**

    주문 내역과 배달 로그는 `restaurant_db.db` 파일에 저장됩니다. `db_manager.py`를 통해 데이터베이스의 상태를 확인할 수 있습니다.

    ```bash
    python src/menu_order_project/db_manager.py
    ```

## 개선 계획

현재 시스템은 기본적인 주문 관리 및 로봇 배달 기능을 갖추고 있지만, 다음과 같은 개선을 통해 더욱 강력하고 효율적인 시스템으로 발전시킬 수 있습니다:

1. **모델 최적화:**
   - **서빙 로봇 경로 최적화:** 로봇의 이동 경로를 최적화하여 배달 시간을 단축하고 에너지 효율을 향상시킵니다.
   - **실시간 장애물 감지:** 로봇에 장애물 감지 센서를 추가하여 실시간으로 경로를 수정할 수 있도록 합니다.

2. **고급 통계 분석 및 예측:**
   - **머신러닝 도입:** 판매 패턴을 분석하여 수요 예측 및 재고 관리에 활용합니다.
   - **사용자 정의 대시보드:** 다양한 통계 지표를 시각화할 수 있는 사용자 정의 대시보드를 개발합니다.

3. **데이터 보안 및 접근 제어:**
   - **데이터베이스 보안 강화:** 데이터베이스 보안을 강화하고, 사용자 인증 및 권한 관리를 통해 데이터 접근을 제어합니다.
   - **실시간 데이터 암호화:** 실시간 데이터 암호화 및 백업 시스템을 도입하여 데이터의 무결성과 보안을 확보합니다.

4. **확장 가능한 아키텍처 구축:**
   - **마이크로서비스 아키텍처:** 마이크로서비스 아키텍처를 도입하여 각 구성 요소를 독립적으로 확장할 수 있도록 합니다.
   - **클라우드 인프라 활용:** 클라우드 인프라를 활용하여 시스템의 가용성과 확장성을 높입니다.

5. **사용자 경험 향상:**
   - **직관적 GUI 개선:** GUI 인터페이스를 더욱 직관적이고 사용자 친화적으로 개선합니다.
   - **모바일 지원:** 모바일 디바이스 지원을 통해 언제 어디서나 시스템을 모니터링할 수 있도록 합니다.

## 기여

이 프로젝트에 기여해주신 모든 분들께 감사드립니다:
- [libero0077](https://github.com/libero0077) : 중앙 제어, DB 및 통계 페이지, 테스트 스크립트 작성, 전체 시스템 통합 
- **양준혁 (Y6HYUK)**: 중앙 제어, DB 및 통계 페이지, 테스트 스크립트 작성, 전체 시스템 통합
- **LeeSW1357**: 데이터 증강 아이디어 모색, 데이터 수집 및 가설 검증
- **juwon407**: 분류 알고리즘 개발, 하드웨어 설계, 제작 및 설치

## 라이선스

이 프로젝트는 [MIT 라이선스](LICENSE)를 따릅니다.

## 연락처

문의 사항이나 지원이 필요하시면 아래 연락처로 연락주세요:

- **이름:** 양준혁
- **GitHub:** [Y6HYUK](https://github.com/Y6HYUK)

---

## 추가 참고 자료

- [ROS2 공식 문서](https://docs.ros.org/en/foxy/index.html)
- [NAV2 공식 문서](https://navigation.ros.org/)
- [PyQt5 공식 문서](https://www.riverbankcomputing.com/static/Docs/PyQt5/)
- [SQLite 공식 문서](https://www.sqlite.org/docs.html)
- [GitHub Actions](https://github.com/features/actions)
