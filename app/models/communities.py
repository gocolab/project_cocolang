from typing import Optional, List
from beanie import Document
from pydantic import BaseModel, HttpUrl, Field
from datetime import datetime

class Communities(Document):
    conversation_language: str = 'kr'
    title: str = None
    description: Optional[str] = None

    activity_type: str      # Code Review, Coding Test, Team Project
    needs_level: int = 0    # 참여 가능 최소 Level
    description_private: Optional[str] = None  # Only Read Members(소통 링크 등 모임 정보 공유)

    # 모집 기간
    recruitment_period_start: datetime = None
    recruitment_period_end: datetime = None
    # 모집 명수
    recruitment_number: int = None
    # 활동 기간
    activity_period_start: datetime = None
    activity_period_end: datetime = None
    # 공개 or 비공개 or 승인된 사람만 여부
    visibility: str = None  # "public", "private", "restricted"
    # 참여 회원별 신청 상황과 승인 여부, 메일 발송과 참여 여부 등
    # id, email, name, Authorizations in Community
    member_ids: Optional[List[str]] = None 

    create_date: datetime = Field(default_factory=datetime.now)
    create_user_id:Optional[str] = None
    create_user_name:Optional[str] = None
    refer_comodules_id: str       # from Comodules Doc

    class Settings:
        name = "communities"


