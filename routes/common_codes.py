from auth.hash_password import HashPassword
from database.connection import Database
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter(
    tags=["CommonCodes"],
)

from fastapi.templating import Jinja2Templates
from fastapi import Request

templates = Jinja2Templates(directory="templates/")

from database.connection import Database
from models.common_codes import CommonCode
collection_user = Database(CommonCode)

@router.post("/", response_model=CommonCodeInDB)
async def create_common_code(common_code: CommonCodeCreate):
    common_code_doc = CommonCode(**common_code.dict())
    await common_code_doc.insert()
    return common_code_doc

@router.get("/{code_id}", response_model=CommonCodeInDB)
async def get_common_code(code_id: PydanticObjectId):
    common_code = await CommonCode.get(code_id)
    if not common_code:
        raise HTTPException(status_code=404, detail="CommonCode not found")
    return common_code

@router.put("/{code_id}", response_model=CommonCodeInDB)
async def update_common_code(code_id: PydanticObjectId, common_code: CommonCodeUpdate):
    common_code_doc = await CommonCode.get(code_id)
    if not common_code_doc:
        raise HTTPException(status_code=404, detail="CommonCode not found")
    update_data = common_code.dict(exclude_unset=True)
    await common_code_doc.set(update_data)
    return common_code_doc

@router.delete("/{code_id}")
async def delete_common_code(code_id: PydanticObjectId):
    common_code_doc = await CommonCode.get(code_id)
    if not common_code_doc:
        raise HTTPException(status_code=404, detail="CommonCode not found")
    await common_code_doc.delete()
    return {"message": "CommonCode deleted successfully"}
