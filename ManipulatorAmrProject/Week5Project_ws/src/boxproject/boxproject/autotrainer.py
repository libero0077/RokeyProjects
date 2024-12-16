import os
import shutil
import random
import yaml
from ultralytics import YOLO

BASE_DIR = "/home/rokey11/autotrain"
IMAGES_DIR = os.path.join(BASE_DIR, "images")
LABELS_DIR = os.path.join(BASE_DIR, "labels")  # classes.txt 여기 있다고 가정
DATASET_DIR = os.path.join(BASE_DIR, "dataset")

TRAIN_DIR = os.path.join(DATASET_DIR, "train")
VALID_DIR = os.path.join(DATASET_DIR, "valid")
TEST_DIR = os.path.join(DATASET_DIR, "test")

BEST_WEIGHTS = os.path.join(BASE_DIR, "best.pt")

# 비율 설정
TRAIN_RATIO = 0.7
VALID_RATIO = 0.2
TEST_RATIO = 0.1

def read_classes(classes_file):
    # classes.txt 파일에서 클래스 이름 리스트 추출
    with open(classes_file, 'r') as f:
        classes = [line.strip() for line in f if line.strip()]
    return classes

def setup_directories():
    # dataset 디렉토리 초기화
    if os.path.exists(DATASET_DIR):
        shutil.rmtree(DATASET_DIR)
    os.makedirs(os.path.join(TRAIN_DIR, "images"), exist_ok=True)
    os.makedirs(os.path.join(TRAIN_DIR, "labels"), exist_ok=True)
    os.makedirs(os.path.join(VALID_DIR, "images"), exist_ok=True)
    os.makedirs(os.path.join(VALID_DIR, "labels"), exist_ok=True)
    os.makedirs(os.path.join(TEST_DIR, "images"), exist_ok=True)
    os.makedirs(os.path.join(TEST_DIR, "labels"), exist_ok=True)

def auto_label_with_model():
    # best.pt 모델을 이용해 raw image에 대한 라벨링 수행
    if not os.path.exists(BEST_WEIGHTS):
        print("No existing best.pt found. Cannot auto-label without a trained model.")
        return

    model = YOLO(BEST_WEIGHTS)
    # YOLOv8 predict: save_txt=True 시 각 이미지에 대한 라벨 txt 생성
    results = model.predict(source=IMAGES_DIR, save=True, save_txt=True)
    # 결과물: runs/detect/predict/ 디렉토리에 이미지와 labels 폴더가 생성됨
    # labels 폴더 내 .txt 파일이 YOLO 포맷의 라벨

    # 생성된 라벨 및 이미지를 DATASET_DIR로 이동
    pred_dir = os.path.join(DATASET_DIR, "runs", "detect", "predict")
    predicted_images_dir = pred_dir  # predict 폴더에 이미지와 labels 폴더가 함께 존재
    predicted_labels_dir = os.path.join(pred_dir, "labels")

    return predicted_images_dir, predicted_labels_dir

def move_predicted_data_to_dataset(predicted_images_dir, predicted_labels_dir):
    # predicted_images_dir, predicted_labels_dir에서 이미지 및 라벨 가져와서
    # dataset 디렉토리에 복사하기
    images = [f for f in os.listdir(predicted_images_dir) if os.path.isfile(os.path.join(predicted_images_dir, f)) and not f.endswith('.txt')]
    # 라벨은 predicted_labels_dir 안에 존재
    # 이미지명에 해당하는 라벨명: 이미지명과 동일한 파일명(확장자만 .txt)

    for img_file in images:
        img_src = os.path.join(predicted_images_dir, img_file)
        # txt 파일명
        txt_file = os.path.splitext(img_file)[0] + ".txt"
        txt_src = os.path.join(predicted_labels_dir, txt_file)

        # 복사할 위치: 일단 train으로 몰아넣고 나중에 split
        shutil.copy(img_src, os.path.join(TRAIN_DIR, "images", img_file))
        if os.path.exists(txt_src):
            shutil.copy(txt_src, os.path.join(TRAIN_DIR, "labels", txt_file))

