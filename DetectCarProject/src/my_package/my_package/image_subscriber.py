import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import time
import json
import csv
import math
import os
import shutil
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

def is_inside_polygon(point, polygon):
    """
    점이 다각형 내부에 있는지 확인하는 함수입니다.
    """
    poly_array = np.array(polygon, dtype=np.int32)
    result = cv2.pointPolygonTest(poly_array, point, False)
    return result >= 0

class CameraSubscriber(Node):
    def __init__(self):
        super().__init__('camera_subscriber')
        self.subscription = self.create_subscription(
            Image,
            'camera_image',
            self.image_callback,
            10
        )
        self.bridge = CvBridge()
        
        # YOLO 모델 로드
        self.model = YOLO('/home/yjh/Doosan/Real_project_ws/Week2/_best.pt')  # 모델 경로 설정
        self.output_dir = './output'
        os.makedirs(self.output_dir, exist_ok=True)
        
        cv2.namedWindow('Webcam')
        cv2.setMouseCallback('Webcam', draw_polygon)

    def image_callback(self, msg):
        # ROS 이미지를 OpenCV 이미지로 변환
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        
        # YOLO 감지 결과 처리
        results = self.model(frame, stream=True)
        object_count = 0
        classNames = ['Car']
        csv_output = []
        confidences = []
        fontScale = 1
        max_object_count = 0
        alarm_triggered = False

        # 마우스 클릭 좌표에 원을 그려 표시
        for point in points:
            cv2.circle(frame, point, 5, (0, 255, 0), -1)

        # 클릭된 좌표들로 다각형을 그림
        if len(points) == 4:  # 4개의 점을 찍었을 때 마우스 클릭 이벤트의 점들만 이어서 사각형 생성
            poly_array = np.array(points, np.int32)
            cv2.polylines(frame, [poly_array], isClosed=True, color=(255, 0, 0), thickness=2)

            # YOLO 결과 처리
            for r in results:
                boxes = r.boxes
                for box in boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

                    confidence = math.ceil((box.conf[0] * 100)) / 100
                    cls = int(box.cls[0])
                    confidences.append(confidence)

                    org = [x1, y1]
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    color = (255, 0, 0)
                    thickness = 2

                    # 탐지된 물체의 이름과 함께 정확도를 화면에 표시
                    cv2.putText(frame, f"{classNames[cls]}: {confidence}", org, font, fontScale, color, thickness)

                    # CSV로 저장할 데이터 추가
                    csv_output.append([x1, y1, x2, y2, confidence, cls])

                    # 바운딩 박스 중앙 좌표
                    center_x = (x1 + x2) // 2
                    center_y = (y1 + y2) // 2

                    # 다각형 내부에 바운딩 박스가 포함되지 않으면 알람을 트리거
                    if not is_inside_polygon((center_x, center_y), points):
                        alarm_triggered = True

                    object_count += 1

            max_object_count = max(max_object_count, object_count)
            cv2.putText(frame, f"Objects_count: {object_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, fontScale, (0, 255, 0), 1)

            # 물체가 검출될 때마다 이미지 저장
            if object_count > 0:
                cv2.imwrite(os.path.join(self.output_dir, f'output_{int(time.time())}.jpg'), frame)

            # 알람 트리거 시 알림 메시지 표시
            if alarm_triggered:
                cv2.putText(frame, "ALARM: Object outside region!", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, fontScale, (0, 0, 255), 2)

        # 이미지 출력
        cv2.imshow('Webcam', frame)
        if cv2.waitKey(1) == ord('q'):
            with open(os.path.join(self.output_dir, 'output.csv'), 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(csv_output)
            with open(os.path.join(self.output_dir, 'output.json'), 'w') as file:
                json.dump(csv_output, file)
            with open(os.path.join(self.output_dir, 'statistics.csv'), 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Max Object Count', 'Average Confidence'])
                writer.writerow([max_object_count, sum(confidences) / len(confidences) if confidences else 0])
            rclpy.shutdown()

def main(args=None):
    rclpy.init(args=args)
    camera_subscriber = CameraSubscriber()
    try:
        rclpy.spin(camera_subscriber)
    except KeyboardInterrupt:
        pass
    finally:
        cv2.destroyAllWindows()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
