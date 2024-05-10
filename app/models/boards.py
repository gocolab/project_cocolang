from typing import Optional, List
from beanie import Document
from pydantic import BaseModel, HttpUrl, Field
from datetime import datetime

class Boards(Document):
    title: str = None
    description: Optional[str] = None
    order_number: int
        
    create_date: datetime = Field(default_factory=datetime.now)
    create_user_id:Optional[str] = None
    create_user_name:Optional[str] = None
    
    parent_id: str       # implement recursive loop with comments
    # 메뉴에 생성되지 않은 _id 적용 방안 고려 필요
    refer_kind_id: Optional[str] = None    # to use other model or model
    refer_kind_name: Optional[str] = None    

    class Settings:
        name = "boards"


