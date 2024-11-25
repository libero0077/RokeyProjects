import os
import requests
import cv2
from sklearn.metrics import confusion_matrix, classification_report
class ObjectDetectionInference:
    def __init__(self, good_dir, bad_dir, result_dir, model_params):
        self.good_dir = good_dir
        self.bad_dir = bad_dir
        self.result_dir = result_dir
        self.model_params = model_params
        self.class_map = {
            1: "BOOTSEL",
            2: "CHIPSET",
            3: "HOLE",
            4: "OSCILLATOR",
            5: "RASPBERRY PICO",
            6: "USB"
        }
        self.color_map = {
            'RASPBERRY PICO': (0, 255, 0),
            'USB': (255, 0, 0),
            'HOLE': (0, 0, 255),
            'OSCILLATOR': (255, 255, 0),
            'CHIPSET': (0, 255, 255),
            'BOOTSEL': (255, 165, 0)
        }
        self.true_labels = []
        self.predicted_labels = []
        self.image_files = self._get_image_files()
        # Create result directory if it does not exist
        if not os.path.exists(self.result_dir):
            os.makedirs(self.result_dir)
    def _get_image_files(self):
        good_files = [
            os.path.join(self.good_dir, f) for f in os.listdir(self.good_dir) if f.lower().endswith('.jpg')
        ]
        bad_files = [
            os.path.join(self.bad_dir, f) for f in os.listdir(self.bad_dir) if f.lower().endswith('.jpg')
        ]
        self.true_labels = ["good"] * len(good_files) + ["bad"] * len(bad_files)
        return good_files + bad_files
    def _process_inference(self, file):
        with open(file, "rb") as images:
            image = {'file': ('image.jpg', images, 'image/jpeg')}
            response = requests.post(
                url="", # put your url
                params=self.model_params,
                files=image,
            )
        return response.json()
    def _validate_prediction(self, object_counts):
        # Check if the 'HOLE' count is 4 and others are 1
        return object_counts['HOLE'] == 4 and all(
            object_counts[key] == 1 for key in self.class_map.values() if key != 'HOLE'
        )
    def _draw_bounding_boxes(self, img, objects):
        for obj in objects:
            points = obj["bbox"]
            start_point = (int(points[0]), int(points[1]))
            end_point = (int(points[2]), int(points[3]))
            class_name = self.class_map.get(obj["class_number"], "Unknown")
            color = self.color_map.get(class_name, (255, 255, 255))
            thickness = 1
            # Draw bounding box
            cv2.rectangle(img, start_point, end_point, color, thickness)
            # Add label with confidence score
            text = f"{class_name} ({obj['confidence']:.2f})"
            position = (start_point[0], start_point[1] - 10)
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.6
            cv2.putText(img, text, position, font, font_scale, color, thickness, cv2.LINE_AA)
        return img
    def _draw_object_counts(self, img, object_counts):
        y_offset = 30
        for obj_class, count in object_counts.items():
            text = f"{obj_class}: {count}"
            cv2.putText(img, text, (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, self.color_map[obj_class], 1, cv2.LINE_AA)
            y_offset += 30
        return img
    def _draw_prediction_text(self, img, result_text, y_offset):
        prediction_color = (0, 255, 0) if result_text == "good" else (0, 0, 255)
        cv2.putText(img, f"Prediction: {result_text}", (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 1, prediction_color, 2)
        return img
    def _save_result_image(self, img, file):
        result_file = os.path.join(self.result_dir, os.path.basename(file))
        cv2.imwrite(result_file, img)
    def run_inference(self):
        for i, file in enumerate(self.image_files):
            print(f"Processing {file}")
            res = self._process_inference(file)
            # Initialize object counts
            object_counts = {key: 0 for key in self.class_map.values()}
            for obj in res["objects"]:
                class_name = self.class_map.get(obj["class_number"], "Unknown")
                if class_name in object_counts:
                    object_counts[class_name] += 1
            # Validation: check if the object count is valid
            result_text = "good" if self._validate_prediction(object_counts) else "bad"
            self.predicted_labels.append(result_text)
            # Read image and process bounding boxes and counts
            img = cv2.imread(file)
            img = self._draw_bounding_boxes(img, res["objects"])
            img = self._draw_object_counts(img, object_counts)
            img = self._draw_prediction_text(img, result_text, 30)
            # Save the result image
            self._save_result_image(img, file)
    def filter_objects(self, objects):
        """Filter objects based on class and confidence."""
        filtered_objects = []
        for class_id, class_name in self.class_map.items():
            class_objects = [obj for obj in objects if obj["class_number"] == class_id]
            if class_name == "HOLE":
                # Keep top 4 HOLE objects
                filtered_objects.extend(sorted(class_objects, key=lambda x: x["confidence"], reverse=True)[:4])
            elif class_objects:
                # Keep the object with the highest confidence for other classes
                filtered_objects.append(max(class_objects, key=lambda x: x["confidence"]))
        return filtered_objects
    def evaluate(self):
        cm = confusion_matrix(self.true_labels, self.predicted_labels, labels=["good", "bad"])
        print("Confusion Matrix:")
        print(cm)
        report = classification_report(self.true_labels, self.predicted_labels, target_names=["good", "bad"])
        print("\nClassification Report:")
        print(report)
if __name__ == "__main__":
    # Directories and model parameters
    good_dir = "/good"
    bad_dir = "/bad"
    result_dir = "/result"
    model_params = {
        "min_confidence": 0.0,
        "base_model": "YOLOv6-L"
    }
    # Initialize and run inference
    inference = ObjectDetectionInference(good_dir, bad_dir, result_dir, model_params)
    inference.run_inference()
    # Evaluate the results
    inference.evaluate()