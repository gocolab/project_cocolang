from typing import Optional, List
from beanie import Document
from pydantic import BaseModel, HttpUrl

class CoModule(Document):
    title: Optional[str] = None
    description: Optional[str] = None
    language_id: Optional[str] = None
    framework_id: Optional[str] = None
    databases_id: Optional[str] = None
    language_name: Optional[str] = None
    framework_name: Optional[str] = None
    databases_name: Optional[str] = None
    docker_files_links: List[str] = []
    required_packages_versions: List[str] = None

    class Settings:
        name = "comodules"

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Sample CoModule",
                "language_id": "Python",
                "framework_id": "FastAPI",
                "databases_id": "MongoDB",
                # "docker_files_links": ["http://example.com/dockerfile"],
                # "required_packages_versions": ["fastapi==0.65.0", "uvicorn==0.14.0"]
            }
        }
