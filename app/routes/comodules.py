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
async def form(request:Request):
    main_router = request.url.path.split('/')[1]

    return templates.TemplateResponse(name="comodules/form.html"
                                      , context={'request':request
                                                 ,'main_router':main_router})

async def extract_splitlines_from_string(input_str: str):
    # 문자열을 줄바꿈 기준으로 분리
    lines = input_str.splitlines()
    
    # 빈 문자열을 제외하고 유효한 URL만을 리스트에 추가
    list_input = [line.strip() for line in lines if line.strip()]
    
    return list_input

from app.auth.authenticate import userfromauthenticate
# CRUD Operations
@router.post("/insert")
async def create(request: Request):
    comodule_data = dict(await request.form())
    user = await userfromauthenticate(request)
    comodule_data["create_user_id"] = user['name']
    comodule_data["create_user_name"] = user['id']
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
async def read(request: Request, comodule_id: str):
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
    
    comodule_data = await request.form()
    comodule = await collection_comodule.get(comodule_id)
    if comodule:
        updated_comodule = {**comodule.dict(), **comodule_data}
        await collection_comodule.save(updated_comodule)
        return templates.TemplateResponse("comodules/read.html"
                                          , {"request": request, "comodule": updated_comodule})
    else:
        raise HTTPException(status_code=404, detail="CoModule not found")

@router.post("/{comodule_id}")
async def delete(request: Request, comodule_id: str):
    result_id = await collection_comodule.delete(comodule_id)
    context = await comodules_list(request, 1)
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

async def format_comodule_details(comodule):
    """
    Formats the details of a comodule object into a string.

    Parameters:
    - comodule: An object with the following attributes:
        - language_name
        - language_version
        - framework_name
        - framework_version
        - database_name
        - database_version

    Returns:
    - A string that contains the formatted details.
    """
    # 각 컴포넌트의 이름과 버전을 조합합니다. 버전 정보가 없는 경우 이름만 사용합니다.
    language_details = f"{comodule.language_name}"
    framework_details = f"{comodule.framework_name}"
    database_details = f"{comodule.database_name}"
    # 모든 컴포넌트의 상세 정보를 하나의 문자열로 결합합니다.
    return f"{language_details}_{framework_details}_{database_details}"

from datetime import datetime
@router.get("/download/{comodule_id}")
async def download_docker_files(request: Request, comodule_id: str):
    comodule = await collection_comodule.get(comodule_id)
    if comodule is None:
        raise HTTPException(status_code=404, detail="CoModule not found")

    comodule_str = await format_comodule_details(comodule)
    # 현재 시간을 "YYYYMMDD_HHMMSS" 포맷으로 변환
    file_suffix = datetime.now().strftime("%Y%m%d")
    zip_file_name = f"dockers_{comodule_str}_{file_suffix}.zip"
    zip_path = os.path.join("app","resources", "downloads", zip_file_name)

    # 도커 파일들의 외부 링크 리스트
    # docker_files_urls = [
    #     "https://raw.githubusercontent.com/gocolab/project_cocolabhub/main/docksers/Dockerfile",
    #     "https://raw.githubusercontent.com/gocolab/project_cocolabhub/main/docksers/docker-compose.yml"
    # ]
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
    
    user = await userfromauthenticate(request)

    await update_comodule_approach(comodule_id, user)

    return FileResponse(path=zip_path, filename=zip_file_name, media_type='application/zip')

async def update_comodule_approach(comodule_id, user):
    # 현재 시간을 "YYYY-MM-DD" 형식으로 포맷팅합니다.
    download_date = datetime.now().strftime("%Y%m%d%H%M%S")
    
    # 사용자 정보에서 user_id와 user_name을 추출합니다.
    # user 객체의 구조에 따라 접근 방식이 달라질 수 있습니다.
    user_id = user.get('id')
    user_name = user.get('name')
    
    # comodule 컬렉션에서 comodule_id를 기준으로 문서를 찾고,
    # approach 필드에 새로운 항목을 추가합니다.
    await collection_comodule.update_withjson(
        comodule_id,
        {"$push": {
            "approach": {
                'download_date':download_date
                , 'user_id':user_id
                , 'user_name':user_name}}}
    )