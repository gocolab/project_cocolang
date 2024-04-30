from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi.security import OAuth2PasswordRequestForm
from app.auth.jwt_handler import create_access_token

router = APIRouter(tags=["securities"])

from fastapi.templating import Jinja2Templates
from fastapi import Request

templates = Jinja2Templates(directory="app/templates/")

from app.database.connection import Database
from app.models.users import User, TokenResponse
collection_user = Database(User)

# auths
from authlib.integrations.starlette_client import OAuth, OAuthError
from app.configs.config_auths import CLIENT_ID, CLIENT_SECRET

oauth = OAuth()
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    client_kwargs={
        'scope': 'email openid profile',
        # 'redirect_url': 'http://localhost:8000/securities/oauth_google'
    }
)

@router.get("/login_google")
async def login_google(request:Request):
    url = request.url_for('oauth_google')
    result = await oauth.google.authorize_redirect(request, url)
    return result

from app.routes.mains import main_list

@router.get('/oauth_google', name='oauth_google')
async def oauth_google(request: Request):
    token_google = ''
    try:
        token_google = await oauth.google.authorize_access_token(request)
    except OAuthError as e:
        return templates.TemplateResponse(
            name='errors/error_auth.html',
            context={'request': request, 'message': e.error}
        )
    user_exist = token_google.get('userinfo')

    response = await signin_withsignup(request, user_exist)
    return response        

async def signin_withsignup(request:Request, user):
    user_exist = await User.find_one(User.email == user.email)
    _model = User(**user)
    if not user_exist: 
        # If the user does not exist, insert the new user model instance.
        result = await _model.insert()
    else:
        # Perform the update operation using the user's ID as the criterion.
        # Make sure to access the ID field correctly according to your ORM.
        # result = await User.update_one({'_id': user_exist.id}, update_data)
        result = await collection_user.update(user_exist.id, _model.dict(exclude={'roles'}))

    # create access token in this site
    access_token = create_access_token(user.email)

    # main tempage information for return 
    request.state.user = user
    context = await main_list(request)
    # response.set_cookie(key="Authorization", value=f"Bearer {access_token}", httponly=True)
    response = templates.TemplateResponse(name="main.html"
                                    , context=context)

    response.set_cookie(key="Authorization", value=f"Bearer {access_token}"
                        ,httponly=True  # Prevents client-side JS from accessing the cookie
                        ,samesite="Lax"  # Controls cross-site cookie sending
                        ,secure=True  # Ensures cookie is sent over HTTPS only
                        )
    return response        

# 로그아웃 처리
@router.get("/logout")
async def logout(request: Request):
    request.state.user = {}
    context = await main_list(request, page_number=1)

    response = templates.TemplateResponse("main.html"
                                          , context=context)
    response.delete_cookie(key="Authorization")

    return response