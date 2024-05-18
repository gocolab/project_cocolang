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
async def main(request: Request, page_number: Optional[int] = 1):
    context = await main_list(request, page_number)
    return templates.TemplateResponse(name="comodules/main.html"
                                      , context=context)

from app.routes.comodules import main_conditions
async def main_list(request: Request, page_number: Optional[int] = 1):
   # 연관 관계 리스트
    comodules_unique_list = await unique_comodules()
    context={'request':request
            , 'comodules_unique' : comodules_unique_list
            }
    return context
