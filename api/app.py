from sys import prefix
from fastapi import FastAPI, Depends # type: ignore
from fastapi.responses import HTMLResponse # type: ignore
from fastapi.exceptions import RequestValidationError # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from starlette.exceptions import HTTPException as StarletteHTTPException # type: ignore
from dependencies.request_id_dependency import attach_request_id

app = FastAPI(
    dependencies=[
        Depends(attach_request_id)
    ]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE = "/api/id_ekyc/v1.0"

app.include_router(prefix=BASE)