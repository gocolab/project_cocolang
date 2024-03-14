import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.responses import RedirectResponse
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

app.include_router(user_router, prefix="/users")
app.include_router(common_codes_router, prefix="/commoncodes")
app.include_router(comodules_router, prefix="/comodules")
app.include_router(mains_router, prefix="/mains")
app.include_router(comodules_router, prefix="/devtemplates")
app.include_router(securities_router, prefix="/securities")

@app.on_event("startup")
async def init_db():
    await settings.initialize_database()

import time
from app.models.request_log import RequestLog  # 로그 모델 임포트
# 미들웨어를 사용하여 요청과 응답 로그를 MongoDB에 저장
@app.middleware("http")
async def log_request_response(request: Request, call_next):
    # 요청 처리 전 시간 측정
    start_time = time.time()

    # 요청 처리
    original_response  = await call_next(request)

    # 요청 처리 후 시간 측정
    end_time = time.time()

    # 처리 시간 계산 (초 단위)
    duration = end_time - start_time

    # 응답의 본문을 읽음 (스트리밍 응답을 처리하기 위해)
    response_body = b''
    async for chunk in original_response.body_iterator:
        response_body += chunk
    # 새로운 응답 생성
    new_response = Response(content=response_body
                            , status_code=original_response.status_code
                            , headers=dict(original_response.headers))
    
    # 로그 데이터 준비 및 저장
    log_data = RequestLog(
        request={
            "method": request.method,
            "url": str(request.url),
            "body": (await request.body())
        },
        response={
            "status_code": original_response.status_code,
            "body": response_body,  # 여기서는 'utf-8' 대신 적절한 인코딩을 사용해야 할 수도 있음
        }
        ,duration=duration
    )

    # MongoDB에 로그 데이터 저장
    await log_data.insert()

    return new_response

@app.get("/items/")
async def read_items(item_id: str):
    return {"item_id": item_id}

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
