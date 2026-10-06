from .detection import Detection
from .ocr import OCR
from .mrz_ocr import (
    parse_id_card,
    parse_mrz_date,
    parse_mrz_expiry,
    parse_name,
    parse_passport,
    MrzScanner
)
from mrzscanner import MRZScanner # type: ignore

detector = Detection()
reader = OCR()
mrz_reader = MRZScanner()

__all__ = [
    "detector",
    "reader",
    "mrz_reader",
    "parse_id_card",
    "parse_mrz_date",
    "parse_mrz_expiry",
    "parse_name",
    "parse_passport",
    "MrzScanner"
]