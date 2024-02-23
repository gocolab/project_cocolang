from typing import Optional
from beanie import Document

class CommonCode(Document):
    code_category: Optional[str] = None
    code_classification: Optional[str] = None
    order: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None

    class Settings:
        name = "CommonCodes"

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
