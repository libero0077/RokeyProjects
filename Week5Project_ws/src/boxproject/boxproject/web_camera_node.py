import rclpy  # ROS2 클라이언트 라이브러리
from rclpy.node import Node  # ROS2 노드 베이스 클래스
from sensor_msgs.msg import Image  # ROS2 Image 메시지 타입
from cv_bridge import CvBridge  # OpenCV와 ROS2 메시지 변환을 위한 브리지
import cv2  # OpenCV 라이브러리

class WebcamNode(Node):
    def __init__(self):
        super().__init__('webcam_node')  # 노드 이름 설정

        self.cap = cv2.VideoCapture(2)  
        if not self.cap.isOpened():  # 카메라가 열리지 않으면 오류 메시지 출력
            self.get_logger().error("Webcam could not be opened")
            return

        self.publisher = self.create_publisher(Image, 'webcam/image_raw', 10) # 'webcam/image_raw' 토픽으로 퍼블리시
        self.bridge = CvBridge() # OpenCV와 ROS 메시지 변환을 위한 브리지 객체 생성
        self.timer = self.create_timer(0.1, self.publish_frame) # 0.1초마다 publish_frame 함수를 호출 (10 FPS)

    def publish_frame(self):
        # 웹캠으로부터 프레임 캡처
        ret, frame = self.cap.read()
        if not ret:  # 프레임 캡처 실패 시 에러 로그 출력
            self.get_logger().error("Failed to capture frame from webcam")
            return

        img_msg = self.bridge.cv2_to_imgmsg(frame, encoding="bgr8") # OpenCV 이미지를 ROS2 Image 메시지로 변환
        self.publisher.publish(img_msg) # 변환된 메시지를 'webcam/image_raw' 토픽으로 퍼블리시

    def destroy_node(self): # 노드 종료 시 카메라 리소스 해제
        self.cap.release()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)

    # WebcamNode 생성
    webcam_node = WebcamNode()

    try:
        # ROS2 노드 실행 (스핀)
        rclpy.spin(webcam_node)
    except KeyboardInterrupt:
        # 종료 시 사용자에게 알림
        webcam_node.get_logger().info('Shutting down webcam node...')
    finally:
        # 노드 종료 및 ROS2 종료
        webcam_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
