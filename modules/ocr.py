from vietocr.tool.config import Cfg # type: ignore
from vietocr.tool.predictor import Predictor # type: ignore
import cv2 # type: ignore
from PIL import Image # type: ignore
import numpy as np # type: ignore
from settings import setting # type: ignore
# import json

class OCR:
    def __init__(self, weights_path: str = setting.OCR_MODEL_PATH, device: str = setting.DEVICE):
        conf = Cfg.load_config_from_name('vgg_seq2seq')
        conf['weights'] = weights_path
        conf['cnn']['pretrained'] = False
        conf['device'] = device
        self.ocr = Predictor(conf)

    def __call__(self, image: np.ndarray) -> str:
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        image = Image.fromarray(image)
        result = self.ocr.predict(image)
        return result


if __name__ == "__main__":
    reader = OCR()
    # img = cv2.imread("../image1.png")
    img = cv2.imread("../image3.png")
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    result = reader(img)
    # result = json.dumps(result, indent=4, ensure_ascii=False)
    print(result)
