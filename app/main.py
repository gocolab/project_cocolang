import uvicorn
from fastapi import FastAPI
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
