from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer
import httpx
from apps.auth.hash_password import HashPassword
from fastapi.security import OAuth2PasswordRequestForm
from apps.auth.jwt_handler import create_access_token
from fastapi.responses import RedirectResponse

router = APIRouter(tags=["securities"])

from fastapi.templating import Jinja2Templates
from fastapi import Request

templates = Jinja2Templates(directory="templates/")

from apps.database.connection import Database
from apps.models.users import User, TokenResponse
collection_user = Database(User)

hash_password = HashPassword()

@router.get("/login") # 펑션 호출 방식
async def insert(request:Request):
    return templates.TemplateResponse(name="securities/login.html"
    , context={'request':request})

from apps.routes.mains import main_list
@router.post("/login")
async def sign_in(request:Request, user: OAuth2PasswordRequestForm = Depends()):
    user_exist = await User.find_one(User.email == user.username)
    if not user_exist:
        context = {'request': request, 'error': "User with email does not exist."}
        return templates.TemplateResponse(name="securities/login.html", context=context)
    if hash_password.verify_hash(user.password, user_exist.password):
        access_token = create_access_token(user_exist.email)

        context = await main_list(request)
        response = templates.TemplateResponse(name="main.html"
                                        , context=context)
        response.set_cookie(key="access_token", value=f"{access_token}", httponly=True)
        response.set_cookie(key="token_type", value=f"Bearer", httponly=True)
        return response        

    context = {'request': request, 'error': "Invalid password."}
    return templates.TemplateResponse(name="securities/login.html", context=context)

@router.post("/signin", response_model=TokenResponse)
async def sign_user_in(user: OAuth2PasswordRequestForm = Depends()) -> dict:
    user_exist = await User.find_one(User.email == user.username)
    if not user_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with email does not exist."
        )
    if hash_password.verify_hash(user.password, user_exist.password):
        access_token = create_access_token(user_exist.email)
        return {
            "access_token": access_token,
            "token_type": "Bearer"
        }

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid details passed."
    )

# 로그아웃 처리
@router.get("/logout")
async def logout(request: Request):
    response = templates.TemplateResponse("main.html", {"request": request})
    response.delete_cookie(key="access_token")
    return response