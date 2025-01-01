import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np
from sensor_msgs.msg import CompressedImage 

class VisualTrackingNode(Node):
    def __init__(self):
        super().__init__('visual_tracking_node')

        # ----------------------------- 파라미터 설정 -----------------------------
        # ros2 run visual_tracking visual_tracking_node --ros-args -p matcher_type:=FLANN
        # 위와 같이 실행 시 matcher_type을 "FLANN"으로 지정할 수 있음.
        
        # ros2 run visual_tracking visual_tracking_node --ros-args -p matcher_type:=BF
        # 위와 같이 실행 시 matcher_type을 "BF"로 지정할 수 있음.
        
        # 현재 기본값을 BF로 설정 (Brute-Force)
        self.declare_parameter('matcher_type', 'BF')
        self.matcher_type = self.get_parameter('matcher_type').get_parameter_value().string_value

        self.get_logger().info(f'사용할 매처 타입: {self.matcher_type}')

        # ----------------------------- 이미지 구독 설정 -----------------------------
        # 토픽 "/oakd/rgb/preview/image_raw"에서 영상(이미지) 데이터를 받아옴.
        self.subscription = self.create_subscription(
            CompressedImage,
            '/oakd/rgb/preview/image_raw/compressed',
            self.image_callback,
            10
        )

        # ----------------------------- CvBridge 초기화 -----------------------------
        # ROS 이미지 <-> OpenCV 이미지 변환에 사용.
        self.bridge = CvBridge()

        # ----------------------------- ORB 설정 -----------------------------
        # ORB를 사용해 특징점을 검출하고 디스크립터를 생성.
        # nfeatures=50 => 최대 50개의 특징점만 검출하겠다는 의미.
        # 숫자를 늘리면 더 많은 특징점을 찾지만, 계산량이 많아져 느려질 수 있음.
        self.detector = cv2.ORB_create(nfeatures=300)
        self.get_logger().info('ORB 생성 완료.')

        # ----------------------------- 매처 설정 -----------------------------
        # 매처를 BF 또는 FLANN 중 하나로 선택.
        # - BFMatcher(NORM_HAMMING): ORB같이 이진 디스크립터에 적합.
        # - FLANN: 근사 최근접 탐색으로 대규모 시에도 빠를 수 있음.
        if self.matcher_type.upper() == 'BF':
            self.matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
            self.get_logger().info('BFMatcher를 사용합니다.')
        else:
            # FLANN_INDEX_LSH = 6 => ORB(이진 디스크립터)용 설정
            index_params = dict(algorithm=6,  # FLANN_INDEX_LSH
                                table_number=6,  # 해시 테이블 개수 (기본 6)
                                key_size=12,     # 해시 키 크기 (기본 12)
                                multi_probe_level=1)  # 해시 테이블 재탐색(기본 1)
            search_params = dict(checks=50)    # 탐색 시 반복 검사 횟수
            self.matcher = cv2.FlannBasedMatcher(index_params, search_params)
            self.get_logger().info('FLANN Matcher를 사용합니다.')

        # ----------------------------- 이전 프레임 저장용 -----------------------------
        self.prev_keypoints = None
        self.prev_descriptors = None

        # ----------------------------- 시각화용 설정 -----------------------------
        # 화면 크기
        self.display_width = 640
        self.display_height = 480
        self.window_name = 'Visual Tracking - ORB'
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.window_name, self.display_width, self.display_height)

        # ----------------------------- 잔상(페이드) 효과를 위한 오버레이 -----------------------------
        # 매 프레임에서 그려질 "매칭선"을 유지/페이드시키는 이미지.
        self.overlay = np.zeros((self.display_height, self.display_width, 3), dtype=np.uint8)

        # ----------------------------- 잔상(페이드) 파라미터 -----------------------------
        # fade_factor: 높을수록 잔상이 더 오래 남음(1.0에 가까울수록 거의 안 사라짐).
        # overlay_alpha: result 합성 시 오버레이 투명도, 높을수록 라인이 진하게 보임.
        self.fade_factor = 0.9      
        self.overlay_alpha = 0.7    

    def image_callback(self, msg):
        try:
            # cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
            cv_image = self.bridge.compressed_imgmsg_to_cv2(msg, desired_encoding='bgr8')
        except Exception as e:
            self.get_logger().error(f'이미지 변환 실패: {e}')
            return

        # ------------- 1) 이미지 리사이즈 -------------
        # 계산량 감소와 화면 표시를 위해 640x480 크기로 축소
        try:
            resized_color = cv2.resize(cv_image, (self.display_width, self.display_height))
        except Exception as e:
            self.get_logger().error(f'이미지 리사이즈 실패: {e}')
            return

        # ------------- 2) 그레이스케일 변환 (디텍터 입력용) -------------
        gray_image = cv2.cvtColor(resized_color, cv2.COLOR_BGR2GRAY)

        # ------------- 3) ORB로 특징점 검출 및 디스크립터 생성 -------------
        keypoints, descriptors = self.detector.detectAndCompute(gray_image, None)

        # ------------- 4) 오버레이 페이드 (잔상 줄어들게) -------------
        # self.fade_factor만큼 오버레이 픽셀 값에 곱 => 점차 어둡게/투명하게
        self.overlay = (self.overlay * self.fade_factor).astype(np.uint8)

        # ------------- 5) 매칭 수행 -------------
        if self.prev_descriptors is not None and descriptors is not None:
            # knnMatch: 각 디스크립터마다 가장 가까운 2개를 찾음
            raw_matches = self.matcher.knnMatch(self.prev_descriptors, descriptors, k=2)

            # 비율 테스트로 좋지 않은 매칭 제거
            good_matches = []
            for match_pair in raw_matches:
                if len(match_pair) < 2:
                    continue  # 매칭이 두 개 미만인 경우 건너뜀
                m, n = match_pair
                if m.distance < 0.75 * n.distance:
                    good_matches.append(m)
            # 상위 N개의 매칭만 사용 (추가적 성능 최적화)00
            N_MATCHES = 80
            good_matches = sorted(good_matches, key=lambda x: x.distance)[:N_MATCHES]

            # 이전 프레임 키포인트 좌표, 현재 프레임 키포인트 좌표 추출
            prev_pts = np.float32([self.prev_keypoints[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
            curr_pts = np.float32([keypoints[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

            # 오버레이에 라인(매칭선) 그리기
            for p0, p1 in zip(prev_pts, curr_pts):
                pt0 = tuple(map(int, p0.ravel()))
                pt1 = tuple(map(int, p1.ravel()))
                # 빨간색 선으로 표시
                cv2.line(self.overlay, pt0, pt1, (0, 0, 255), 2)

        # 이번 프레임을 다음 프레임을 위한 prev_*에 저장
        self.prev_keypoints = keypoints
        self.prev_descriptors = descriptors

        # ------------- 6) 오버레이 합성 -------------
        # 합성: resized_color와 overlay를 addWeighted로 합성
        # overlay_alpha가 클수록 라인이 진하게 표시됨
        result = cv2.addWeighted(resized_color, 1.0, self.overlay, self.overlay_alpha, 0)

        # ------------- 키포인트 시각화 (녹색 원) -------------
        for kp in keypoints:
            x, y = map(int, kp.pt)
            cv2.circle(result, (x, y), 3, (0, 255, 0), -1)

        # 최종 결과 표시
        cv2.imshow(self.window_name, result)
        cv2.waitKey(1)

def main(args=None):
    rclpy.init(args=args)
    node = VisualTrackingNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Shutting down VisualTrackingNode.')
    finally:
        cv2.destroyAllWindows()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
