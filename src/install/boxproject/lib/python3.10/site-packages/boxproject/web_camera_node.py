import cv2
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from std_msgs.msg import String

class CameraNode(Node):
    def __init__(self):
        super().__init__('camera_node')

        # ROS2 퍼블리셔
        self.webcam_publisher = self.create_publisher(Image, 'webcam/image_raw', 10)
        self.log_publisher = self.create_publisher(String, 'log_mesg', 10)

        # OpenCV - ROS 메시지 변환 브리지
        self.bridge = CvBridge()

        # 카메라 초기화
        self.camera = None
        self.camera_index = None
        self.camera_connected = False
        self.find_and_connect_camera()

        # 타이머 설정
        self.timer_period = 0.1  # 0.1초마다 프레임 퍼블리시
        self.timer = self.create_timer(self.timer_period, self.publish_frame)

        # 카메라 상태 확인 타이머
        self.check_camera_timer = self.create_timer(3.0, self.check_camera_status)  # 3초마다 연결 확인

    def find_and_connect_camera(self):
        """사용 가능한 카메라를 찾아 연결"""
        self.get_logger().info("Searching for available cameras...")
        for index in range(10):  # 최대 10개의 카메라 시도
            cap = cv2.VideoCapture(index)
            if cap.isOpened():
                cap.release()
                self.camera_index = index
                self.camera = cv2.VideoCapture(self.camera_index)
                if self.camera.isOpened():
                    self.camera_connected = True
                    self.get_logger().info(f"카메라 연결됨 /dev/video{self.camera_index}")
                    self.publish_log_message(f"카메라 연결됨 /dev/video{self.camera_index}")
                    return True
        self.camera_connected = False
        self.get_logger().warning("No available cameras found.")
        return False

    def check_camera_status(self):
        """카메라 상태 확인 및 재연결 시도"""
        if self.camera and self.camera.isOpened():
            # 카메라 연결 상태를 확인하려면 실제 프레임 읽기를 시도
            ret, _ = self.camera.read()
            if not ret:  # 프레임 읽기 실패
                self.camera.release()
                self.camera_connected = False
                self.get_logger().warning("프레임을 읽는 동안 카메라 연결이 끊어졌습니다. 다시 연결하는 중...")
                self.publish_log_message("카메라 연결이 끊어졌습니다. 다시 연결을 시도하는 중...")
                self.find_and_connect_camera()
        else:
            if self.camera_connected:  # 이전에 연결되었지만 현재는 끊긴 상태
                self.camera.release()
                self.camera_connected = False
                self.get_logger().warning("카메라 연결이 끊어졌습니다. 다시 연결을 시도하는 중...")
                self.publish_log_message("카메라 연결이 끊어졌습니다. 다시 연결을 시도하는 중...")
            self.find_and_connect_camera()

    def publish_frame(self):
        """현재 프레임을 퍼블리시"""
        if not (self.camera and self.camera.isOpened()):
            return  # 카메라가 없으면 퍼블리시하지 않음

        ret, frame = self.camera.read()
        if not ret:
            self.get_logger().warning("카메라의 프레임을 읽지 못 했습니다.")
            #self.publish_log_message("카메라의 프레임을 읽지 못 했습니다.")
            return

        # 프레임 퍼블리시
        try:
            msg = self.bridge.cv2_to_imgmsg(frame, encoding='bgr8')
            self.webcam_publisher.publish(msg)
        except Exception as e:
            self.get_logger().error(f"Error publishing frame: {e}")

    def publish_log_message(self, message):
        """Log 메시지 퍼블리시"""
        msg = String()
        msg.data = message
        self.log_publisher.publish(msg)
        self.get_logger().info(f"Published log message: {message}")


def main(args=None):
    rclpy.init(args=args)
    camera_node = CameraNode()

    try:
        rclpy.spin(camera_node)
    except KeyboardInterrupt:
        pass
    finally:
        # 리소스 정리
        if camera_node.camera:
            camera_node.camera.release()
        camera_node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
