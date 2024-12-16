import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage
import cv2
from cv_bridge import CvBridge
import numpy as np

class CameraPublisher1(Node):
    def __init__(self):
        super().__init__('camera_publisher_1')
        self.publisher_ = self.create_publisher(CompressedImage, 'camera_image_1/compressed', 10)
        timer_period = 0.1  # Publish at 10 Hz
        self.timer = self.create_timer(timer_period, self.publish_image)
        self.cap = cv2.VideoCapture('/dev/video2')  # 첫 번째 카메라 장치 (usb 웹캠 : video2)
        self.bridge = CvBridge()

        if not self.cap.isOpened():
            self.get_logger().error('Failed to open camera 1')
            raise RuntimeError('Camera 1 not accessible')

    def publish_image(self):
        ret, frame = self.cap.read()
        if ret:
            # 이미지 압축 (JPEG 형식으로 압축)
            ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 50])  # 압축률은 필요에 따라 조절 가능
            if not ret:
                self.get_logger().warn('Failed to compress image from camera 1')
                return
            
            # 압축 이미지를 CompressedImage 메시지로 변환
            msg = CompressedImage()
            msg.header.stamp = self.get_clock().now().to_msg()
            msg.format = "jpeg"
            msg.data = np.array(buffer).tobytes()
            
            # 퍼블리시
            self.publisher_.publish(msg)
            self.get_logger().info('Published compressed image from camera 1')
        else:
            self.get_logger().warn('Failed to capture image from camera 1')

    def destroy_node(self):
        self.cap.release()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    camera_publisher = CameraPublisher1()

    try:
        rclpy.spin(camera_publisher)
    except KeyboardInterrupt:
        pass
    finally:
        camera_publisher.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
