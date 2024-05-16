from typing import Optional
from fastapi.templating import Jinja2Templates
from app.database.connection import Database
from fastapi import APIRouter, Depends, HTTPException, Request, status

from app.models.common_codes import CommonCode

router = APIRouter(tags=["CommonCodes"])
templates = Jinja2Templates(directory="app/templates/")

# Database 클래스와 CommonCode 모델을 적절히 정의했다고 가정
collection_common_codes = Database(CommonCode)

@router.get("/form")
@router.get("/update/{code_id}")
async def form(request: Request, code_id: str = None):
    main_router = request.url.path.split('/')[1]

    common_code = {}
    if code_id is not None:
        common_code = await collection_common_codes.get(code_id)
        if common_code is None:
            raise HTTPException(status_code=404, detail="CommonCode not found")

    return templates.TemplateResponse(name="common_codes/form.html",
                                      context={'request': request,
                                               'common_code': common_code,
                                               'main_router': main_router})

@router.post("/insert")
async def create(request: Request):
    common_code_data = dict(await request.form())
    user = request.state.user  # userfromauthenticate 구현 가정
    common_code_data["create_user_id"] = user['id']
    common_code_data["create_user_name"] = user['name']
    main_router = request.url.path.split('/')[1]
    common_code_data["main_router"] = main_router

    common_code = CommonCode(**common_code_data)
    result_id = await collection_common_codes.save(common_code)

    context = await common_codes_list(request, 1)
    return templates.TemplateResponse("common_codes/list.html", context=context)

@router.get("/list/{page_number}")
@router.get("/list")  # 검색 with pagination
async def list(request: Request, page_number: Optional[int] = 1):
    context = await common_codes_list(request, page_number)
    return templates.TemplateResponse(name="common_codes/list.html", context=context)

async def common_codes_list(request: Request, page_number: Optional[int] = 1):
    _dict = dict(request.query_params)
    queries = []
    main_router = request.url.path.split('/')[1]
    try:
        search_word = _dict["word"].strip()
        if search_word:
            queries.append({_dict['key_name']: {'$regex': search_word}})
    except:
        pass

    if queries:
        conditions = {'$and': queries}
    else:
        conditions = {}

    common_codes_list, pagination = await collection_common_codes.getsbyconditionswithpagination(conditions, page_number)
    context = {'request': request, 'common_codes': common_codes_list
               , 'pagination': pagination, 'main_router': main_router}
    return context

@router.get("/{code_id}")
async def read(request: Request, code_id: str = None):
    main_router = request.url.path.split('/')[1]

    common_code = await collection_common_codes.get(code_id)
    if common_code is None:
        raise HTTPException(status_code=404, detail="CommonCode not found")

    return templates.TemplateResponse("common_codes/read.html",
                                      {"request": request,
                                       "common_code": common_code,
                                       'main_router': main_router})

@router.post("/update/{code_id}")
async def update(request: Request, code_id: str):
    common_code = await collection_common_codes.get(code_id)
    if common_code:
        common_code_data = dict(await request.form())
        _model = CommonCode(**common_code_data)
        result = await collection_common_codes.update(code_id, _model)
        context = await common_codes_list(request)
        return templates.TemplateResponse("common_codes/list.html", context=context)
    else:
        raise HTTPException(status_code=404, detail="CommonCode not found")

@router.post("/{code_id}")
async def delete(request: Request, code_id: str):
    result_id = await collection_common_codes.delete(code_id)
    context = await common_codes_list(request)
    return templates.TemplateResponse(name="common_codes/list.html", context=context)
