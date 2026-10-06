from uuid import uuid4
from fastapi import Request # type: ignore

def attach_request_id(request: Request):
    if 'x-request-id' in request.headers and request.headers['x-request-id']:
        request_id = str(request.headers['x-request-id'])
    else:
        request_id = str(uuid4())
    request.state.request_id = request_id
    return request_id

def exec_request_id(request: Request, default="req-id"):
    if hasattr(request.state, "request_id"):
        return request.state.request_id
    else:
        return default