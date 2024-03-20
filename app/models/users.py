from typing import Optional, List
from beanie import Document

from pydantic import BaseModel, EmailStr


class User(Document):
    name: str = None
    email: EmailStr
    password: str
    roles :List[str] = ['GUEST']

    class Settings:
        name = "users"

    class Config:
        json_schema_extra = {
            "example": {
                "email": "fastapi@packt.com",
                "password": "strong!!!"
            }
        }


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
