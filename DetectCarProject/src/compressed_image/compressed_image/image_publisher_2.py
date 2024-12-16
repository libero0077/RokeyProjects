import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage #sensor_msgs.msg.Image 대신 sensor_msgs.msg.CompressedImage로 변경
import cv2
from cv_bridge import CvBridge
import numpy as np

class CameraPublisher2(Node):
    def __init__(self):
        super().__init__('camera_publisher_2')
        # CompressedImage 타입의 퍼블리셔 생성
        # 라인 9: 퍼블리셔 타입을 CompressedImage로 변경하고, 토픽 이름을 camera_image_2/compressed로 설정
        self.publisher_ = self.create_publisher(CompressedImage, 'camera_image_2/compressed', 10)
        timer_period = 0.1  # Publish at 10 Hz
        self.timer = self.create_timer(timer_period, self.publish_image)
        self.cap = cv2.VideoCapture('/dev/video0')  # 두 번째 카메라 장치
        self.bridge = CvBridge()

        if not self.cap.isOpened():
            self.get_logger().error('Failed to open camera 2')
            raise RuntimeError('Camera 2 not accessible')

    def publish_image(self):
        ret, frame = self.cap.read()
        if ret:
            # 이미지 압축 (JPEG 형식으로 압축) / [cv2.IMWRITE_JPEG_QUALITY, 80] 숫자는 압축률을 의미
            # 라인 21: ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])로 이미지 압축을 추가
            # 이 코드는 frame을 JPEG 형식으로 압축하며, 80은 JPEG 압축 품질을 의미
            ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 50])
            if not ret:
                self.get_logger().warn('Failed to compress image from camera 2')
                return
            
            # 압축된 이미지를 CompressedImage 메시지로 변환
            '''
            라인 26~29: CompressedImage 메시지를 생성하고, 압축된 이미지 데이터를 메시지에 할당하는 부분을 추가
            msg.format = "jpeg"는 메시지 포맷을 설정하며, 
            msg.data = np.array(buffer).tobytes()는 압축된 이미지를 바이트 형식으로 할당
            '''
            msg = CompressedImage()
            msg.header.stamp = self.get_clock().now().to_msg()
            msg.format = "jpeg"
            msg.data = np.array(buffer).tobytes()
            
            # 퍼블리시
            self.publisher_.publish(msg)
            self.get_logger().info('Published compressed image from camera 2')
        else:
            self.get_logger().warn('Failed to capture image from camera 2')

    def destroy_node(self):
        self.cap.release()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    camera_publisher = CameraPublisher2()

    try:
        rclpy.spin(camera_publisher)
    except KeyboardInterrupt:
        pass
    finally:
        camera_publisher.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
