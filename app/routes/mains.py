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

@router.get("/list/{page_number}")
@router.get("/list") # 검색 with pagination
async def list(request: Request, page_number: Optional[int] = 1):
    context = await main_list(request, page_number)
    return templates.TemplateResponse(name="main.html"
                                      , context=context)

async def main_list(request: Request, page_number: Optional[int] = 1):
    _dict = dict(request._query_params)

    # 연관 관계 리스트
    # comodules_relative_list = await collection_comodule.aggregatebyconditions(conditions)
    comodules_unique_list = await unique_comodules()
    context={'request':request
            , 'comodules_unique' : comodules_unique_list
            # , 'user':user 
            }
    return context

from itertools import zip_longest
import re
from app.models.common_codes import CommonCode
collection_common_codes = Database(CommonCode)

async def unique_comodules():

    # Initialize sets for tracking uniqueness
    unique_frameworks = []
    unique_languages = []
    unique_database = []

    conditions = {'code_category':'comodules'}
    
    commoncode_list = await collection_common_codes.getsbyconditions(conditions)

    for item in commoncode_list:
        # framework_name 분리 및 추가
        if item.code_classification == 'Frameworks':
            unique_frameworks.append(item.name)
        
        # language_name 분리 및 추가
        if item.code_classification == 'Languages':
            unique_languages.append(item.name)
        
        # database_name 분리 및 추가
        if item.code_classification == 'Databases':
            unique_database.append(item.name)
    # Use itertools.zip_longest to combine lists with padding of None automatically
    combinations = [
        {'language': lang if lang is not None else '', 
        'framework': fw if fw is not None else '', 
        'database': db if db is not None else ''}  
        for lang, fw, db in zip_longest(set(unique_languages), set(unique_frameworks), set(unique_database))
    ]
    return combinations