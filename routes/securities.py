from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer
import httpx
from auth.hash_password import HashPassword
from fastapi.security import OAuth2PasswordRequestForm
from auth.jwt_handler import create_access_token

router = APIRouter(tags=["securities"])

# GitHub OAuth 설정
CLIENT_ID = "your_github_client_id"
CLIENT_SECRET = "your_github_client_secret"
REDIRECT_URI = "your_redirect_uri"
TOKEN_URL = "https://github.com/login/oauth/access_token"
USER_URL = "https://api.github.com/user"

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://github.com/login/oauth/authorize",
    tokenUrl=TOKEN_URL,
    refreshUrl=None,
    scheme_name="GitHub OAuth",
)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    async with httpx.AsyncClient() as client:
        resp = await client.get(USER_URL, headers={"Authorization": f"token {token}"})
        if resp.status_code != 200:
            raise HTTPException(status_code=400, detail="Invalid authentication credentials")
        user = resp.json()
        return user

@router.get("/login/github")
async def login_via_github(code: str):
    async with httpx.AsyncClient() as client:
        # GitHub로부터 access token 받기
        data = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": code,
            "redirect_uri": REDIRECT_URI,
        }
        resp = await client.post(TOKEN_URL, data=data, headers={"Accept": "routerlication/json"})
        resp_json = resp.json()
        access_token = resp_json.get("access_token")
        if not access_token:
            raise HTTPException(status_code=400, detail="GitHub OAuth failed")
        
        # 사용자 정보 받아오기
        user = await get_current_user(access_token)
        # 여기에서 사용자 정보를 바탕으로 회원 가입 로직을 구현하세요.
        # 예: 사용자 DB에 저장, 사용자 세션 생성 등

        return {"message": "GitHub OAuth succeeded", "user": user}

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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with email does not exist."
        )
    if hash_password.verify_hash(user.password, user_exist.password):
        access_token = create_access_token(user_exist.email)
        access_auths = {
            "access_token": access_token,
            "token_type": "Bearer"
        }
        return templates.TemplateResponse(name="main.html"
                            , context={'request':request
                                       , 'access_auths':access_auths})

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid details passed."
    )
