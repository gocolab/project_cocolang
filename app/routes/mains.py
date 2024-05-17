from fastapi import FastAPI, APIRouter, Request, HTTPException, status, Depends
from fastapi.templating import Jinja2Templates
from app.database.connection import Database  # Assume this handles your database connection
from app.models.comodules import CoModule  # This should be your CoModule model
from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional
from app.auth.authenticate import authenticate
from app.models.users import User
from app.utils.comodules import unique_comodules

router = APIRouter(tags=["CoModules"])
templates = Jinja2Templates(directory="app/templates/")

# Assuming Database class and CoModule model are defined appropriately
collection_comodule = Database(CoModule)

@router.get("/list/{page_number}")
@router.get("/list") # 검색 with pagination
async def list(request: Request, page_number: Optional[int] = 1):
    context = await main_list(request, page_number)
    return templates.TemplateResponse(name="main.html"
                                      , context=context)

async def main_list(request: Request, page_number: Optional[int] = 1):
    _dict = dict(request._query_params)
    # conditions = {'main_router':'comodules'}
    conditions = {}

    try :
        conditions[_dict['key_name']] = {'$regex': _dict["word"] }
    except:
        pass

    comodules_list, pagination = await collection_comodule.getsbyconditionswithpagination(conditions
                                                                     ,page_number
                                                                     ,5)
    comodule = {}
    if comodules_list:
        comodule = comodules_list[0]

   # 연관 관계 리스트
    comodules_unique_list = await unique_comodules()
    context={'request':request
            , 'comodule' : comodule
            , 'comodules' : comodules_list
            , 'comodules_unique' : comodules_unique_list
            , 'pagination' : pagination
            }
    return context
