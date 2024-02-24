from fastapi import FastAPI, APIRouter, Request, HTTPException, status, Depends
from fastapi.templating import Jinja2Templates
from database.connection import Database  # Assume this handles your database connection
from models.comodules import CoModule  # This should be your CoModule model
from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional

router = APIRouter(tags=["CoModules"])
templates = Jinja2Templates(directory="templates/")

# Assuming Database class and CoModule model are defined appropriately
collection_comodule = Database(CoModule)

@router.get("/form") 
async def form(request:Request):
    # print(dict(request._query_params))
    return templates.TemplateResponse(name="comodules/form.html"
                                      , context={'request':request})

# CRUD Operations
@router.post("/create")
async def create_comodule(request: Request):
    comodule_data = await request.form()
    comodule = CoModule(**comodule_data)
    await collection_comodule.save(comodule)
    return templates.TemplateResponse("comodules/list.html", {"request": request, "comodules": [comodule]})

@router.get("/list/{page_number}")
@router.get("/list") # 검색 with pagination
async def list_comodules(request: Request, page_number: Optional[int] = 1):
    _dict = dict(request._query_params)
    conditions = { }

    try :
        conditions = {_dict['key_name'] : { '$regex': _dict["word"] }}
    except:
        pass

    comodules_list, pagination = await collection_comodule.getsbyconditionswithpagination(conditions
                                                                     ,page_number)
    return templates.TemplateResponse(name="comodules/list.html"
                                      , context={'request':request
                                                 , 'comodules' : comodules_list
                                                  ,'pagination' : pagination })

@router.get("/{comodule_id}")
async def read_comodule(request: Request, comodule_id: str):
    comodule = await collection_comodule.get(comodule_id)
    if comodule is None:
        raise HTTPException(status_code=404, detail="CoModule not found")
    return templates.TemplateResponse("comodules/read.html", {"request": request, "comodule": comodule})

@router.post("/update/{comodule_id}")
async def update_comodule(request: Request, comodule_id: str):
    comodule_data = await request.form()
    comodule = await collection_comodule.get(comodule_id)
    if comodule:
        updated_comodule = {**comodule.dict(), **comodule_data}
        await collection_comodule.save(updated_comodule)
        return templates.TemplateResponse("comodules/read.html", {"request": request, "comodule": updated_comodule})
    else:
        raise HTTPException(status_code=404, detail="CoModule not found")

@router.post("/delete/{comodule_id}")
async def delete_comodule(request: Request, comodule_id: str):
    await collection_comodule.delete(comodule_id)
    return templates.TemplateResponse("comodules/list.html", {"request": request})
