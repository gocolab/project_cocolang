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
    conditions = {'main_router':'comodules'}

    main_router = request.url.path.split('/')[1]
    try :
        conditions[_dict['key_name']] = {'$regex': _dict["word"] }
    except:
        pass

    comodules_list, pagination = await collection_comodule.getsbyconditionswithpagination(conditions
                                                                     ,page_number
                                                                     ,5)
    comodule = {}
    if comodules_list:
        comodule = await collection_comodule.get(comodules_list[0].id)

    conditions = [
        {
            "$match": {
                "main_router": "comodules" 
            }
        },
        {
            "$group": {
                "_id": {
                    "framework_name": "$framework_name",
                    "language_name": "$language_name",
                    "database_name": "$database_name"
                },
                "framework_name": {"$first": "$framework_name"},
                "language_name": {"$first": "$language_name"},
                "database_name": {"$first": "$database_name"}
            }
        },
        {
            "$project": {
                "_id": 0,
                "framework_name": 1,
                "language_name": 1,
                "database_name": 1
            }
        }
    ]
    # 연관 관계 리스트
    comodules_relative_list = await collection_comodule.aggregatebyconditions(conditions)
    comodules_unique_list = await unique_comodules(comodules_relative_list)
    context={'request':request
            , 'comodule' : comodule
            , 'comodules' : comodules_list
            , 'comodules_relative' : comodules_relative_list
            , 'comodules_unique' : comodules_unique_list
            ,'pagination' : pagination
            , 'main_router':main_router
            # , 'user':user 
            }
    return context

from itertools import zip_longest
import re
async def unique_comodules(original_list):

    # Initialize sets for tracking uniqueness
    unique_frameworks = set()
    unique_languages = set()
    unique_database = set()

    for item in original_list:
        # framework_name 분리 및 추가
        if item['framework_name'] != 'null' and item['framework_name'].strip() != '':
            unique_frameworks.update(re.split(r' +', item['framework_name']))
        
        # language_name 분리 및 추가
        if item['language_name'] != 'null' and item['language_name'].strip() != '':
            unique_languages.update(re.split(r' +', item['language_name']))
        
        # database_name 분리 및 추가
        if item['database_name'] != 'null' and item['database_name'].strip() != '':
            unique_database.update(re.split(r' +', item['database_name']))
    # Use itertools.zip_longest to combine lists with padding of None automatically
    combinations = [
        {'language': lang if lang is not None else '', 
        'framework': fw if fw is not None else '', 
        'database': db if db is not None else ''}  
        for lang, fw, db in zip_longest(unique_languages, unique_frameworks, unique_database)
    ]
    return combinations