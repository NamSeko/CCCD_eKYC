import re
from exceptions.exceptions import ID_Format_Exception

# Bảng mã tỉnh / thành phố trực thuộc TW theo quy chuẩn
PROVINCE_CODES = {
    "001": "Hà Nội", "002": "Hà Giang", "004": "Cao Bằng", "006": "Bắc Kạn",
    "008": "Tuyên Quang", "010": "Lào Cai", "011": "Điện Biên", "012": "Lai Châu",
    "014": "Sơn La", "015": "Yên Bái", "017": "Hòa Bình", "019": "Thái Nguyên",
    "020": "Lạng Sơn", "022": "Quảng Ninh", "024": "Bắc Giang", "025": "Phú Thọ",
    "026": "Vĩnh Phúc", "027": "Bắc Ninh", "030": "Hải Dương", "031": "Hải Phòng",
    "033": "Hưng Yên", "034": "Thái Bình", "035": "Hà Nam", "036": "Nam Định",
    "037": "Ninh Bình", "038": "Thanh Hóa", "040": "Nghệ An", "042": "Hà Tĩnh",
    "044": "Quảng Bình", "045": "Quảng Trị", "046": "Thừa Thiên Huế", "048": "Đà Nẵng",
    "049": "Quảng Nam", "051": "Quảng Ngãi", "052": "Bình Định", "054": "Phú Yên",
    "056": "Khánh Hòa", "058": "Ninh Thuận", "060": "Bình Thuận", "062": "Kon Tum",
    "064": "Gia Lai", "066": "Đắk Lắk", "067": "Đắk Nông", "068": "Lâm Đồng",
    "070": "Bình Phước", "072": "Tây Ninh", "074": "Cà Mau", "075": "Bạc Liêu",
    "077": "Trà Vinh", "079": "Cần Thơ", "080": "Hậu Giang", "082": "Sóc Trăng",
    "083": "An Giang", "084": "Đồng Tháp", "086": "Vĩnh Long", "087": "Tiền Giang",
    "089": "Bến Tre", "090": "Đồng Nai", "091": "Bà Rịa – Vũng Tàu", "092": "Thành phố Hồ Chí Minh",
    "093": "Long An", "094": "Tây Ninh", "095": "Thừa Thiên Huế",
    "999": "Không xác định"  # Trường hợp đặc biệt chưa có trong danh sách
}

GENDER_CENTURY_MAP = {
    0: ("Nam", 20, 19),
    1: ("Nữ",  20, 19),
    2: ("Nam", 21, 20),
    3: ("Nữ",  21, 20),
    4: ("Nam", 22, 21),
    5: ("Nữ",  22, 21),
    6: ("Nam", 23, 22),
    7: ("Nữ",  23, 22),
    8: ("Nam", 24, 23),
    9: ("Nữ",  24, 23),
}

def parse_cccd_id(id_number: str) -> dict | None:
    id_clean = re.sub(r"\D", "", str(id_number))
    if len(id_clean) != 12:
        raise ID_Format_Exception("ID format incorrect !!!")

    prov_code = id_clean[0:3]
    gender_century_code = int(id_clean[3])
    birth_year_suffix = id_clean[4:6]
    random_code = id_clean

    gender, century, year_prefix = GENDER_CENTURY_MAP.get(gender_century_code, ("Không xác định", None, None))
    full_birth_year = f"{year_prefix}{birth_year_suffix}" if year_prefix else None

    return {
        "id_number": id_clean,
        "province_code": prov_code,
        "province_name": PROVINCE_CODES.get(prov_code, "Chưa cập nhật"),
        "gender": gender,
        "century": century,
        "birth_year": int(full_birth_year) if full_birth_year else None,
        "random_code": random_code,
    }