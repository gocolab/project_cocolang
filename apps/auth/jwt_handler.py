import time
from datetime import datetime

from apps.database.connection import Settings
from fastapi import HTTPException, status
from jose import jwt, JWTError

settings = Settings()

def create_access_token(user: str):
    payload = {
        "user": user,
        # "expires": time.time() + 3600
        "expires": time.time() + int(settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    }

    token = jwt.encode(payload, settings.SECRET_KEY
                       , algorithm=settings.ALGORITHM)
    return token


def verify_access_token(token: str):
    try:
        data = jwt.decode(token, settings.SECRET_KEY
                          , algorithms=[settings.SECRET_KEY])

        expire = data.get("expires")

        if expire is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No access token supplied"
            )
        if datetime.utcnow() > datetime.utcfromtimestamp(expire):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token expired!"
            )
        return data

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token"
        )
