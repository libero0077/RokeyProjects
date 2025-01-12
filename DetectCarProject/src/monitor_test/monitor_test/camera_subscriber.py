import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class CameraSubscriber(Node):
    def __init__(self):
        super().__init__('camera_subscriber_node')
        
        # 두 개의 토픽 구독자 설정
        self.subscription1 = self.create_subscription(
            Image,
            '/camera/image1',
            self.listener_callback1,
            10
        )
        
        self.subscription2 = self.create_subscription(
            Image,
            '/camera/image2',
            self.listener_callback2,
            10
        )
        
        # OpenCV와 ROS 간 이미지 변환을 위한 브리지 생성
        self.bridge = CvBridge()

    def listener_callback1(self, msg):
        # 첫 번째 토픽의 이미지 수신 및 처리
        self.get_logger().info('Received image from /camera/image1')
        # ROS Image 메시지를 OpenCV 이미지로 변환
        cv_image = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        # OpenCV 창에 이미지를 표시 (디버깅 용도)
        cv2.imshow('Camera Image 1', cv_image)
        cv2.waitKey(1)

    def listener_callback2(self, msg):
        # 두 번째 토픽의 이미지 수신 및 처리
        self.get_logger().info('Received image from /camera/image2')
        # ROS Image 메시지를 OpenCV 이미지로 변환
        cv_image = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        # OpenCV 창에 이미지를 표시 (디버깅 용도)
        cv2.imshow('Camera Image 2', cv_image)
        cv2.waitKey(1)

def main(args=None):
    rclpy.init(args=args)
    camera_subscriber = CameraSubscriber()
    
    try:
        rclpy.spin(camera_subscriber)
    except KeyboardInterrupt:
        pass
    finally:
        # 종료 시 노드와 OpenCV 창 닫기
        camera_subscriber.destroy_node()
        rclpy.shutdown()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()