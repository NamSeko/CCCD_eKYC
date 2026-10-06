from typing import Any, Optional
from pydantic import BaseModel

class Response(BaseModel):
    response_code: int
    response_status: str
    response_message: str
    request_id: Optional[str] = None
    response_data: Any = None

class SuccessResponse(Response):
    response_code: int = 200
    response_status: str = "OK"
    response_message: str = "Success"

class ErrorResponse(Response):
    response_code: int = 400
    response_status: str = "BAD_REQUEST"
    response_message: str = "Bad Request"