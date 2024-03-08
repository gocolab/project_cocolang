from fastapi import FastAPI, APIRouter, Request, HTTPException, status, Depends
from fastapi.templating import Jinja2Templates
from database.connection import Database  # Assume this handles your database connection
from models.comodules import CoModule  # This should be your CoModule model
from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional
from auth.authenticate import authenticate
from models.users import User

router = APIRouter(tags=["CoModules"])
templates = Jinja2Templates(directory="templates/")

# Assuming Database class and CoModule model are defined appropriately
collection_comodule = Database(CoModule)

@router.get("/form") 
async def form(request:Request):
    return templates.TemplateResponse(name="comodules/form.html"
                                      , context={'request':request})

# CRUD Operations
@router.post("/create")
async def create(request: Request):
    comodule_data = await request.form()
    comodule = CoModule(**comodule_data)
    await collection_comodule.save(comodule)
    return templates.TemplateResponse("comodules/list.html", {"request": request, "comodules": [comodule]})


@router.get("/list/{page_number}")
@router.get("/list") # 검색 with pagination
async def list(request: Request, page_number: Optional[int] = 1
               , user: str = Depends(authenticate)):
    _dict = dict(request._query_params)
    querys = []
    main_router = request.url.path.split('/')[1]
    querys.append({'main_router':main_router})
    try :
        search_word = _dict["word"].trim()
        if search_word :
            querys.append({_dict['key_name'] : { '$regex': search_word}})
    except:
        pass

    conditions = {'$and':querys}
    comodules_list, pagination = await collection_comodule.getsbyconditionswithpagination(conditions
                                                                     ,page_number)
    return templates.TemplateResponse(name="comodules/list.html"
                                      , context={'request':request
                                                 , 'comodules' : comodules_list
                                                  ,'pagination' : pagination
                                                   , 'main_router':main_router })
@router.get("/{comodule_id}")
async def read(request: Request, comodule_id: str):
    comodule = await collection_comodule.get(comodule_id)
    if comodule is None:
        raise HTTPException(status_code=404, detail="CoModule not found")
    return templates.TemplateResponse("comodules/read.html", {"request": request, "comodule": comodule})

@router.post("/update/{comodule_id}")
async def update(request: Request, comodule_id: str):
    comodule_data = await request.form()
    comodule = await collection_comodule.get(comodule_id)
    if comodule:
        updated_comodule = {**comodule.dict(), **comodule_data}
        await collection_comodule.save(updated_comodule)
        return templates.TemplateResponse("comodules/read.html", {"request": request, "comodule": updated_comodule})
    else:
        raise HTTPException(status_code=404, detail="CoModule not found")

@router.post("/delete/{comodule_id}")
async def delete(request: Request, comodule_id: str):
    await collection_comodule.delete(comodule_id)
    return templates.TemplateResponse("comodules/list.html", {"request": request})

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
    language = _dict['language']
    framework = _dict['framework']
    database = _dict['database']
    # Construct the query
    query = {}
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

@router.get("/download/{comodule_id}")
async def download_docker_files(request: Request, comodule_id: str):
    comodule = await collection_comodule.get(comodule_id)
    if comodule is None:
        raise HTTPException(status_code=404, detail="CoModule not found")

    # 도커 파일들의 외부 링크 리스트
    # docker_files_urls = [
    #     "https://raw.githubusercontent.com/gocolab/project_cocolabhub/main/docksers/Dockerfile",
    #     "https://raw.githubusercontent.com/gocolab/project_cocolabhub/main/docksers/docker-compose.yml"
    # ]
    docker_files_urls = comodule.docker_files_links
    zip_file_name = f"dockers_{comodule_id}.zip"
    zip_path = os.path.join("resources", "downloads", zip_file_name)

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
    
    return FileResponse(path=zip_path, filename="dockers.zip", media_type='application/zip')
