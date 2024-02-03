from typing import List

from beanie import PydanticObjectId
from database.connection import Database
from fastapi import APIRouter, Depends, HTTPException, status
from models.events import Event, EventUpdate

router = APIRouter(
    tags=["Events"]
)

event_database = Database(Event)

# 전체 내용 가져오기
@router.get("/", response_model=List[Event])
async def retrieve_all_events() -> List[Event]:
    events = await event_database.get_all()
    return events

# id 기준 한 row 확인
@router.get("/{id}", response_model=Event)
async def retrieve_event(id: PydanticObjectId) -> Event:
    event = await event_database.get(id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist"
        )
    return event

# 새로운 레코드 추가
# http://127.0.0.1:8000/events_api/new
# {
#         "creator": "박지민",
#         "title": "가을 속으로",
#         "image": "autumn_leaves.jpg",
#         "description": "가을이 깊어가는 숲속의 오색찬란한 단풍",
#         "tags": ["가을", "단풍", "자연", "숲"],
#         "location": "내장산, 전라북도"
#     }
@router.post("/new")
async def create_event(body: Event) -> dict:
    document = await event_database.save(body)
    return {
        "message": "Event created successfully"
        ,"datas": document
    }


@router.put("/{id}", response_model=Event)
async def update_event(id: PydanticObjectId, body: EventUpdate) -> Event:
    event = await event_database.get(id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    updated_event = await event_database.update(id, body)
    if not updated_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist"
        )
    return updated_event

# update with json by id 
from fastapi import Request
@router.put("/json/{id}", response_model=Event)
async def update_event_withjson(id: PydanticObjectId, request:Request) -> Event:
    event = await event_database.get(id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    body = await request.json()
    updated_event = await event_database.update_withjson(id, body)
    if not updated_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist"
        )
    return updated_event

# ID에 따른 row 삭제
@router.delete("/{id}")
async def delete_event(id: PydanticObjectId) -> dict:
    event = await event_database.get(id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    event = await event_database.delete(id)

    return {
        "message": "Event deleted successfully."
        ,"datas": event
    }
