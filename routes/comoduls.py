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

# CRUD Operations
@router.post("/comodules/create")
async def create_comodule(request: Request):
    comodule_data = await request.form()
    comodule = CoModule(**comodule_data)
    await collection_comodule.save(comodule)
    return templates.TemplateResponse("comodules/list.html", {"request": request, "comodules": [comodule]})

@router.get("/comodules/")
async def list_comodules(request: Request):
    comodules = await collection_comodule.find_all().to_list()
    return templates.TemplateResponse("comodules/list.html", {"request": request, "comodules": comodules})

@router.get("/comodules/{comodule_id}")
async def read_comodule(request: Request, comodule_id: str):
    comodule = await collection_comodule.get(comodule_id)
    if comodule is None:
        raise HTTPException(status_code=404, detail="CoModule not found")
    return templates.TemplateResponse("comodules/read.html", {"request": request, "comodule": comodule})

@router.post("/comodules/update/{comodule_id}")
async def update_comodule(request: Request, comodule_id: str):
    comodule_data = await request.form()
    comodule = await collection_comodule.get(comodule_id)
    if comodule:
        updated_comodule = {**comodule.dict(), **comodule_data}
        await collection_comodule.save(updated_comodule)
        return templates.TemplateResponse("comodules/read.html", {"request": request, "comodule": updated_comodule})
    else:
        raise HTTPException(status_code=404, detail="CoModule not found")

@router.post("/comodules/delete/{comodule_id}")
async def delete_comodule(request: Request, comodule_id: str):
    await collection_comodule.delete(comodule_id)
    return templates.TemplateResponse("comodules/list.html", {"request": request})
