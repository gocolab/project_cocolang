from typing import Optional, List
from beanie import Document
from pydantic import BaseModel, HttpUrl, Field
from datetime import datetime

class CoModule(Document):
    main_router: str
    title: str = None
    language_name: Optional[str] = None
    framework_name: Optional[str] = None
    database_name: Optional[str] = None
    docker_files_links: str
    required_packages_versions: Optional[str] = None
    description: Optional[str] = None
    create_date: datetime = Field(default_factory=datetime.now)
    create_user_id:Optional[str] = None
    create_user_name:Optional[str] = None
    level: int = 0
    # 공개 or 비공개 or 승인된 사람만 여부
    visibility: str = None  # "public", "private", "restricted"

    class Settings:
        name = "comodules"

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Sample CoModule",
                "language_id": "Python",
                "framework_id": "FastAPI",
                "database_id": "MongoDB",
                # "docker_files_links": ["http://example.com/dockerfile"],
                # "required_packages_versions": ["fastapi==0.65.0", "uvicorn==0.14.0"]
            }
        }
