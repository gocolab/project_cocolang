from typing import Optional, List
from beanie import Document
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class User(Document):
    name: str = None
    email: EmailStr
    roles :List[str] = ['GUEST',]
    # google oauth
    email_verified: bool = False
    picture: str = None
    given_name: str = None
    family_name: str = None
    exp: int = 0
    oauth_issuer: str = 'google'
    create_date: datetime = Field(default_factory=datetime.now)
    last_access_date: datetime = Field(default_factory=datetime.now)

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