def split_data():
    # train/images 디렉토리에 있는 파일 기준으로 split
    train_images = [f for f in os.listdir(os.path.join(TRAIN_DIR, "images")) if os.path.isfile(os.path.join(TRAIN_DIR, "images", f))]

    random.shuffle(train_images)
    total_files = len(train_images)
    train_end = int(total_files * TRAIN_RATIO)
    valid_end = train_end + int(total_files * VALID_RATIO)

    # train_images 리스트를 train/valid/test로 분배
    actual_train = train_images[:train_end]
    actual_valid = train_images[train_end:valid_end]
    actual_test = train_images[valid_end:]

    def move_files(file_list, src_image_dir, src_label_dir, dst_image_dir, dst_label_dir):
        for f in file_list:
            shutil.move(os.path.join(src_image_dir, f), os.path.join(dst_image_dir, f))
            txt_file = os.path.splitext(f)[0] + ".txt"
            txt_src_path = os.path.join(src_label_dir, txt_file)
            if os.path.exists(txt_src_path):
                shutil.move(txt_src_path, os.path.join(dst_label_dir, txt_file))

    # 기존 TRAIN_DIR 내에 이미 모든 파일이 있으므로 이동만 하면 됨.
    move_files(actual_valid,
               os.path.join(TRAIN_DIR, "images"),
               os.path.join(TRAIN_DIR, "labels"),
               os.path.join(VALID_DIR, "images"),
               os.path.join(VALID_DIR, "labels"))

    move_files(actual_test,
               os.path.join(TRAIN_DIR, "images"),
               os.path.join(TRAIN_DIR, "labels"),
               os.path.join(TEST_DIR, "images"),
               os.path.join(TEST_DIR, "labels"))

    # TRAIN_DIR에는 actual_train만 남는다.

def create_data_yaml(classes):
    data = {
        'train': os.path.join(TRAIN_DIR, 'images'),
        'val': os.path.join(VALID_DIR, 'images'),
        'test': os.path.join(TEST_DIR, 'images'),
        'nc': len(classes),
        'names': classes
    }
    with open(os.path.join(DATASET_DIR, 'custom_data.yaml'), 'w') as f:
        yaml.dump(data, f)

def train_model():
    # best.pt 기반 파인튜닝 또는 yolov8n.pt 시작
    if os.path.exists(BEST_WEIGHTS):
        model = YOLO(BEST_WEIGHTS)
    else:
        model = YOLO('yolov8n.pt')

    data_yaml = os.path.join(DATASET_DIR, 'custom_data.yaml')
    model.train(data=data_yaml, epochs=50, patience=10, batch=16, imgsz=640)

    # 학습 완료 후 best.pt 갱신
    run_dir = os.path.join(DATASET_DIR, "runs", "detect", "train", "weights")
    best_pt_src = os.path.join(run_dir, "best.pt")
    if os.path.exists(best_pt_src):
        shutil.copy(best_pt_src, BEST_WEIGHTS)

def cleanup():
    # train, valid, test 디렉토리 정리
    for d in [TRAIN_DIR, VALID_DIR, TEST_DIR]:
        if os.path.exists(d):
            shutil.rmtree(d)
    # runs 디렉토리도 정리
    runs_dir = os.path.join(DATASET_DIR, "runs")
    if os.path.exists(runs_dir):
        shutil.rmtree(runs_dir)


if __name__ == "__main__":
    # classes.txt로부터 클래스 정보 읽기
    classes_file = os.path.join(LABELS_DIR, "classes.txt")
    if not os.path.exists(classes_file):
        raise FileNotFoundError("classes.txt not found. Please provide a classes.txt in the labels directory.")

    classes = read_classes(classes_file)

    setup_directories()

    # best.pt가 있을 경우 raw images에 대해 추론하여 라벨 생성
    # 없으면 기존 로직대로 진행 (raw images만으로는 라벨 자동생성이 불가하므로 의미는 떨어짐)
    if os.path.exists(BEST_WEIGHTS):
        predicted_images_dir, predicted_labels_dir = auto_label_with_model()
        move_predicted_data_to_dataset(predicted_images_dir, predicted_labels_dir)
    else:
        # best.pt가 없는 경우, 가정: images와 labels 모두 있는 경우만 정상 학습 가능
        # 여기서는 raw image만 있다는 전제에서 best.pt가 없으면 의미 없음.
        # 필요하다면 여기서 기존의 labels 디렉토리 기반으로 copy해서 split 할 수도 있음.
        # 그 경우 아래 로직 추가 가능:
        # (사용자 요구사항에 "원래" 라벨이 있는지 명확치 않으므로 여기는 생략)
        pass

    # train/valid/test 스플릿
    split_data()

    # custom_data.yaml 작성
    create_data_yaml(classes)

    # 학습 진행
    train_model()

    # 정리
    cleanup()
