class OCRException(Exception):
    def __init__(
        self,
        response=400,
        response_status="CANNOT OCR",
        message="OCR processing failed!"
    ):
        self.response = response
        self.response_status = response_status
        self.message = message

        super().__init__(self.message)

class MRZ_Format_Exception(OCRException):
    def __init__(
        self,
        message="MRZ format incorrect !!!",
        prefix=None
    ):
        if prefix:
            message = f"{prefix}: {message}"

        super().__init__(
            response=400,
            response_status="MRZ INCORRECT",
            message=message
        )

class ID_Format_Exception(OCRException):
    def __init__(
        self,
        message="ID format incorrect !!!",
        prefix=None
    ):
        if prefix:
            message = f"{prefix}: {message}"

        super().__init__(
            response=400,
            response_status="ID INCORRECT",
            message=message
        )