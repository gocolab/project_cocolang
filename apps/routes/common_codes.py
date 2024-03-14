from apps.database.connection import Database
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter(
    tags=["CommonCodes"],
)

from fastapi.templating import Jinja2Templates
from fastapi import Request
from beanie import PydanticObjectId


templates = Jinja2Templates(directory="templates/")

from apps.database.connection import Database
from apps.models.common_codes import CommonCode
collection_CommonCode = Database(CommonCode)

@router.post("/")
async def create_common_code(request:Request):
    _dict = dict(await request.form())
    # 저장
    _model = CommonCode(**_dict)

    await _model.insert()
    return templates.TemplateResponse(name="/commoncodes/list.html"
                        , context={'request':request})

@router.get("/{object_id}")
async def get_common_code(object_id: PydanticObjectId):
    common_code = await CommonCode.get(object_id)
    if not common_code:
        raise HTTPException(status_code=404, detail="CommonCode not found")
    return common_code

@router.put("/{object_id}")
async def update_common_code(object_id: PydanticObjectId, request:Request):
    _dict = dict(await request.form())
    # 저장
    _model = CommonCode(**_dict)
    common_code_doc = await CommonCode.get(object_id)
    if not common_code_doc:
        raise HTTPException(status_code=404, detail="CommonCode not found")
    # update_data = _model.dict(exclude_unset=True)
    await common_code_doc.set(_model)
    return common_code_doc

@router.delete("/{object_id}")
async def delete_common_code(object_id: PydanticObjectId):
    common_code_doc = await CommonCode.get(object_id)
    if not common_code_doc:
        raise HTTPException(status_code=404, detail="CommonCode not found")
    await common_code_doc.delete()
    return {"message": "CommonCode deleted successfully"}
