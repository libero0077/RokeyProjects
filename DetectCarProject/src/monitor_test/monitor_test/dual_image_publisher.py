import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge
import cv2

class CameraPublisher(Node):
    def __init__(self):
        super().__init__('camera_publisher_node')
        
        # CompressedImage 메시지 타입으로 두 개의 퍼블리셔를 설정
        self.publisher1 = self.create_publisher(CompressedImage, '/camera/image1/compressed', 10)
        self.publisher2 = self.create_publisher(CompressedImage, '/camera/image2/compressed', 10)
        
        # OpenCV와 ROS 간 이미지 변환을 위한 브리지 생성
        self.bridge = CvBridge()
        
        # 타이머를 설정하여 이미지를 주기적으로 퍼블리싱
        self.timer = self.create_timer(0.05, self.publish_images1)  # 0.1초 간격(10Hz)
        #self.timer = self.create_timer(0.1, self.publish_images2)  # 0.1초 간격(10Hz)
    

        # USB 카메라 연결 (기본 장치 ID는 2)
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.get_logger().error('Failed to open camera')
    
    
    def publish_images1(self):
        # 카메라에서 프레임 읽기
        ret, frame = self.cap.read()
        if not ret:
            self.get_logger().warning('No frame received from camera')
            return
        
        resized_frame = cv2.resize(frame, (640, 480), interpolation=cv2.INTER_LINEAR)
        
        # OpenCV 이미지를 압축된 ROS Image 메시지로 변환
        _, buffer = cv2.imencode('.jpg', resized_frame, [cv2.IMWRITE_JPEG_QUALITY, 80])  # JPEG 압축 품질 80 설정
        compressed_image_msg = CompressedImage()
        compressed_image_msg.format = "jpeg"
        compressed_image_msg.data = buffer.tobytes()
        
        # 두 개의 퍼블리셔에 동일한 압축 이미지를 퍼블리싱
        self.publisher1.publish(compressed_image_msg)
        #self.publisher2.publish(compressed_image_msg)
        
        self.get_logger().info('Published compressed images to /camera/image1/compressed')

    def publish_images2(self):
        # 카메라에서 프레임 읽기
        ret, frame = self.cap.read()
        if not ret:
            self.get_logger().warning('No frame received from camera')
            return
        
        resized_frame = cv2.resize(frame, (640, 480), interpolation=cv2.INTER_LINEAR)
        
        # OpenCV 이미지를 압축된 ROS Image 메시지로 변환
        _, buffer = cv2.imencode('.jpg', resized_frame, [cv2.IMWRITE_JPEG_QUALITY, 80])  # JPEG 압축 품질 80 설정
        compressed_image_msg = CompressedImage()
        compressed_image_msg.format = "jpeg"
        compressed_image_msg.data = buffer.tobytes()
        
        # 두 개의 퍼블리셔에 동일한 압축 이미지를 퍼블리싱
        #self.publisher1.publish(compressed_image_msg)
        self.publisher2.publish(compressed_image_msg)
        
        self.get_logger().info('Published compressed images to /camera/image2/compressed')
    
    
    def __del__(self):
        # 카메라 자원을 해제
        if self.cap.isOpened():
            self.cap.release()

def main(args=None):
    rclpy.init(args=args)
    camera_publisher = CameraPublisher()
    
    try:
        rclpy.spin(camera_publisher)
    except KeyboardInterrupt:
        pass
    finally:
        # 종료 시 노드와 리소스 해제
        camera_publisher.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
