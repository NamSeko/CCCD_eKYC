from modules import *
import cv2 # type: ignore
from utils import ocr_validation

def ocr(img):
    raw_results = {}
    field_detection = detector.detect(img)
    for field in field_detection:
        x1, y1, x2, y2 = field['box']
        field_crop = img[y1:y2, x1:x2]
        label = field['label']
        text = reader(field_crop)
        raw_results[label] = text.strip() if isinstance(text, str) else text

    final_results = {}
    residence_parts = []

    for label, text in raw_results.items():
        if "residence" in label:
            residence_parts.append((label, text))
        elif label == "ID":
            id_info = ocr_validation.parse_cccd_id(text)
            final_results["id_number"] = id_info["id_number"]
            final_results["province_name"] = id_info["province_name"]
            final_results["gender"] = id_info["gender"]
            final_results["birth_year"] = id_info["birth_year"]
        else:
            final_results[label] = text

    if residence_parts:
        residence_parts.sort(key=lambda x: x[0])
        final_results["residence"] = ", ".join(text for _, text in residence_parts if text)
    

    return final_results


# img = cv2.imread("../photo_2026-05-05_16-40-49.jpg")
# img = cv2.imread("../2026-06-24 15.44.40.jpg")
img = cv2.imread("../img1.jpg")
# img = cv2.imread("../E0105823581_jpg.rf.64b48d01132b6e05497079563582ccec.jpg")
print(ocr(img))