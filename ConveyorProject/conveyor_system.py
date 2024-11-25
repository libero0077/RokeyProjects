import time
import serial
import cv2

from defect_detection import ObjectDetectionInference
from db_manager import create_db  # Import the create_db function

# Initialize serial connection and inference handler
ser = serial.Serial(___________) # put your serial here. ex)"/dev/ttyACM0", 9600
inference_handler = ObjectDetectionInference()

# Initialize the database
create_db()  # Ensure the database and tables are created before using them

def find_camera_indexes(max_index=10):
    available_indexes = []
    for i in range(max_index):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            available_indexes.append(i)
            cap.release()
    return available_indexes

def capture_image(camera_index):
    """Capture image from the camera."""
    cam = cv2.VideoCapture(camera_index)
    if not cam.isOpened():
        print("Camera Error")
        return None
    ret, img = cam.read()
    cam.release()
    return img

while True:
    # Read data from serial port
    data = ser.read()
    if data == b"0":
        print("Object detected! Capturing image...")
        start_time = time.time()
        # Capture image from the camera
        available_indexes = find_camera_indexes()
        img = capture_image(available_indexes[0])
        if img is None:
            print("Image capture failed. Skipping...")
            continue
        
        # Process the image and log the result
        status = inference_handler.process_image(img, endpoint=True)
        print(f"Detection Status: {status}")

        # Send signal back via serial
        ser.write(b"1")
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(start_time, end_time, elapsed_time)
        time.sleep(1)
    else:
        time.sleep(0.1)
