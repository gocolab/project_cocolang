from typing import Any, List, Optional

from beanie import init_beanie, PydanticObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from pydantic_settings import BaseSettings


from models.users import User
from models.common_codes import CommonCode
from models.comodules import CoModule

class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = None
    SECRET_KEY: Optional[str] = None
    ALGORITHM: Optional[str] = None
    ACCESS_TOKEN_EXPIRE_MINUTES: Optional[str] = None


    async def initialize_database(self):
        client = AsyncIOMotorClient(self.DATABASE_URL)
        await init_beanie(database=client.get_default_database(), 
        document_models=[User, CommonCode, CoModule])

    class Config:
        env_file = ".env"

from utils.paginations import Paginations

import json
class Database:
    def __init__(self, model):
        self.model = model

    async def save(self, document):
        result = await document.create()
        return result

    async def get(self, id: PydanticObjectId):
        doc = await self.model.get(id)
        if doc:
            return doc
        return False

    async def get_all(self):
        docs = await self.model.find_all().to_list()
        return docs

    # update with params json
    async def update_withjson(self, id: PydanticObjectId, body: json):
        doc_id = id

        # des_body = {k: v for k, v in des_body.items() if v is not None}
        update_query = {"$set": {**body}}

        doc = await self.get(doc_id)
        if not doc:
            return False
        await doc.update(update_query)
        return doc
    
    async def update(self, id: PydanticObjectId, body: BaseModel):
        doc_id = id
        des_body = body.dict()

        des_body = {k: v for k, v in des_body.items() if v is not None}
        update_query = {"$set": {
            field: value for field, value in des_body.items()
        }}

        doc = await self.get(doc_id)
        if not doc:
            return False
        await doc.update(update_query)
        return doc

    async def delete(self, id: PydanticObjectId):
        doc = await self.get(id)
        if not doc:
            return False
        await doc.delete()
        return True

    # column 값으로 여러 Documents 가져오기
    async def getsbyconditions(self, conditions:dict) -> [Any]:
        documents = await self.model.find(conditions).to_list()  # find({})
        if documents:
            return documents
        return False    

    # column 값으로 aggregate해 여러 Documents 가져오기
    async def aggregatebyconditions(self, conditions:dict) -> [Any]:
        documents = await self.model.aggregate(conditions).to_list()  # find({})
        if documents:
            return documents
        return False    

    # column 값으로 여러 Documents with pagination 가져오기
    async def getsbyconditionswithpagination(self
                                             , conditions:dict, page_number
                                             , records_per_page=10, pages_per_block=5
                                             , sorted = -1
                                             , sort_field:str = 'create_date') -> [Any]:
        # find({})
        try:
            total = await self.model.find(conditions).count()
        except:
            total = 0
        pagination = Paginations(total_records=total, current_page=page_number
                                 , records_per_page=records_per_page
                                 , pages_per_block=pages_per_block)
        documents = await self.model.find(conditions).sort(f'-{sort_field}').skip(pagination.start_record_number).limit(pagination.records_per_page).to_list()
        if documents:
            return documents, pagination
        return False    


if __name__ == '__main__':
    settings = Settings()
    async def init_db():
        await settings.initialize_database()

    collection_user = Database(User)
    conditions = "{ name: { $regex: '이' } }"
    list = collection_user.getsbyconditions(conditions)
    pass