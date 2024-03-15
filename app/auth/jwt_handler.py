import time
from datetime import datetime

from app.database.connection import Settings
from fastapi import HTTPException, status
from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Optional

settings = Settings()

def create_access_token(email: str, expires_delta: Optional[timedelta] = None):
    payload = {"user_email":email}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = time.time() + int(settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload.update({"expires": expire})

    token = jwt.encode(payload, settings.SECRET_KEY
                       , algorithm=settings.ALGORITHM)
    return token

from app.models.users import User
async def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY
                          , algorithms=[settings.ALGORITHM])

        expire = payload.get("expires")

        # if expire is None:
        #     raise HTTPException(
        #         status_code=status.HTTP_400_BAD_REQUEST,
        #         detail="No access token supplied"
        #     )
        # if datetime.utcnow() > datetime.utcfromtimestamp(expire):
        #     raise HTTPException(
        #         status_code=status.HTTP_403_FORBIDDEN,
        #         detail="Token expired!"
        #     )
        username: str = payload.get("user_email")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No access token supplied"
            )
        user = await User.find_one(User.email == username)
        return user.model_dump()

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token"
        )
