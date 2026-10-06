import logging
import os
import jwt

logger = logging.getLogger(__name__)

JWT_SECRET: str = os.getenv("JWT_SECRET", "change-me-secret")
JWT_ALGORITHM: str = "HS256"
