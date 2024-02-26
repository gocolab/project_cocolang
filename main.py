import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from database.connection import Settings

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
from routes.events import event_router
from routes.events_api import router as event_api_router
from routes.users import router as user_router
from routes.common_codes import router as common_codes_router
from routes.comodules import router as comodules_router
from routes.mains import router as mains_router

app.include_router(user_router, prefix="/users")
app.include_router(common_codes_router, prefix="/commoncodes")
app.include_router(comodules_router, prefix="/comodules")
app.include_router(mains_router, prefix="/mains")

app.include_router(event_router, prefix="/event")
app.include_router(event_api_router, prefix="/events_api")

@app.on_event("startup")
async def init_db():
    await settings.initialize_database()

from fastapi.staticfiles import StaticFiles
# url 경로, 자원 물리 경로, 프로그램밍 측면
import os
static_css_directory = os.path.join("resources", "css")
static_images_directory = os.path.join("resources", "images")
app.mount("/css", StaticFiles(directory=static_css_directory), name="static_css")
app.mount("/images", StaticFiles(directory=static_images_directory), name="static_images")

from fastapi import Request
from fastapi.templating import Jinja2Templates
# html 들이 있는 폴더 위치
templates = Jinja2Templates(directory="templates/")

from typing import List, Optional
@app.get("/")
async def root(request: Request, page_number: Optional[int] = 1):
    return RedirectResponse(url=f"/mains/list/{page_number}")

if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
