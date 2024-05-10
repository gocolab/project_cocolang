from fastapi import APIRouter, Request, HTTPException
from typing import Optional
from app.models.boards import Boards  # Boards 모델 import
from app.database.connection import Database  # Database 클래스 import 가정
from fastapi.templating import Jinja2Templates
from datetime import datetime

router = APIRouter(tags=["Boards"])
templates = Jinja2Templates(directory="app/templates/")

# Database 클래스와 Boards 모델을 적절히 정의했다고 가정
collection_boards = Database(Boards)

@router.get("/form")
@router.get("/update/{board_id}")
async def form(request: Request, board_id: str = None):
    main_router = request.url.path.split('/')[1]

    board = {}
    if board_id is not None:
        board = await collection_boards.get(board_id)
        if board is None:
            raise HTTPException(status_code=404, detail="Board not found")

    return templates.TemplateResponse(name="boards/form.html",
                                      context={'request': request,
                                               'board': board,
                                               'main_router': main_router})

@router.post("/insert")
async def create(request: Request):
    board_data = dict(await request.form())
    user = request.state.user  # userfromauthenticate 구현 가정
    board_data["create_user_id"] = user['id']
    board_data["create_user_name"] = user['name']
    main_router = request.url.path.split('/')[1]
    board_data["main_router"] = main_router

    board = Boards(**board_data)
    result_id = await collection_boards.save(board)

    context = await boards_list(request, 1)
    return templates.TemplateResponse("boards/list.html", context=context)

@router.get("/list/{page_number}")
@router.get("/list")  # 검색 with pagination
async def list(request: Request, page_number: Optional[int] = 1):
    context = await boards_list(request, page_number)
    return templates.TemplateResponse(name="boards/list.html", context=context)

async def boards_list(request: Request, page_number: Optional[int] = 1):
    _dict = dict(request.query_params)
    queries = []
    main_router = request.url.path.split('/')[1]
    # queries.append({'main_router': main_router})
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
    
    boards_list, pagination = await collection_boards.getsbyconditionswithpagination(conditions, page_number)
    context = {'request': request, 'boards': boards_list, 'pagination': pagination, 'main_router': main_router}
    return context

@router.get("/{board_id}")
async def read(request: Request, board_id: str = None):
    main_router = request.url.path.split('/')[1]

    board = await collection_boards.get(board_id)
    if board is None:
        raise HTTPException(status_code=404, detail="Board not found")

    return templates.TemplateResponse("boards/read.html",
                                      {"request": request,
                                       "board": board,
                                       'main_router': main_router})

@router.post("/update/{board_id}")
async def update(request: Request, board_id: str):
    board = await collection_boards.get(board_id)
    if board:
        board_data = dict(await request.form())
        _model = Boards(**board_data)
        result = await collection_boards.update(board_id, _model)
        context = await boards_list(request)
        return templates.TemplateResponse("boards/list.html", context=context)
    else:
        raise HTTPException(status_code=404, detail="Board not found")

@router.post("/{board_id}")
async def delete(request: Request, board_id: str):
    result_id = await collection_boards.delete(board_id)
    context = await boards_list(request)
    return templates.TemplateResponse(name="boards/list.html", context=context)
