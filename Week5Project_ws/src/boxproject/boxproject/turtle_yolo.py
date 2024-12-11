import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge
from ultralytics import YOLO
import cv2
import json

class USBCameraWithYOLO(Node):
    def __init__(self):
        super().__init__('usb_camera_with_yolo_track')
        self.image_publisher = self.create_publisher(Image, '/usb_camera/image_raw', 10)
        self.detection_publisher = self.create_publisher(String, 'usb_camera/detections', 10)

        self.camera_device = "/dev/video0"
        self.cap = cv2.VideoCapture(self.camera_device)

        if not self.cap.isOpened():
            self.get_logger().error("Cannot open camera device.")
            return

        self.bridge = CvBridge()
        # YOLO 모델 로드 - track 기능 사용 위해 persist=True 옵션 등 사용
        self.yolo_model = YOLO("/home/rokey11/_best_new/best.pt")

        # 0.5초에 한 번씩 프레임 읽고 처리
        self.timer = self.create_timer(0.5, self.process_frame)

        self.get_logger().info("USB Camera with YOLO tracking started")

    def process_frame(self):
        ret, frame = self.cap.read()     
        if not ret:
            self.get_logger().error("Failed to grab frame from camera.")
            return

        try:
            # YOLO 추적 수행: track 모드
            # persist=True로 한번 id 매긴 객체 유지
            results = self.yolo_model.track(frame, persist=True)

            detections = []
            # track 결과에서 bounding box, id, cls 추출
            # ultralytics YOLOv8 track 모드 결과 boxes에 id 포함
            # 각 boxes 안에 .id, .cls, .conf, .xyxy 등 존재
            # results[0].boxes: Box들의 리스트 형태
            for box in results[0].boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                confidence = float(box.conf[0].item())
                class_id = int(box.cls[0].item())
                track_id = int(box.id[0].item()) if box.id is not None else -1
                label = self.yolo_model.names[class_id]

                # label_id = label + track_id 형태
                # 예: red3, blue5
                label_id = f"{label}{track_id}"

                detections.append({
                    "label": label,
                    "label_id": label_id,
                    "bbox": [int(x1), int(y1), int(x2), int(y2)],
                    "confidence": confidence
                })

            # 탐지 결과 퍼블리시
            detection_msg = String()
            detection_msg.data = json.dumps(detections)
            self.detection_publisher.publish(detection_msg)

            # 원본 이미지 퍼블리시
            img_msg = self.bridge.cv2_to_imgmsg(frame, encoding='bgr8')
            self.image_publisher.publish(img_msg)

        except Exception as e:
            self.get_logger().error(f"Error during YOLO tracking: {e}")

    def destroy_node(self):
        self.cap.release()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = USBCameraWithYOLO()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Shutting down USB camera with YOLO tracking node...')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
