from typing import Optional, List
from beanie import Document

from pydantic import BaseModel, EmailStr


class User(Document):
    name: Optional[str] = None
    email: EmailStr
    password: str
    manager: Optional[str] = None
    sellist1 : Optional[str] = None
    text : Optional[str] = None
    role : Optional[str] = None

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
