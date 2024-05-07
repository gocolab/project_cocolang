from fastapi import FastAPI, APIRouter, Request, HTTPException, status, Depends
from fastapi.templating import Jinja2Templates
from app.database.connection import Database  # Assume this handles your database connection
from app.models.comodules import CoModule  # This should be your CoModule model
from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional
from app.auth.authenticate import authenticate
from app.models.users import User

router = APIRouter(tags=["CoModules"])
templates = Jinja2Templates(directory="app/templates/")

# Assuming Database class and CoModule model are defined appropriately
collection_comodule = Database(CoModule)

@router.get("/form") 
@router.get("/update/{comodule_id}") 
async def form(request:Request, comodule_id: str = None):
    main_router = request.url.path.split('/')[1]

    comodule = {}
    if comodule_id is not None:
        comodule = await collection_comodule.get(comodule_id)
        if comodule is None:
            raise HTTPException(status_code=404, detail="CoModule not found")

    return templates.TemplateResponse(name="comodules/form.html"
                                      , context={'request':request
                                                 ,'comodule' : comodule
                                                 ,'main_router':main_router})

async def extract_splitlines_from_string(input_str: str):
    # 문자열을 줄바꿈 기준으로 분리
    lines = input_str.splitlines()
    
    # 빈 문자열을 제외하고 유효한 URL만을 리스트에 추가
    list_input = [line.strip() for line in lines if line.strip()]
    
    return list_input

# CRUD Operations
@router.post("/insert")
async def create(request: Request):
    comodule_data = dict(await request.form())
    user = request.state.user
    comodule_data["create_user_id"] = user['id']
    comodule_data["create_user_name"] = user['name']
    main_router = request.url.path.split('/')[1]
    comodule_data["main_router"] = main_router

    comodule = CoModule(**comodule_data)
    result_id = await collection_comodule.save(comodule)

    context = await comodules_list(request, 1)
    return templates.TemplateResponse("comodules/list.html"
                                      , context=context)


@router.get("/list/{page_number}")
@router.get("/list") # 검색 with pagination
async def list(request: Request, page_number: Optional[int] = 1):
    context = await comodules_list(request, page_number)
    
    return templates.TemplateResponse(name="comodules/list.html"
                                      , context=context)

async def comodules_list(request: Request, page_number: Optional[int] = 1):
    _dict = dict(request._query_params)
    querys = []
    main_router = request.url.path.split('/')[1]
    querys.append({'main_router':main_router})
    try :
        search_word = _dict["word"].strip()
        if search_word :
            querys.append({_dict['key_name'] : { '$regex': search_word}})
    except:
        pass

    conditions = {'$and':querys}
    comodules_list, pagination = await collection_comodule.getsbyconditionswithpagination(conditions
                                                                     ,page_number)
    context={'request':request, 'comodules' : comodules_list
             ,'pagination' : pagination, 'main_router':main_router }
    return context

@router.get("/{comodule_id}")
async def read(request: Request, comodule_id: str = None):
    main_router = request.url.path.split('/')[1]

    comodule = await collection_comodule.get(comodule_id)
    if comodule is None:
        raise HTTPException(status_code=404, detail="CoModule not found")
    
    return templates.TemplateResponse("comodules/read.html"
                                      , {"request": request
                                         , "comodule": comodule
                                         ,'main_router':main_router})

@router.post("/update/{comodule_id}")
async def update(request: Request, comodule_id: str):
    comodule = await collection_comodule.get(comodule_id)
    if comodule:
        comodule_data = dict(await request.form())
        _model = CoModule(**comodule_data)
        result = await collection_comodule.update(comodule_id, _model)
        context = await comodules_list(request)
        return templates.TemplateResponse("comodules/list.html"
                                          , context=context)
    else:
        raise HTTPException(status_code=404, detail="CoModule not found")

@router.post("/{comodule_id}")
async def delete(request: Request, comodule_id: str):
    result_id = await collection_comodule.delete(comodule_id)
    context = await comodules_list(request)
    return templates.TemplateResponse(name="comodules/list.html"
                                      , context=context)

from fastapi.responses import FileResponse
import httpx
import zipfile
import os

@router.get("/v1/{comodule_id}")
async def read(request: Request, comodule_id: str):
    comodule = await collection_comodule.get(comodule_id)
    if comodule is None:
        raise HTTPException(status_code=404, detail="CoModule not found")
    return comodule

@router.get("/v1/list/main")
# async def get_list(language: List[str] = None, framework: List[str] = None, database: List[str] = None):
async def get_list(request: Request):
    _dict = dict(request._query_params)
    language = _dict.get('language')
    framework = _dict.get('framework')
    database = _dict.get('database')

    # Construct the query
    query = {'main_router':"comodules"}

    if language:
        query['language_name'] = {"$in": language.split(',')}
    if framework:
        query['framework_name'] = {"$in": framework.split(',')}
    if database:
        query['database_name'] = {"$in": database.split(',')}

    conditions = {}
    if query:
        conditions["$and"] = [query]

    try:
        comodules_list, pagination = await collection_comodule.getsbyconditionswithpagination(conditions,1,5)
        comodules_dict_list = [comodule.dict() for comodule in comodules_list]
        return {"comodules":comodules_dict_list, "total_records":pagination.total_records}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from app.utils.comodules import create_filename

import re
@router.get("/r/download/{comodule_id}")
@router.get("/download/{comodule_id}")
async def download_docker_files(request: Request, comodule_id: str):
    comodule = await collection_comodule.get(comodule_id)
    if comodule is None:
        raise HTTPException(status_code=404, detail="CoModule not found")

    zip_file_name = await create_filename(comodule)
    zip_path = os.path.join("app","resources", "downloads", zip_file_name)

    # 도커 파일들의 외부 링크 리스트
    docker_files_urls = await extract_splitlines_from_string(comodule.docker_files_links)
    async with httpx.AsyncClient() as client:
        # ZIP 파일 생성
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for url in docker_files_urls:
                # 파일 다운로드
                response = await client.get(url)
                file_name = url.split('/')[-1]  # URL에서 파일 이름 추출
                # 다운로드된 내용을 임시 파일로 저장
                with open(file_name, 'wb') as file:
                    file.write(response.content)
                # ZIP 파일에 추가
                zipf.write(file_name, file_name)
                # 임시 파일 삭제
                os.remove(file_name)
    
    user = request.state.user

    await update_comodule_approach(comodule_id, user)

    return FileResponse(path=zip_path
                        , filename=zip_file_name
                        , media_type='application/zip')

from datetime import datetime

async def update_comodule_approach(comodule_id, user):
    # 현재 시간을 "YYYY-MM-DD" 형식으로 포맷팅합니다.
    download_date = datetime.now().strftime("%Y%m%d%H%M%S")
    
    # 사용자 정보에서 user_id와 user_name을 추출합니다.
    user_id = user.get('id')
    user_name = user.get('name', 'wget')
    email = user.get('email')
    
    # comodule 컬렉션에서 comodule_id를 기준으로 문서를 찾고,
    # approach 필드에 새로운 항목을 추가합니다.
    await collection_comodule.update_withjson(
        comodule_id,
        {"$push": {
            "approach": {
                'download_date':download_date
                , 'user_id':user_id
                , 'user_name':user_name
                , 'email':email}}}
    )

async def is_activatebyuser(create_user_id, user):
    user_id = user.get('id')
    is_activate = False
    if create_user_id == user_id:
        is_activate = True
    return is_activate


