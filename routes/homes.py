from fastapi import APIRouter
from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request


router = APIRouter()

templates = Jinja2Templates(directory="templates/")
'''
@router.get("/", response_class=HTMLResponse) # 펑션 호출 방식
async def home():
    # return {"message": "home World"}
    html = "<body> <h2>it's Home</h2> </body>"
    return html

@router.get("/list") # 주로 2단계까지만 연결
async def home_list() :
    # pass
    # return 0
    html = "<body> <h2>it's Home list</h2> </body>"
    return html
'''


@router.get("/", response_class=HTMLResponse) # 펑션 호출 방식
async def root(request:Request):
    # return {"message": "home World"}
    return templates.TemplateResponse(name="homes/standards.html", context={'request':request})


# @ = Annotation  / 체질을 바꿔주는 역할 / 웹에서 펑션 호출

@router.get("/list") # 주로 2단계까지만 연결

async def home_list() :
    # pass
    # return 0
    html = "<body> <h2>it's Home list</h2> </body>"
    return html

# /homes/params_query -> /homes/parameters_query.html 호출
@router.get("/params_query", response_class=HTMLResponse) # 펑션 호출 방식
async def home(request:Request):
    # return {"message": "home World"}
    return templates.TemplateResponse(name="homes/parameters_query.html", context={'request':request})