from fastapi import APIRouter, Request, HTTPException
from typing import Optional
from app.models.communities import Communities  # Communities 모델 import 가정
from app.database.connection import Database  # Database 클래스 import 가정
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["Communities"])
templates = Jinja2Templates(directory="app/templates/")

# Database 클래스와 Communities 모델을 적절히 정의했다고 가정
collection_communities = Database(Communities)

@router.get("/form")
@router.get("/update/{community_id}")
async def form(request: Request, community_id: str = None):
    community = {}
    if community_id is not None:
        community = await collection_communities.get(community_id)
        if community is None:
            raise HTTPException(status_code=404, detail="Community not found")

    return templates.TemplateResponse(name="communities/form.html",
                                      context={'request': request,
                                               'community': community})

@router.post("/insert")
async def create(request: Request):
    community_data = dict(await request.form())
    user = request.state.user  # userfromauthenticate 구현 가정
    community_data["create_user_id"] = user['id']
    community_data["create_user_name"] = user['name']

    community = Communities(**community_data)
    result_id = await collection_communities.save(community)

    context = await communities_list(request, 1)
    return templates.TemplateResponse("communities/list.html", context=context)

@router.get("/list/{page_number}")
@router.get("/list")  # 검색 with pagination
async def list(request: Request, page_number: Optional[int] = 1):
    context = await communities_list(request, page_number)
    return templates.TemplateResponse(name="communities/list.html", context=context)

async def communities_list(request: Request, page_number: Optional[int] = 1):
    _dict = dict(request.query_params)
    queries = []
    try:
        search_word = _dict["word"].strip()
        if search_word:
            queries.append({_dict['key_name']: {'$regex': search_word}})
    except:
        pass

    # queries 배열이 비어있는 경우, 모든 문서를 매칭시키는 조건을 사용합니다.
    if queries:
        conditions = {'$and': queries}
    else:
        conditions = {}

    communities_list, pagination = await collection_communities.getsbyconditionswithpagination(conditions, page_number)
    context = {'request': request, 'communities': communities_list, 'pagination': pagination}
    return context

@router.get("/{community_id}")
async def read(request: Request, community_id: str = None):
    community = await collection_communities.get(community_id)
    if community is None:
        raise HTTPException(status_code=404, detail="Community not found")

    return templates.TemplateResponse("communities/read.html",
                                      {"request": request,
                                       "community": community})

@router.post("/update/{community_id}")
async def update(request: Request, community_id: str):
    community = await collection_communities.get(community_id)
    if community:
        community_data = dict(await request.form())
        _model = Communities(**community_data)
        result = await collection_communities.update(community_id, _model)
        context = await communities_list(request)
        return templates.TemplateResponse("communities/list.html", context=context)
    else:
        raise HTTPException(status_code=404, detail="Community not found")

@router.post("/{community_id}")
async def delete(request: Request, community_id: str):
    result_id = await collection_communities.delete(community_id)
    context = await communities_list(request)
    return templates.TemplateResponse(name="communities/list.html"
                                      , context=context)