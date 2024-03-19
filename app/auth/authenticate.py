from datetime import timedelta
import datetime
import os

from fastapi.responses import HTMLResponse
from app.auth.jwt_handler import verify_access_token
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import List, Optional
from jose import jwt, JWTError
from app.models.users import User
from app.database.connection import Settings
from fastapi import Request

settings = Settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/securities/signin")

async def authenticate(request: Request):
    return request.state.user

async def userfromauthenticate(request: Request):
    # Exclude certain paths from role-based access control
    authorization = request.cookies.get("Authorization")
    user = {}
    if authorization:
        token = authorization.split(" ")[1]
        try:
            user = await verify_access_token(token)
            request.state.user = user
        except Exception as e:
            return HTMLResponse(content=str(e), status_code=401)
    return user