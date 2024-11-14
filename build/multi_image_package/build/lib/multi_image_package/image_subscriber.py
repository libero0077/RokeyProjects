import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import time
from ultralytics import YOLO
import numpy as np

# 마우스로 설정된 좌표를 저장할 리스트
points = []

# 마우스 이벤트 콜백 함수
def draw_polygon(event, x, y, flags, param):
    global points
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        print(f"Point {len(points)}: ({x}, {y})")

# 점이 다각형 내부에 있는지 확인하는 함수
def is_inside_polygon(point, polygon):
    poly_array = np.array(polygon, dtype=np.int32)
    result = cv2.pointPolygonTest(poly_array, point, False)
    return result >= 0

class ImageSubscriber(Node):
    def __init__(self):
        super().__init__('image_subscriber')
        self.bridge = CvBridge()

        # 두 개의 이미지 토픽을 구독
        self.subscription_1 = self.create_subscription(
            Image,
            'camera_image_1',
            self.image_callback_1,
            10
        )
        self.subscription_2 = self.create_subscription(
            Image,
            'camera_image_2',
            self.image_callback_2,
            10
        )

        # YOLO 모델 로드
        try:
            self.model = YOLO('/home/yjh/Doosan/Real_project_ws/Week2/_best.pt')  # 올바른 모델 경로로 수정
            self.get_logger().info('YOLO 모델 로드 성공')
        except Exception as e:
            self.get_logger().error(f'YOLO 모델 로드 실패: {e}')
            self.model = None  # 모델 로드 실패 시 None으로 설정

        # 클래스 이름 목록 ###########11.14 추가했음 ####
        self.classNames = ['car']  # 여기에 모델의 클래스 이름을 추가 (예: 'Car', 'Truck' 등)

        # OpenCV 창과 마우스 이벤트 설정
        cv2.namedWindow("Camera Image 1")
        cv2.setMouseCallback("Camera Image 1", draw_polygon)  # 첫 번째 카메라에 마우스 이벤트 설정
        cv2.namedWindow("Camera Image 2")

        

    def process_frame_with_yolo_and_polygon(self, frame, window_name):
        # 모델이 없으면 함수 종료
        if self.model is None:
            self.get_logger().error('YOLO 모델이 로드되지 않아 프레임을 처리할 수 없습니다.')
            return

        # YOLO 감지 전 시간 측정
        start_time = time.time()
        results = self.model(frame, stream=True)
        self.get_logger().info(f'YOLO 처리 시간: {time.time() - start_time:.2f}초')

        alarm_triggered = False  # 알람 상태

        # YOLO 결과 박스 그리기 및 다각형 영역 확인
        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

                # 바운딩 박스의 중심 좌표
                center_x = (x1 + x2) // 2
                center_y = (y1 + y2) // 2

                ##### 바운딩박스의 클래스 정보, confidence를 텍스트로 출력하는 코드 추가 11.14 #####
                # 클래스와 confidence 정보 표시
                cls = int(box.cls[0])  # 클래스 인덱스
                confidence = box.conf[0]  # 신뢰도 (confidence)
                org = (x1, y1 - 10)  # 텍스트 위치 (바운딩 박스 위)
                font = cv2.FONT_HERSHEY_SIMPLEX
                fontScale = 0.5
                color = (0, 255, 0)  # 텍스트 색상 (초록색)
                thickness = 1

                # 클래스 이름과 confidence를 텍스트로 표시
                if cls < len(self.classNames):
                    cv2.putText(frame, f"{self.classNames[cls]}: {confidence:.2f}", org, font, fontScale, color, thickness)

                # 다각형 내에 있는지 확인
                if len(points) == 4:  # 다각형이 최소 3개 점으로 정의된 경우
                    if not is_inside_polygon((center_x, center_y), points):
                        alarm_triggered = True  # 다각형 영역 밖에 있으면 알람 활성화

        # 알람이 활성화되면 화면에 표시
        if alarm_triggered:
            cv2.putText(frame, "ALARM: Object outside region!", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # 다각형 그리기
        for point in points:
            cv2.circle(frame, point, 5, (0, 255, 0), -1)  # 클릭한 좌표에 원 표시
        if len(points) >= 3:  # 최소 3개의 점을 클릭한 경우에만 다각형을 그림
            poly_array = np.array(points, np.int32)
            cv2.polylines(frame, [poly_array], isClosed=True, color=(255, 0, 0), thickness=2)

        cv2.imshow(window_name, frame)
        cv2.waitKey(1)

    def process_frame_no_yolo_no_polygon(self, frame, window_name):
        # 두 번째 카메라에 YOLO와 다각형을 적용하지 않고 단순히 영상을 표시
        cv2.imshow(window_name, frame)
        cv2.waitKey(1)

    def image_callback_1(self, msg):
        # 첫 번째 이미지 토픽에서 받은 메시지 처리 (YOLO와 다각형 적용)
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        self.process_frame_with_yolo_and_polygon(frame, "Camera Image 1")

    def image_callback_2(self, msg):
        # 두 번째 이미지 토픽에서 받은 메시지 처리 (YOLO와 다각형 미적용)
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        self.process_frame_no_yolo_no_polygon(frame, "Camera Image 2")

def main(args=None):
    rclpy.init(args=args)
    image_subscriber = ImageSubscriber()
    try:
        rclpy.spin(image_subscriber)
    except KeyboardInterrupt:
        pass
    finally:
        cv2.destroyAllWindows()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
