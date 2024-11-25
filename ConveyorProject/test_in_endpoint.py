import os
import requests
from requests.auth import HTTPBasicAuth
import cv2
import numpy as np
from sklearn.metrics import confusion_matrix, classification_report
# 디렉토리 설정
good_dir = "/good"  # 양품 이미지 경로
# good_dir = "/home/rokey/rokey/1124_New_train_image"
bad_dir = "/bad"    # 불량 이미지 경로
# bad_dir = "/home/rokey/rokey/1124_New_bad_Test_images"
result_dir = "/result"  # 결과 저장 디렉토리
ACCESS_KEY = ''

# 디렉토리 생성 (결과 저장을 위한 폴더)
if not os.path.exists(result_dir):
    os.makedirs(result_dir)
# 이미지 파일 경로 리스트
good_files = [
    os.path.join(good_dir, f) for f in os.listdir(good_dir) if f.lower().endswith('.jpg')
]
bad_files = [
    os.path.join(bad_dir, f) for f in os.listdir(bad_dir) if f.lower().endswith('.jpg')
]
# 데이터 합치기
image_files = good_files + bad_files
true_labels = ["good"] * len(good_files) + ["bad"] * len(bad_files)
# 색상 매핑
color_map = {
    'RASPBERRY PICO': (0, 255, 0),
    'USB': (255, 0, 0),
    'DHOLE': (0, 0, 255),
    'OSCILLATOR': (255, 255, 0),
    'CHIPSET': (0, 255, 255),
    'BOOTSEL': (255, 165, 0)
}
# API 요청 및 결과 처리
predicted_labels = []
for i, file in enumerate(image_files):
    print(file)
    with open(file, "rb") as image:
        response = requests.post(
            url="", # put your endpoint here
            auth=HTTPBasicAuth("", ACCESS_KEY),
            headers={"Content-Type": "image/jpeg"},
            data=image.read(),
        )
    res = response.json()
    print(res)
    # 객체 개수 카운트
    object_counts = {key: 0 for key in color_map.keys()}
    for obj in res["objects"]:
        if obj["class"] in object_counts:
            object_counts[obj["class"]] += 1
    # 검증 조건: HOLE 4개, 나머지 1개씩
    is_valid = object_counts['DHOLE'] == 4 and all(
        object_counts[key] == 1 for key in color_map.keys() if key != 'DHOLE'
    )
    result_text = "good" if is_valid else "bad"
    predicted_labels.append(result_text)
    # 이미지에 박스와 텍스트 그리기
    img = cv2.imread(file)
    for obj in res["objects"]:
        start_point = obj["box"][0:2]
        end_point = obj["box"][2:]
        color = color_map.get(obj["class"], (255, 255, 255))
        thickness = 1
        # 객체를 그리기
        cv2.rectangle(img, tuple(start_point), tuple(end_point), color, thickness)
        text = f"{obj['class']} ({obj['score']:.2f})"
        position = (start_point[0], start_point[1] - 10)
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.6
        cv2.putText(img, text, position, font, font_scale, color, thickness, cv2.LINE_AA)
    # 객체 개수 표시
    y_offset = 30
    for obj_class, count in object_counts.items():
        text = f"{obj_class}: {count}"
        cv2.putText(img, text, (10, y_offset), font, font_scale, color_map[obj_class], thickness, cv2.LINE_AA)
        y_offset += 30
    # 예측 결과 텍스트 추가 (good은 초록색, bad는 빨간색)
    prediction_color = (0, 255, 0) if result_text == "good" else (0, 0, 255)
    cv2.putText(img, f"Prediction: {result_text}", (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 1, prediction_color, 2)
    # 결과 이미지 저장
    result_file = os.path.join(result_dir, os.path.basename(file))
    cv2.imwrite(result_file, img)
# Confusion Matrix 계산
cm = confusion_matrix(true_labels, predicted_labels, labels=["good", "bad"])
# Confusion Matrix 결과 출력
print("Confusion Matrix:")
print(cm)
# 정밀도, 재현율, F1 점수 계산 및 출력
report = classification_report(true_labels, predicted_labels, target_names=["good", "bad"])
print("\nClassification Report:")
print(report)