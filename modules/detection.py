from ultralytics import YOLO # type: ignore
from PIL import Image # type: ignore
import cv2 # type: ignore
import numpy as np # type: ignore
from settings import setting # type: ignore

class Detection:
    def __init__(self, model_path: str = setting.CCCD_12SO_FIELD_DETECTION_PATH, device:str = setting.DEVICE, task = "detect"):
        self.device = device
        self.task = task
        self.cccd_12_field_detection = YOLO(model_path)
        self.names = self.cccd_12_field_detection.names

    def detect(self, image: np.ndarray) -> list[dict]:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.cccd_12_field_detection(image, imgsz=640, device=self.device, verbose=False, conf=0.3)[0]
        
        # Danh sách các label có thể có nhiều dòng
        MULTI_LINE_LABELS = {"residence"}
        
        candidates = {}
        for box in results.boxes:
            cls_id = int(box.cls[0])
            label = self.names[cls_id]
            conf = float(box.conf[0])
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
            
            if label not in candidates:
                candidates[label] = []
            candidates[label].append({"box": (x1, y1, x2, y2), "conf": conf})

        final_results = []
        for label, items in candidates.items():
            if label in MULTI_LINE_LABELS:
                # Sắp xếp các dòng theo tọa độ y1 (dòng trên trước, dòng dưới sau)
                sorted_items = sorted(items, key=lambda x: x["box"][1])
                for idx, item in enumerate(sorted_items, start=1):
                    final_results.append({
                        "label": f"{label}_{idx}",  
                        "box": item["box"],
                        "conf": round(item["conf"], 2)
                    })
            else:
                # Các trường 1 dòng: chọn box có conf cao nhất
                best_item = max(items, key=lambda x: x["conf"])
                final_results.append({
                    "label": label,
                    "box": best_item["box"],
                    "conf": round(best_item["conf"], 2)
                })

        return final_results


if __name__ == "__main__":
    import matplotlib.pyplot as plt # type: ignore
    detector = Detection()
    image = cv2.imread("../img.jpg")
    # image = cv2.resize(image, (512, 512))
    results = detector.detect(image)
    for result in results:
        x1, y1, x2, y2 = result["box"]
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)    
        cv2.putText(image, result["label"], (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    cv2.imshow("Image", image)
    cv2.waitKey(0)
    