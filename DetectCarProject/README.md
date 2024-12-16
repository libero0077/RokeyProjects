# AMR 기반 음주 단속 회피 차량 추적 시스템
이 프로젝트는 음주 단속 현장에서 도주하거나 우회하는 차량을 실시간으로 감지하고 추적하기 위한 AMR(Autonomous Mobile Robot) 기반 시스템을 개발하는 것을 목표로 합니다. 객체 탐지, 데이터 전송, 모니터링 인터페이스를 포함하여 다양한 기능을 구현하고 있습니다.

# 📋 프로젝트 구성
## 1. Image Publisher 노드
- Publisher 노드 1: 도주 차량을 감지하기 위한 고정 카메라 데이터를 퍼블리싱.
- Publisher 노드 2: AMR 또는 드론에서 수집된 실시간 카메라 데이터를 퍼블리싱.
## 2. Image Subscriber 노드
- Publisher 노드에서 전송된 데이터를 수신하여 YOLO 모델을 활용해 차량 감지 및 이상 상황 분석.
## 3. YOLO 객체 탐지
- YOLO 모델 통합: 도주 차량 및 우회 차량을 실시간으로 감지하는 AI 모델.
- AMR 및 드론의 카메라 피드에서 객체를 분석하여 경고 메시지를 생성.
## 4. Flask 기반 대시보드
- 사용자 친화적인 웹 대시보드를 통해 AMR 상태, 차량 추적 데이터 및 알림 관리.
- 실시간 데이터 시각화 및 수동 제어 기능 지원.
# 💻 현재까지 구현된 주요 기능
- ROS 기반 노드 구현: Image Publisher 및 Subscriber 노드 완성.
- YOLO 객체 탐지 통합: 도주 차량 및 우회 차량 탐지 기능 구현.
- Flask 웹 대시보드: 실시간 차량 위치 및 상태 모니터링 기능 개발.
- 데이터 전송 및 처리: AMR과 서버 간 실시간 데이터 처리와 통신.
# 🚀 사용 기술
- Python: 주요 구현 언어.
- ROS2: AMR의 노드 통신 및 제어.
- YOLOv8: 차량 객체 탐지를 위한 AI 모델.
- Flask: 대시보드 백엔드 및 데이터 시각화.
# 📂 향후 계획
- AMR의 자율 네비게이션 기능 추가.
- 네트워크 장애 시 백업 통신 기능 구현.
- 데이터 보안 강화 및 시스템 최적화.
## 구상중인 Node 구현 계획
전체 노드 구성
- 퍼블리셔 노드 1 (camera_publisher_1)
카메라 1의 이미지를 발행.
- 퍼블리셔 노드 2 (camera_publisher_2)
카메라 2의 이미지를 발행.
- 서브스크라이버 노드 (image_subscriber)
퍼블리셔 노드 1과 2로부터 이미지를 수신.
YOLO 모델로 도주 차량의 바운딩 박스를 계산.
바운딩 박스 중심값을 새로운 토픽(target_coordinates)으로 발행.

- AMR 제어 노드 (amr_navigator)
target_coordinates 토픽을 구독.
중심값을 네비게이션 스택에 전달하여 AMR을 이동.

## 💡 이 프로젝트는 공공 안전을 강화하고 음주 단속의 효율성을 높이기 위해 설계되었습니다. 지속적인 업데이트와 개선이 이루어질 예정입니다.

### Gazebo 시뮬레이션 실행시 다음과 같은 에러가 발생한다면
> [ERROR] [gzclient-2]: process has died [pid 5901, exit code -6, cmd 'gzclient'].

> $ source /usr/share/gazebo/setup.sh

> $ echo "source /usr/share/gazebo/setup.sh" >> ~/.bashrc

> $ source ~/.bashrc
