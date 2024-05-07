from typing import Optional, List
from beanie import Document
from pydantic import BaseModel, HttpUrl, Field
from datetime import datetime

class Communities(Document):
    conversation_language: str = 'kr'
    title: str = None
    activity_type: str      # Code Review, Coding Test, Team Project
    description: Optional[str] = None
    needs_level: int = 0    # 참여 가능 최소 Level
    description_private: Optional[str] = None  # Only Read Members(소통 링크 등 모임 관련 공유)

    # 모집 기간
    # 활동 기간
    # 공개 or 비공개 or 승인된 사람만 여부
    # 참여 회원별 신청 상황과 승인 여부, 메일 발송과 참여 여부 등
    member_ids: Optional[List]
        
    create_date: datetime = Field(default_factory=datetime.now)
    create_user_id:Optional[str] = None
    create_user_name:Optional[str] = None
    comodules_id: str       # from Comodules Doc

    class Settings:
        name = "communities"


