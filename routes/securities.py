from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer
import httpx
from auth.hash_password import HashPassword
from fastapi.security import OAuth2PasswordRequestForm
from auth.jwt_handler import create_access_token

router = APIRouter(tags=["securities"])

from fastapi.templating import Jinja2Templates
from fastapi import Request

templates = Jinja2Templates(directory="templates/")

from database.connection import Database
from models.users import User
collection_user = Database(User)

hash_password = HashPassword()

@router.get("/login") # 펑션 호출 방식
async def insert(request:Request):
    return templates.TemplateResponse(name="securities/login.html"
    , context={'request':request})

@router.post("/signin")
async def sign_user_in(request:Request, user: OAuth2PasswordRequestForm = Depends()):
    user_exist = await User.find_one(User.email == user.username)
    if not user_exist:
        context = {'request': request, 'error': "User with email does not exist."}
        return templates.TemplateResponse(name="securities/login.html", context=context)
    if hash_password.verify_hash(user.password, user_exist.password):
        access_token = create_access_token(user_exist.email)
        access_auths = {
            "access_token": access_token,
            "token_type": "Bearer"
        }
        return templates.TemplateResponse(name="main.html"
                            , context={'request':request
                                       , 'access_auths':access_auths})

    context = {'request': request, 'error': "Invalid details passed."}
    return templates.TemplateResponse(name="securities/login.html", context=context)