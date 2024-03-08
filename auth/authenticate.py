from auth.jwt_handler import verify_access_token
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import List, Optional

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/securities/signin")

async def authenticate(token: Optional[str] = Depends(oauth2_scheme)) -> str:
    if not token:
        return None
        # raise HTTPException(
        #     status_code=status.HTTP_403_FORBIDDEN,
        #     detail="Sign in for access"
        # )

    decoded_token = verify_access_token(token)
    return decoded_token["user"]
