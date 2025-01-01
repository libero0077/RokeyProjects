import cv2
import numpy as np

class VisualTrackingWebcam:
    def __init__(self):
        # ----------------------------- ORB 설정 -----------------------------
        # ORB를 사용해 특징점을 검출하고 디스크립터를 생성.
        self.detector = cv2.ORB_create(nfeatures=500)

        # ----------------------------- 매처 설정 -----------------------------
        # 매처를 BF (브루트포스)로 가정 (원하는 경우 FLANN으로 변경 가능)
        self.matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)

        # ----------------------------- 이전 프레임 저장용 -----------------------------
        self.prev_keypoints = None
        self.prev_descriptors = None

        # ----------------------------- 시각화용 설정 -----------------------------
        self.display_width = 640
        self.display_height = 480
        self.window_name = 'Visual Tracking - ORB (Webcam)'
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.window_name, self.display_width, self.display_height)

        # ----------------------------- 잔상(페이드) 효과를 위한 오버레이 -----------------------------
        self.overlay = np.zeros((self.display_height, self.display_width, 3), dtype=np.uint8)

        # ----------------------------- 잔상(페이드) 파라미터 -----------------------------
        self.fade_factor = 0.9     
        self.overlay_alpha = 0.7  

    def run(self):
        # 웹캠 열기 (0번: 기본 카메라)
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("웹캠(카메라)을 열 수 없습니다.")
            return

        while True:
            ret, frame = cap.read()
            if not ret:
                print("프레임을 읽어올 수 없습니다.")
                break

            # 1) 화면 크기 맞추기
            resized_color = cv2.resize(frame, (self.display_width, self.display_height))

            # 2) 그레이스케일 변환
            gray_image = cv2.cvtColor(resized_color, cv2.COLOR_BGR2GRAY)

            # 3) ORB로 특징점 검출 및 디스크립터 생성
            keypoints, descriptors = self.detector.detectAndCompute(gray_image, None)

            # 4) 오버레이 페이드
            self.overlay = (self.overlay * self.fade_factor).astype(np.uint8)

            # 5) 매칭 수행
            if self.prev_descriptors is not None and descriptors is not None:
                # knnMatch로 매칭
                raw_matches = self.matcher.knnMatch(self.prev_descriptors, descriptors, k=2)

                good_matches = []
                for match_pair in raw_matches:
                    if len(match_pair) < 2:
                        continue
                    m, n = match_pair
                    if m.distance < 0.75 * n.distance:
                        good_matches.append(m)

                # 상위 N개 매칭만
                N_MATCHES = 30
                good_matches = sorted(good_matches, key=lambda x: x.distance)[:N_MATCHES]

                # 이전 프레임 키포인트 좌표, 현재 프레임 키포인트 좌표 추출
                prev_pts = np.float32([self.prev_keypoints[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
                curr_pts = np.float32([keypoints[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

                # 매칭선 그리기
                for p0, p1 in zip(prev_pts, curr_pts):
                    pt0 = tuple(map(int, p0.ravel()))
                    pt1 = tuple(map(int, p1.ravel()))
                    cv2.line(self.overlay, pt0, pt1, (0, 0, 255), 2)

            # 현재 프레임을 다음 비교용으로 저장
            self.prev_keypoints = keypoints
            self.prev_descriptors = descriptors

            # 6) 오버레이 합성
            result = cv2.addWeighted(resized_color, 1.0, self.overlay, self.overlay_alpha, 0)

            # 키포인트 시각화 (녹색 원)
            for kp in keypoints:
                x, y = map(int, kp.pt)
                cv2.circle(result, (x, y), 3, (0, 255, 0), -1)

            cv2.imshow(self.window_name, result)

            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC 키 누르면 종료
                break

        cap.release()
        cv2.destroyAllWindows()

def main():
    visual_tracking = VisualTrackingWebcam()
    visual_tracking.run()

if __name__ == '__main__':
    main()
