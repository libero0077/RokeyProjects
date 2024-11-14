import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class ImageSubscriber(Node):
    def __init__(self):
        super().__init__('image_subscriber')
        self.bridge = CvBridge()
        
        # 두 개의 토픽을 구독
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

    def image_callback_1(self, msg):
        # 첫 번째 이미지 토픽에서 받은 메시지 처리
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        cv2.imshow("Camera Image 1", frame)
        cv2.waitKey(1)

    def image_callback_2(self, msg):
        # 두 번째 이미지 토픽에서 받은 메시지 처리
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        cv2.imshow("Camera Image 2", frame)
        cv2.waitKey(1)

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
