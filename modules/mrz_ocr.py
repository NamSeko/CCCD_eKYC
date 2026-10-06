import cv2 # type: ignore
import numpy as np # type: ignore
from mrzscanner import MRZScanner # type: ignore
from exceptions.exceptions import MRZ_Format_Exception
from datetime import date

def parse_mrz_date(value: str, max_age: int = 120) -> date:
    if len(value) != 6 or not value.isdigit():
        raise ValueError("Birth date must be YYMMDD")
    yy = int(value[:2])
    mm = int(value[2:4])
    dd = int(value[4:6])
    today = date.today()
    century = (today.year // 100) * 100
    candidates = []
    for year in [century + yy, century - 100 + yy]:
        try:
            dob = date(year, mm, dd)
        except ValueError:
            continue
        if dob > today:
            continue
        age = (today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day)))
        if 0 <= age <= max_age:
            candidates.append(dob)
    if not candidates:
        raise ValueError(f"Cannot determine DOB from: {value}")
    return max(candidates)

def parse_mrz_expiry(
    value: str,
    dob: date | None = None
) -> date:
    if len(value) != 6 or not value.isdigit():
        raise ValueError("Expiry date must be YYMMDD")
    yy = int(value[:2])
    mm = int(value[2:4])
    dd = int(value[4:6])
    candidates = []
    for year in [1900 + yy, 2000 + yy]:
        try:
            exp = date(year, mm, dd)
        except ValueError:
            continue
        if dob and exp <= dob:
            continue
        candidates.append(exp)
    if not candidates:
        raise ValueError(f"Cannot determine expiry date: {value}")
    today = date.today()
    return min(candidates, key=lambda d: abs(d.year - today.year))

def parse_name(name_raw: str) -> dict:
    name_raw = name_raw.rstrip("<")
    parts = name_raw.split("<<", 1)
    surname = parts[0].replace("<", " ").strip()
    given_names = ""
    if len(parts) > 1:
        given_names = (parts[1].replace("<", " ").strip())
    full_name = " ".join(x for x in [surname, given_names] if x)
    return {
        "surname": surname,
        "given_names": given_names,
        "full_name": full_name
    }

def parse_passport(mrz_texts: list[str]) -> dict:
    if len(mrz_texts) != 2:
        raise ValueError(f"Passport TD3 requires 2 MRZ lines, got {len(mrz_texts)}")
    line1 = mrz_texts[0].strip()
    line2 = mrz_texts[1].strip()
    if len(line1) < 44 or len(line2) < 44:
        raise ValueError(f"Invalid TD3 MRZ length: line1={len(line1)}, line2={len(line2)}")
    document_code = line1[0:2].replace("<", "")
    issuing_country = line1[2:5]
    name_raw = line1[5:44]
    name = parse_name(name_raw)
    passport_number = line2[0:9].replace("<", "")
    passport_number_check = line2[9]
    nationality = line2[10:13]
    dob_raw = line2[13:19]
    dob_check = line2[19]
    gender = line2[20]
    expiry_raw = line2[21:27]
    expiry_check = line2[27]
    personal_number = (line2[28:42].replace("<", ""))
    personal_number_check = line2[42]
    composite_check = line2[43]
    dob = parse_mrz_date(dob_raw)
    expiry_date = parse_mrz_expiry(expiry_raw, dob)
    return {
        "docs_type": document_code,
        "country_code": issuing_country,
        "docs_number": passport_number,
        "nationality": nationality,
        "date_of_birth": dob.strftime("%d/%m/%Y"),
        "gender": gender,
        "expiration_date": expiry_date.strftime("%d/%m/%Y"),
        "surname": name["surname"],
        "given_names": name["given_names"],
        "full_name": name["full_name"],
        "personal_number": personal_number,

        "check_digits": {
            "passport_number": passport_number_check,
            "date_of_birth": dob_check,
            "expiration_date": expiry_check,
            "personal_number": personal_number_check,
            "composite": composite_check
        }
    }

def parse_id_card(mrz_texts: list[str]) -> dict:
    if len(mrz_texts) != 3:
        raise ValueError(f"TD1 requires 3 MRZ lines, got {len(mrz_texts)}")
    line1, line2, line3 = mrz_texts
    docs_type = line1[:2]
    country_code = line1[2:5]
    docs_number = line1[5:14]
    id_number = line1[15:27]
    dob_raw = line2[:6]
    gender = line2[7]
    expiry_raw = line2[8:14]
    nationality = line2[15:18]
    dob = parse_mrz_date(dob_raw)
    exp_date = parse_mrz_expiry(expiry_raw, dob)
    name = parse_name(line3)
    return {
        "docs_type": docs_type,
        "country_code": country_code,
        "docs_number": docs_number,
        "id_number": id_number,
        "date_of_birth": dob.strftime("%d/%m/%Y"),
        "gender": gender,
        "expiration_date": exp_date.strftime("%d/%m/%Y"),
        "nationality": nationality,
        "surname": name["surname"],
        "given_names": name["given_names"],
        "full_name": name["full_name"]
    }

def MrzScanner(
    reader: MRZScanner = None,
    image: np.ndarray = None
):
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    result = reader(image, do_center_crop=False, do_postprocess=False)
    mrz_texts = result["mrz_texts"]
    # print("MRZ:", mrz_texts)
    if not mrz_texts:
        raise ValueError("MRZ not detected")
    if len(mrz_texts) == 2:
        return parse_passport(mrz_texts)
    elif len(mrz_texts) == 3:
        return parse_id_card(mrz_texts)
    else:
        raise MRZ_Format_Exception(f"Unsupported MRZ format: {len(mrz_texts)} lines")