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

@router.get("/list/{page_number}")
@router.get("/list") # 검색 with pagination
async def list(request: Request, page_number: Optional[int] = 1):
    _dict = dict(request._query_params)
    conditions = { }

    try :
        conditions = {_dict['key_name'] : { '$regex': _dict["word"] }}
    except:
        pass

    comodules_list, pagination = await collection_comodule.getsbyconditionswithpagination(conditions
                                                                     ,page_number
                                                                     ,5)
    comodule = await collection_comodule.get(comodules_list[0].id)
    
    conditions = [
        {
            "$group": {
                "_id": {
                    "framework_name": "$framework_name",
                    "language_name": "$language_name",
                    "databases_name": "$databases_name"
                },
                "framework_name": {"$first": "$framework_name"},
                "language_name": {"$first": "$language_name"},
                "databases_name": {"$first": "$databases_name"}
            }
        },
        {
            "$project": {
                "_id": 0,
                "framework_name": 1,
                "language_name": 1,
                "databases_name": 1
            }
        }
    ]
    # 연관 관계 리스트
    comodules_relative_list = await collection_comodule.aggregatebyconditions(conditions)
    comodules_unique_list = await unique_comodules(comodules_relative_list)
    return templates.TemplateResponse(name="main.html"
                                      , context={'request':request
                                                 , 'comodule' : comodule
                                                 , 'comodules' : comodules_list
                                                 , 'comodules_relative' : comodules_relative_list
                                                 , 'comodules_unique' : comodules_unique_list
                                                  ,'pagination' : pagination })

from itertools import zip_longest
async def unique_comodules(original_list):

    # Initialize sets for tracking uniqueness
    unique_frameworks = {item['framework_name'] for item in original_list}
    unique_languages = {item['language_name'] for item in original_list}
    unique_databases = {item['databases_name'] for item in original_list}

    # Use itertools.zip_longest to combine lists with padding of None automatically
    combinations = [
        {'language': lang if lang is not None else '', 
        'framework': fw if fw is not None else '', 
        'databases': db if db is not None else ''}  
        for lang, fw, db in zip_longest(unique_languages, unique_frameworks, unique_databases)
    ]
    return combinations