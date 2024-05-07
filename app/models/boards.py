from typing import Optional, List
from beanie import Document
from pydantic import BaseModel, HttpUrl, Field
from datetime import datetime

class Boards(Document):
    # 메뉴에 생성되지 않은 _id 적용 방안 고려 필요
    title: str = None
    description: Optional[str] = None
    order_number: int
        
    create_date: datetime = Field(default_factory=datetime.now)
    create_user_id:Optional[str] = None
    create_user_name:Optional[str] = None
    parent_id: str       # 상위 글 id
    refer_model_id: Optional[str] = None    # 다른 model에 사용하는 게시글

    class Settings:
        name = "boards"


