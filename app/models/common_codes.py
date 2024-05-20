from typing import Optional
from beanie import Document
from pydantic import BaseModel, HttpUrl, Field
from datetime import datetime
class CommonCode(Document):
    code_category: Optional[str] = None
    code_classification: Optional[str] = None
    order: Optional[int] = 1
    name: Optional[str] = None
    description: Optional[str] = None
    conformed: Optional[bool] = False   # 외부 의한 입력 시 사용 여부 판단 후 사용
    create_date: datetime = Field(default_factory=datetime.now)
    create_user_id:Optional[str] = None
    create_user_name:Optional[str] = None

    class Settings:
        name = "common_codes"

    class Config:
        json_schema_extra = {
            "example": {
                "code_category": "comodules",
                "code_classification": "Languages",
                "order": 1,
                "name": "Python",
                "description": "고급 프로그래밍 언어로, 명료성과 가독성을 강조하며 다양한 분야에 활용됩니다."
            }
        }
