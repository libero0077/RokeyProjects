# 두산 로봇 활용
## 프로젝트 기간 : 2024.12.17 ~ 2024.12.23

------------------------------------------

### 데모영상

- 3*3형태 pallet에 블록배치 : https://youtu.be/q8Xm6hnT-i8
- 젠가 쌓기 : https://youtu.be/GRrfOn8wpvs
- 기어 조립 : https://youtu.be/4eTDPMtYRCM
- socket통신을 이용한 두 로봇팔의 블록 전달 : https://youtu.be/f1HJRCGwliU
- sport stacking : https://youtu.be/4_s6fq9cKoA

------------------------------------------

## 목차

- [개요](#개요)
- [주요 기능](#주요-기능)
- [task](#task)
  - [3*3형태 pallet에 블록배치](#3*3형태-pallet에-블록배치)
  - [젠가 쌓기](#젠가-쌓기)
  - [기어 조립](#기업-조립)
  - [socket통신을 이용한 두 로봇팔의 블록 전달 과정 구현](#socket통신을-이용한-두-로봇팔의-블록-전달-과정-구현)
  - [sport stacking](sport-stacking)
- [디렉토리 구조](#디렉토리)
- [설치](#설치)
- [사용법](#사용법)
- [개선 계획](#개선-계획)
- [기여](#기여)
- [연락처](#연락처)
- [추가 참고 자료](#추가-참고-자료)

## 개요

**DOOSAN 로봇 프로젝트**는 두산 로봇 M0609모델을 사용하며, DSR(Doosan Software for Robotics)패키지와 ROS(Robot Operating System)환경을 활용하여 다양한 task를 진행합니다. 이 프로젝트는 3*3형태의 pallet에 블록의 길이 순서대로 배치하는 task, 젠가를 쌓는 task, 기어를 조립하는 task, socket통신을 이용한 두 로봇팔의 블록 전달 task, sport stacking task로 이루어집니다. 현장에서의 실제 task들을 간소화하여 진행하였으며 이를 활용하여 일관된 task 진행과 정밀제어를 통해 효율성 및 제품의 고품질 유지를 보장합니다.

## 주요 기능

- **힘 제어 시스템:** 정밀한 힘 감지를 통해 물체의 높이를 측정할 수 있으며 안전성을 강화할 수 있습니다.
- **그리퍼 제어:** 디지털 입출력을 이용하여 정확한 그리퍼 동작을 제어할 수 있습니다.
- **위치 제어:** DRL(Doosan Robotics Language)을 이용하여 모델의 조인트 및 툴 작업 속도 및 가속도 등을 정밀하게 조정하여 위치를 제어할 수 있습니다.
- **작업 순서 최적화:** 센서 데이터와 로봇 동작을 병렬로 처리하며, 홈 포지션과 각 작업의 목표 위치를 미리 정의하여 불필요한 계산을 줄이고 이에 따라 효율적으로 작업 순서를 정해서 진행할 수 있습니다. 
- **통신 최적화:** socket 통신을 사용하여 양방향 실시간 데이터 교환이 가능하며 다수의 로봇 팔을 각각 제어할 수 있으며 효율적으로 작업을 진행할 수 있습니다.


## task

### 3*3형태 pallet에 블록배치

- **파일:** `pallet_control.py`
- **설명:** 3*3형태의 pallet에 random하게 배치된 블록을 높이에 따라 정렬합니다.
- **주요 기능:**
  - ROS2와 Doosan 로봇 시스템 통합
  - 힘 제어 : task_compliance_ctrl와 set_desired_force를 사용하여 블록을 감지하고 안전하게 조작
  - 위치 제어 : movej와 movel를 사용하여 로봇 팔을 정확한 위치로 이동
  - 그리퍼 제어 : 디지털 입출력을 통해 그리퍼를 제어하여 블록 픽업 및 배치
  - 블록 높이에 따른 홈 레벨 설정 : 블록의 높이에 따라 적절한 홈 레벨을 동적으로 결정

### 젠가 쌓기

- **파일:** `jenga_stacker.py`
- **설명:**  Jenga 블록을 18층까지 쌓아 초기의 jenga 형태를 만듭니다.
- **주요 기능:**
  - 힘 제어 : task_compliance_ctrl와 set_desired_force를 사용하여 블록을 감지하고 안전하게 조작
  - 위치 제어 : movej와 movel를 사용하여 로봇 팔을 정확한 위치로 이동
  - 그리퍼 제어 : 디지털 입출력을 통해 그리퍼를 제어
  - 층별 배치 : 짝수 층에서는 그리퍼를 90도 회전시켜 블록을 교차 배치 

### 기어조립

- **파일:** `gear_assembly.py`
- **설명:** 지정된 시작 위치에서 기어를 집어 목표 위치로 이동하여 조립하는 작업을 실행합니다.
- **주요 기능:**
  - 힘 제어 : task_compliance_ctrl와 set_desired_force, check_force_condition를 사용하여 블록을 감지하고 안전하게 조작
  - 위치 제어 : movej와 movel를 사용하여 로봇 팔을 정확한 위치로 이동
  - 그리퍼 제어 : 디지털 입출력을 통해 그리퍼를 제어
  - 4번째 기어(가운데 기어)에 대해서는 추가적인 힘 제어 및 periodic 동작 수행
  - 힘 제어를 하는 동안에 periodic을 진행시키고, 특정 높이까지 하강하면 release를 하는 구조

### socket통신을 이용한 두 로봇팔의 블록 전달 과정 구현

- **파일:** `two_robot_socket_server.py`, 'two_robot_socket_client.py'
- **설명:** socket통신을 이용하여 서로 다른 두 로봇팔끼리 블록을 전달합니다.
- **주요 기능:**
  - socket_server_thread를 사용하여 소켓 서버를 실행하며 SocketClientThread를 통해 클라이언트 측에서 서버와 연결
  - 통신 및 로봇 제어: socket 서버와 클라이언트가 연결이 되면 클라이언트와 서버 간의 통신이 시작되고 로봇 제어 명령이 전달
  - 멀티스레딩: 소켓 서버와 로봇 제어를 별도의 스레드에서 실행
  - 힘 제어 : task_compliance_ctrl와 set_desired_force, check_force_condition를 사용하여 블록을 감지하고 안전하게 조작
  - 위치 제어 : movej와 movel를 사용하여 로봇 팔을 정확한 위치로 이동
  - 그리퍼 제어 : 서버는 명령 수신 및 실행을 하고 클라이언트는 명령 전송 및 응답 처리를 통해 그리퍼 제어
  
  
### sport stacking

- **파일:** `cup_stacker.py`
- **설명:** 11개의 컵을 한 번에 옮기면서 그리퍼를 사선 방향으로 하고 하나씩 컵을 놔두면서 피라미드 모양(6-3-1-1)의 sport stacking을 진행합니다. 
- **주요 기능:**
  - 기울임 동작 : 컵을 쌓을 때 그리퍼를 특정 각도로 기울이는 동작(TILT_ANGLE = 120.0) 포함
  - stacking : 층(layer), 라인(line), 컵(cup)의 순서를 기반으로 피라미드 형태로 stacking 진행
  - 좌표 이동 : movel, amovel, movec 등을 통해 효율적인 동선 구축 및 stacking 시간 단축
  - 힘 제어 : task_compliance_ctrl와 set_desired_force, check_force_condition를 사용하여 블록을 감지하고 안전하게 조작
  - 그리퍼 제어 : 디지털 입출력을 통해 그리퍼를 제어
  
  
## 디렉토리 구조
```bash
├── B5_Sportstaking_발표자료.pdf
├── B5_Sportstaking_발표자료.pptx
├── README.md
├── cup_stacker.py
├── cup_stacker_with_algorithm.py
├── gear_assembly.py
├── jenga_stacker.py
├── jenga_stacker_faster.py
├── pallet_control.py
├── two_robot_socket_client.py
└── two_robot_socket_server.py

0 directories, 11 files

```

## 설치

### 필수 사항

- **Python 3.7 이상**
- **필수 라이브러리:**
  - `rclpy`
  - `DR_init`
  - `math`
  - `time`
  - `threading`
  - `socket`
  - 'queue'

### 설치 단계 (<ros-distro>는  호환되는 ROS 2 배포판(예: Foxy, Galactic, Humble) 입니다)

1. **ros2 설치:**

    ```bash
    sudo apt update && sudo apt upgrade -y
    sudo apt install software-properties-common
    sudo add-apt-repository universe
    sudo apt install curl
    sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
    sudo apt update
    sudo apt install ros-<ros-distro>-desktop python3-argcomplete
    
    ```
    

2. **ROS2 환경 설정:**

    ```bash
    echo "source /opt/ros/<ros-distro>/setup.bash" >> ~/.bashrc
    source ~/.bashrc

    ```
    
3. **ROS2 디렉토리 생성 및 저장소 클론:**

    ```bash
    mkdir -p ~/ros2_ws/src    
    cd ~/ros2_ws/src
    git clone https://github.com/doosan-robotics/doosan-robot2
    colcon build
    ```
    
4. **링크에 있는 py들을 디렉토리에 복사:**
   https://github.com/libero0077/RokeyProjects/tree/main/DoosanRobotProejct

5. **의존성 패키지 설치 및 작업 공간 빌드:**
   ```bash
    sudo apt install ros-<ros-distro>-rqt* ros-<ros-distro>-moveit* ros-<ros-distro>-gazebo-ros-pkgs ros-<ros-distro>-gazebo-ros2-control ros-<ros-distro>-joint-state-publisher-gui
    cd ~/ros2_ws
    colcon build --symlink-install
    source install/setup.bash

    ```

6. **ROS2 개발 환경에서 필요한 Python 모듈 로드 및 Doosan 로봇을 조작하는 launch 파일을 실행:**
   ```bash
   export PYTHONPATH=$PYTHONPATH:~/ros2_ws/install/common2/lib/common2/imp
   ros2 launch dsr_bringup2 dsr_bringup2_gazebo.launch.py mode:=real host:=[로봇과 동일한 ip] model:=[사용하려는 실제 로봇 모델]
   
   '''

## 사용법

1. ** 3*3형태 pallet에 블록배치 실행:**

    ```bash
    python pallet_control.py
    ```

2. **젠가 쌓기 실행:**

    ```bash
    python jenga_stacker.py
    ```

3. **기어 조립 실행:**

    ```bash
    python gear_assembly.py
    ```

4. **socket통신을 이용한 두 로봇팔의 블록 전달 실행:**

        먼저 서버를 실행한 후 클라이언트를 실행합니다.

    ```bash
    python two_robot_socket_server.py
    python two_robot_socket_client.py
    ```
    
5. **sport stacking 실행:**

    ```bash
    python cup_stacker.py
    ```


## 개선 계획

1. **3*3형태 pallet에 블록배치:**
   - **촉각 센서 통합:** 그리퍼에 고감도 촉각 센서를 추가하여 블록 파지 및 조작의 정밀도를 향상시킵니다.

2. **젠가 쌓기:**
   - **피드백 루프:** 각 블록 적재 후 적재 상태를 확인하는 피드백 루프를 추가하여 안정성을 높입니다.
   - **3D 비전 센서 활용:** 블록의 정확한 위치와 방향을 감지하여 정밀성을 높입니다.

3. **기어 조립:**
   - **컴퓨터 비전 통합:** OpenCV를 사용하여 카메라 피드백을 통해 기어의 정확한 위치와 방향을 감지하고, 이를 바탕으로 로봇의 움직임을 미세 조정할 수 있습니다.

4. **socket통신을 이용한 두 로봇팔의 블록 전달:**
   - **재연결 매커니즘:** 서버와의 연결이 끊어졌을 때 자동으로 재연결을 시도하는 로직을 추가해서 기능을 개선합니다.
   - **인증 메커니즘:** 클라이언트 연결 시 간단한 인증 절차를 추가하여 보안을 강화합니다.

5. **sport stacking:**
   - **힘-토크 센서 통합:** 힘-토크 센서를 로봇 팔에 통합하여 "촉각" 기능을 추가하여 컵을 다룰 때 적용되는 힘을 더 정밀하게 제어할 수 있습니다.
   - **소프트 로보틱스 적용:** 부드러운 소재를 사용한 그리퍼를 도입하여 안정성을 강화합니다.

## 기여

- [libero0077](https://github.com/libero0077) : 사선 방향 접근 스택킹 아이디어 모색, 사선 방향 접근 아이디어 기반 스택킹 구현, pallet에 random하게 배치된 블록을 높이에 따라 정렬하는 알고리즘 구현
- [Y6HYUK](https://github.com/Y6HYUK) : 사선 방향 접근 스택킹 아이디어 모색, 아이디어 결과를 검증할 비교 대상(수직 방향 접근 스택킹)개발
- [leesw1357](https://github.com/leesw1357) : 아이디어 결과를 검증할 비교 대상(수직 방향 접근 스택킹)개발
- [juwon407](https://github.com/juwon407) : 사선 방향 접근 스택킹 아이디어 모색, 사선 방향 접근 아이디어 기반 스택킹 구현, socket 클라이언트 및 서버 구현


## 연락처

문의 사항이나 지원이 필요하시면 아래 연락처로 연락주세요:

- **이름:** Sangwoo Lee
- **GitHub:** [leesw1357](https://github.com/leesw1357)

---

## 추가 참고 자료

- [Doosan Robotics 문서](https://manual.doosanrobotics.com/?l=ko)
- [ROS2 공식 문서](https://docs.ros.org/)
- [Socket 공식 문서](https://socket.io/docs/v4/)
