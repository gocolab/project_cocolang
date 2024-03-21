import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from app.database.connection import Settings

app = FastAPI()

settings = Settings()

# 출처 등록

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우트 등록
from app.routes.users import router as user_router
from app.routes.common_codes import router as common_codes_router
from app.routes.comodules import router as comodules_router
from app.routes.mains import router as mains_router
from app.routes.securities import router as securities_router
from app.routes.errors import router as errors_router

app.include_router(user_router, prefix="/users")
app.include_router(common_codes_router, prefix="/commoncodes")
app.include_router(comodules_router, prefix="/comodules")
app.include_router(mains_router, prefix="/mains")
app.include_router(comodules_router, prefix="/devtemplates")
app.include_router(securities_router, prefix="/securities")
app.include_router(errors_router, prefix="/errors")

@app.on_event("startup")
async def init_db():
    await settings.initialize_database()

from app.auth.jwt_handler import verify_access_token
# 제외할 URL 경로 목록
EXCLUDE_PATHS = [
    "/css", "/images", "/js"
    , "/favicon.ico", "/errors"
    , '/users/form', '/mains/list'
    ,"/devtemplates/list"
    , "/comodules/list", '/comodules/v1'
    , '/securities/login', '/users/signup'
    # "/docs",   # Swagger 문서
    # "/openapi.json",  # OpenAPI 스펙
]

# Role-based URL access configuration
ROLE_BASED_ACCESS = {
    "GUEST": ["/comodules/download"
              , "/securities", '/users/read']
    ,"PARTNER": ["/comodules", "/devtemplates", ]
    ,"ADMIN": ["/admins", '/commoncodes', '/users']
}

from app.auth.authenticate import userfromauthenticate
# Middleware for token verification
@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    user = await userfromauthenticate(request)
    request.state.user = user

    if not (any(request.url.path.startswith(path) for path in EXCLUDE_PATHS) 
            or request.url.path == '/'):
        # Role-based access control
        user_roles: List[str] = user.get("roles", [])
        path_allowed = False
        for role in user_roles:
            if any(request.url.path.startswith(path) for path in ROLE_BASED_ACCESS.get(role, [])):
                path_allowed = True
                break
        
        if not path_allowed:
            # Redirect user to a "permission denied" page if they have no access
            # return RedirectResponse(url="/errors/permission-denied")
            return RedirectResponse(url="/securities/login")

    # Continue with the next middleware or route handler
    response = await call_next(request)
    await log_request_response(request, response, user)
    return response

import time
import json
from app.models.request_log import RequestLog  # 로그 모델 임포트
async def log_request_response(request: Request, response: Response, user):
    # 요청 처리 전 시간 측정
    start_time = time.time()
 
     # Extract parameters based on the request method
    parameters = {}
    if request.method == "GET":
        parameters = dict(request.query_params)
    # elif request.method in ["POST", "PUT", "DELETE"]:
    #     # Accumulate request body data into a bytearray
    #     # request_body = bytearray()
    #     # async for chunk in request.stream():
    #     #     request_body.extend(chunk)
    #     # # Decode the bytearray as JSON
    #     # parameters = json.loads(request_body.decode())
    # else:

    # async def response_bytes(response):
    #     async for chunk in response.body_iterator:
    #         yield chunk
    
    # response_body = b''.join([chunk async for chunk in response_bytes(response)])
    
    end_time = time.time()
    duration = end_time - start_time
    
    # 로그 데이터 준비 및 저장
    log_data = RequestLog(
        request={
            "method": request.method
            ,'header': dict(request.headers)
            , "parameters": parameters
            # ,"body": (await request.body())
        },
        response={
            "status_code": response.status_code,
            # "body": response_body,  # 여기서는 'utf-8' 대신 적절한 인코딩을 사용해야 할 수도 있음
        }
        ,duration=duration
        ,user=user
    )

    # MongoDB에 로그 데이터 저장
    await log_data.insert()


from fastapi.staticfiles import StaticFiles
# url 경로, 자원 물리 경로, 프로그램밍 측면
import os
static_css_directory = os.path.join("app", "resources", "css")
static_images_directory = os.path.join("app", "resources", "images")
static_js_directory = os.path.join("app", "resources", "js")
static_downloads_directory = os.path.join("app", "resources", "downloads")
app.mount("/css", StaticFiles(directory=static_css_directory), name="static_css")
app.mount("/images", StaticFiles(directory=static_images_directory), name="static_images")
app.mount("/js", StaticFiles(directory=static_js_directory), name="static_js")
app.mount("/downloads", StaticFiles(directory=static_downloads_directory), name="static_downloads")

from fastapi import Request
from fastapi.templating import Jinja2Templates
# html 들이 있는 폴더 위치
templates = Jinja2Templates(directory="app/templates/")

from typing import List, Optional
@app.get("/")
async def root(request: Request, page_number: Optional[int] = 1):
    return RedirectResponse(url=f"/mains/list/{page_number}")

if __name__ == '__main__':
    pass
    # uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
