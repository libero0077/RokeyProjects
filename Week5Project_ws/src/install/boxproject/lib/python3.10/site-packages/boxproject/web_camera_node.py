import rclpy  # ROS2 클라이언트 라이브러리
from rclpy.node import Node  # ROS2 노드 베이스 클래스
from sensor_msgs.msg import Image  # ROS2 Image 메시지 타입
from cv_bridge import CvBridge  # OpenCV와 ROS2 메시지 변환을 위한 브리지
import cv2  # OpenCV 라이브러리
from std_msgs.msg import String  # 상태 메시지를 위한 임포트 추가

class WebcamNode(Node):
    def __init__(self):
        super().__init__('webcam_node')  # 노드 이름 설정

        self.cap = cv2.VideoCapture(2)  
        if not self.cap.isOpened():  # 카메라가 열리지 않으면 오류 메시지 출력
            self.get_logger().error("Webcam could not be opened")
            self.publish_status("카메라 연결 끊김")  # 상태 메시지 즉시 퍼블리시
            return
        
        '''######### 720p 해상도로 설정
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        ############################################'''

        self.publisher = self.create_publisher(Image, 'webcam/image_raw', 10) # 'webcam/image_raw' 토픽으로 퍼블리시

        #################### 카메라 연결 끊김에 대한 내용을 퍼블리시 하기 위해 추가###########################
        self.status_publisher = self.create_publisher(String, 'robot_status', 10)  # 상태 퍼블리셔 추가
        self.camera_connected = True  # 카메라 연결 상태를 추적
        ############################################################################################
        
        self.bridge = CvBridge() # OpenCV와 ROS 메시지 변환을 위한 브리지 객체 생성
        self.timer = self.create_timer(0.1, self.publish_frame) # 0.1초마다 publish_frame 함수를 호출 (10 FPS)

    def publish_frame(self):
        # 웹캠으로부터 프레임 캡처
        ret, frame = self.cap.read()
        if not ret:  # 프레임 캡처 실패 시 에러 로그 출력
            self.get_logger().error("Failed to capture frame from webcam")
            ################### 카메라 연결이 끊겼을 때 로직 추가 #############
            self.publish_status("카메라 연결 끊김")
            self.camera_connected = False  # 연결 상태를 끊김으로 설정
            ############################################################
            return
        
        # 연결이 복구된 경우 상태를 업데이트
        if not self.camera_connected:
            self.publish_status("카메라 연결 복구")
            self.camera_connected = True

        img_msg = self.bridge.cv2_to_imgmsg(frame, encoding="bgr8") # OpenCV 이미지를 ROS2 Image 메시지로 변환
        self.publisher.publish(img_msg) # 변환된 메시지를 'webcam/image_raw' 토픽으로 퍼블리시

    def destroy_node(self): # 노드 종료 시 카메라 리소스 해제
        self.cap.release()
        super().destroy_node()

    ################ 카메라 연결 끊김시 퍼블리시 하기 위한 로직 ####################
    def publish_status(self, status_message):
        msg = String()
        msg.data = status_message
        self.status_publisher.publish(msg)
        self.get_logger().info(f"Published status: {status_message}")
    ##########################################################################

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
