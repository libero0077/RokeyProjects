import requests
import cv2
from io import BytesIO
import uuid
from datetime import datetime
import json
from requests.auth import HTTPBasicAuth

from db_manager import insert_data
from validator import DefectDetector

class ObjectDetectionInference():
    def __init__(self):
        self.api_url = "_______________" # put your url
        self.params = {"min_confidence": 0.0, "base_model": "YOLOv6-L"}
        self.class_map = {
            1: "BOOTSEL", 2: "CHIPSET", 3: "HOLE",
            4: "OSCILLATOR", 5: "RASPBERRY PICO", 6: "USB"
        }
        self.color_map = {
            'RASPBERRY PICO': (0, 255, 0),
            'USB': (150, 0, 0),
            'HOLE': (0, 0, 255),
            'OSCILLATOR': (255, 255, 0),
            'CHIPSET': (0, 255, 255),
            'BOOTSEL': (255, 165, 0)
        }

    def run_inference(self, img, endpoint):
        """Send image to API and return results with annotated image"""
        _, img_encoded = cv2.imencode(".jpg", img)
        img_bytes = BytesIO(img_encoded.tobytes())
        files = {"file": ("image.jpg", img_bytes, "image/jpeg")}
        uuid_value = str(uuid.uuid4())  # Unique identifier for each detection event

        try:
            if endpoint:
                response = requests.post(
                    url="__________________", # put your endpoint
                    auth=HTTPBasicAuth("", ''), # put your auth
                    headers={"Content-Type": "image/jpeg"},
                    data=img_encoded.tobytes()
                )
            else:
                response = requests.post(self.api_url, files=files, params=self.params)
            if response.status_code != 200:
                print(f"Failed to send image. Status code: {response.status_code}")
                return None, img, "Failed inference"
            try:
                res = response.json()
                objects = res.get("objects", [])
            except ValueError:
                print("Error parsing JSON response")
                return None, img, "JSON parse error"
            if not objects:
                print("No objects detected in response")
                return None, img, "No objects detected"
            # Process and validate objects
            detector = DefectDetector(res)
            # filtered_objects = self.filter_objects(objects)
            # validation_result, defect_reason = self.validate_objects(filtered_objects)
            validation_result, defect_reason = detector.__main__()
            defect_reason = json.dumps(defect_reason)
            annotated_img, result_txt = self.annotate_image(img, objects, validation_result, endpoint)
            # Log the validation status
            validation_status = 0 if validation_result else 1
            datetime_value = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            insert_data(datetime_value, uuid_value, validation_status, defect_reason)

            return objects, annotated_img, result_txt
        except requests.exceptions.RequestException as e:
            print(f"Error sending request: {e}")
            return None, img, "Request failed"
        
    # def filter_objects(self, objects):
    #     """Filter objects based on class and confidence."""
    #     filtered_objects = []
    #     for class_id, class_name in self.class_map.items():
    #         class_objects = [obj for obj in objects if obj["class_number"] == class_id]
    #         if class_name == "HOLE":
    #             # Keep top 4 HOLE objects
    #             filtered_objects.extend(sorted(class_objects, key=lambda x: x["confidence"], reverse=True)[:4])
    #         elif class_objects:
    #             # Keep the object with the highest confidence for other classes
    #             filtered_objects.append(max(class_objects, key=lambda x: x["confidence"]))
    #     return filtered_objects
    
    # def validate_objects(self, objects):
    #     """Validate object detection results."""
    #     object_counts = {class_name: 0 for class_name in self.class_map.values()}
    #     defect_reasons = []
    #     for obj in objects:
    #         class_name = self.class_map.get(obj["class_number"], "Unknown")
    #         if class_name in object_counts:
    #             object_counts[class_name] += 1
    #     # Validation logic
    #     if object_counts["HOLE"] != 4:
    #         defect_reasons.append("HOLE")
    #     for class_name, count in object_counts.items():
    #         if class_name != "HOLE" and count != 1:
    #             defect_reasons.append(class_name)
    #     if defect_reasons:
    #         return False, ", ".join(defect_reasons)
    #     return True, "-"
    
    def annotate_image(self, img, objects, validation_result, endpoint):
        """Annotate image with bounding boxes, labels, and validation result."""
        if endpoint:
            for obj in objects:
                print(objects)
                points = obj["box"]
                start_point = (int(points[0]), int(points[1]))
                end_point = (int(points[2]), int(points[3]))
                class_name = obj["class"]
                if class_name == "DHOLE":
                    class_name = "HOLE"
                color = self.color_map.get(class_name, (255, 255, 255))
                thickness = 1
                # Draw bounding box
                cv2.rectangle(img, start_point, end_point, color, thickness)
                # Draw label text
                text = f"{class_name} ({obj['score']:.2f})"
                position = (start_point[0], start_point[1] - 10)
                cv2.putText(img, text, position, cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, thickness, cv2.LINE_AA)
            # Add overall validation result
            result_text = "good" if validation_result else "bad"
            prediction_color = (0, 255, 0) if validation_result else (0, 0, 255)
            cv2.putText(img, f"Prediction: {result_text}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, prediction_color, 2)
            return img, result_text
        else:
            for obj in objects:
                points = obj["bbox"]
                start_point = (int(points[0]), int(points[1]))
                end_point = (int(points[2]), int(points[3]))
                class_name = self.class_map.get(obj["class_number"], "Unknown")
                color = self.color_map.get(class_name, (255, 255, 255))
                thickness = 1
                # Draw bounding box
                cv2.rectangle(img, start_point, end_point, color, thickness)
                # Draw label text
                text = f"{class_name} ({obj['confidence']:.2f})"
                position = (start_point[0], start_point[1] - 10)
                cv2.putText(img, text, position, cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, thickness, cv2.LINE_AA)
            # Add overall validation result
            result_text = "good" if validation_result else "bad"
            prediction_color = (0, 255, 0) if validation_result else (0, 0, 255)
            cv2.putText(img, f"Prediction: {result_text}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, prediction_color, 2)
            return img, result_text
    
    def process_image(self, img, endpoint=False):
        """Process the captured image, perform inference and validation."""
        # Run inference on the captured image
        objects, annotated_img, result_txt = self.run_inference(img, endpoint)

        if objects is None:
            print(f"Inference failed: {result_txt}")
            return img  # If inference fails, return the original image.

        print("Validation Result:", result_txt)
        # Annotate the image with the results
        cv2.imshow("Annotated Image", annotated_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        return annotated_img