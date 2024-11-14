import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge

class CameraPublisher1(Node):
    def __init__(self):
        super().__init__('camera_publisher_1')
        self.publisher_ = self.create_publisher(Image, 'camera_image_1', 10)
        timer_period = 0.1  # Publish at 10 Hz
        self.timer = self.create_timer(timer_period, self.publish_image)
        self.cap = cv2.VideoCapture('/dev/video2')  # 첫 번째 카메라 장치
        self.bridge = CvBridge()

        if not self.cap.isOpened():
            self.get_logger().error('Failed to open camera 1')
            raise RuntimeError('Camera 1 not accessible')

    def publish_image(self):
        ret, frame = self.cap.read()
        if ret:
            msg = self.bridge.cv2_to_imgmsg(frame, encoding='bgr8')
            self.publisher_.publish(msg)
            self.get_logger().info('Published image from camera 1')
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


'''
코드 리뷰
노드 초기화 및 구조:

CameraPublisher1 클래스는 Node 클래스를 상속하여 ROS2 노드를 구현하고 있습니다.
초기화 메서드 __init__에서 카메라 장치, 퍼블리셔, CvBridge 객체를 적절히 초기화하여 노드가 실행될 준비를 하고 있습니다.

카메라 연결 확인:
self.cap.isOpened()를 통해 카메라 장치가 올바르게 연결되었는지 확인하고 있습니다.
카메라가 열리지 않을 경우 get_logger().error와 RuntimeError 예외를 통해 문제를 명확히 보고하는 방식은 적절합니다.

이미지 퍼블리시 메서드 (publish_image):
카메라로부터 이미지를 읽고, cv2_to_imgmsg를 통해 ROS2 메시지 형식으로 변환한 뒤 퍼블리시하는 로직이 잘 구현되었습니다.
카메라에서 이미지를 읽는 데 실패할 경우 경고 로그를 출력하도록 하여 문제 상황을 모니터링할 수 있습니다.

자원 정리:
destroy_node 메서드에서 self.cap.release()로 카메라 장치를 해제하고, 부모 클래스의 destroy_node를 호출하여 노드를 깨끗이 종료하도록 하여 자원 누수를 방지한 점이 좋습니다.
메인 함수:

rclpy.spin으로 노드를 실행하며, 키보드 인터럽트로 종료되면 camera_publisher.destroy_node()와 rclpy.shutdown()이 호출되어 프로그램이 안전하게 종료되도록 처리되었습니다.
'''