from auth.hash_password import HashPassword
from auth.jwt_handler import create_access_token
from database.connection import Database
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from models.users import User, TokenResponse

router = APIRouter(
    tags=["User"],
)

user_database = Database(User)
hash_password = HashPassword()


@router.post("/signup")
async def sign_user_up(user: User) -> dict:
    user_exist = await User.find_one(User.email == user.email)

    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with email provided exists already."
        )
    hashed_password = hash_password.create_hash(user.password)
    user.password = hashed_password
    await user_database.save(user)
    return {
        "message": "User created successfully"
    }

@router.post("/signin", response_model=TokenResponse)
async def sign_user_in(user: OAuth2PasswordRequestForm = Depends()) -> dict:
    user_exist = await User.find_one(User.email == user.username)
    if not user_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with email does not exist."
        )
    if hash_password.verify_hash(user.password, user_exist.password):
        access_token = create_access_token(user_exist.email)
        return {
            "access_token": access_token,
            "token_type": "Bearer"
        }

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid details passed."
    )

from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request

templates = Jinja2Templates(directory="templates/")

@router.get("/form") # 펑션 호출 방식
async def insert(request:Request):
    print(dict(request._query_params))
    return templates.TemplateResponse(name="users/inserts.html"
                                      , context={'request':request
                                                 , 'first': 5, 'second':6})

@router.post("/login", response_class=HTMLResponse) # 펑션 호출 방식
async def insert(request:Request):
    form_data = await request.form()
    dict_form_data = dict(form_data)
    print(dict_form_data)
    return templates.TemplateResponse(name="users/login.html"
                                      , context={'request':request
                                                 , 'form_data' : dict_form_data
                                                 , 'first' : 'text'})

@router.post("/login", response_class=HTMLResponse) # 펑션 호출 방식
async def insert(request:Request):
    form_data = await request.form()
    dict_form_data = dict(form_data)
    print(dict_form_data)
    return templates.TemplateResponse(name="users/login.html"
                                      , context={'request':request
                                                 , 'form_data' : dict_form_data
                                                 , 'first' : 'text'})

@router.get("/login", response_class=HTMLResponse) # 펑션 호출 방식
async def insert(request:Request):
    print(dict(request._query_params))
    return templates.TemplateResponse(name="users/login.html", context={'request':request})

# 회원 가입 /users/insert -> users/login.html
@router.get("/insert") # 펑션 호출 방식
async def insert(request:Request):
    print(dict(request._query_params))
    return templates.TemplateResponse(name="users/login.html", context={'request':request})

# 회원 가입 /users/insert -> users/login.html
@router.post("/insert") # 펑션 호출 방식
async def insert_post(request:Request):
    user_dict = dict(await request.form())
    print(user_dict)
    # 저장
    user = User(**user_dict)
    await collection_user.save(user)

    # 리스트 정보
    user_list = await collection_user.get_all()
    return templates.TemplateResponse(name="users/list_jinja.html"
                                      , context={'request':request
                                                 , 'users' : user_list })

# 회원 리스트 /users/list -> users/list.html
@router.get("/list") # 펑션 호출 방식
async def list(request:Request):
    await request.form()
    print(dict(await request.form()))
    return templates.TemplateResponse(name="users/list.html"
                                      , context={'request':request})

# from pymongo import MongoClient
# # mongodb에 접속 -> 자원에 대한 class
# mongoClient = MongoClient("mongodb://localhost:27017")

# # database 연결
# database = mongoClient["toy_fastapis"]

# # collection 작업
# collection = database['users']

from database.connection import Database
from models.users import User
collection_user = Database(User)

@router.get("/list_jinja") # 펑션 호출 방식
async def list(request:Request):
    print(dict(request._query_params))
    # user_list = [
    #     {"id": 1, "name": "김철수", "email": "cheolsu@example.com"},
    #     {"id": 2, "name": "이영희", "email": "younghi@example.com"},
    #     {"id": 3, "name": "박지성", "email": "jiseong@example.com"},
    #     {"id": 4, "name": "김미나", "email": "mina@example.com"},
    #     {"id": 5, "name": "장현우", "email": "hyeonwoo@example.com"}
    # ]
    # insert 작업 진행
    # documents = collection.find({})
    # # documents.next()  # 오류 여부 확인용

    # # cast cursor to list 
    user_list = await collection_user.get_all()

    # for document in documents:
    #     # print("document : {}".format(document))
    #     user_list.append(document)
    #     pass

    # return templates.TemplateResponse(name="users/list.html"
    return templates.TemplateResponse(name="users/list_jinja.html"
                                      , context={'request':request
                                                 , 'users' : user_list })

from typing import Optional
@router.get("/list_jinja_pagination/{page_number}")
@router.get("/list_jinja_pagination") # 검색 with pagination
# http://127.0.0.1:8000/users/list_jinja_pagination?key_name=name&word=김
# http://127.0.0.1:8000/users/list_jinja_pagination/2?key_name=name&word=
# http://127.0.0.1:8000/users/list_jinja_pagination/2?key_name=name&word=김
async def list(request:Request, page_number: Optional[int] = 1):
    user_dict = dict(request._query_params)
    print(user_dict)
    # db.answers.find({'name':{ '$regex': '김' }})
    # { 'name': { '$regex': user_dict.word } }
    conditions = { }
    try :
        search_word = user_dict["word"]
    except:
        search_word = None
    if search_word:     # 검색어 작성
        conditions = {user_dict['key_name'] : { '$regex': user_dict["word"] }}
    
    user_list, pagination = await collection_user.getsbyconditionswithpagination(conditions
                                                                     ,page_number)
    return templates.TemplateResponse(name="/users/list_jinja_paginations.html"
                                      , context={'request':request
                                                 , 'users' : user_list
                                                  ,'pagination' : pagination })

@router.get("/search") # 검색
# http://127.0.0.1:8000/users/search?key=name&word=김
async def list(request:Request):
    user_dict = dict(request._query_params)
    print(user_dict)
    # db.answers.find({'name':{ '$regex': '김' }})
    # { 'name': { '$regex': user_dict.word } }
    try:
        conditions = { user_dict['key'] : { '$regex': user_dict["word"] } }
    except:
        conditions = {}

    user_list = await collection_user.getsbyconditions(conditions)
    return templates.TemplateResponse(name="users/list_jinja.html"
                                      , context={'request':request
                                                 , 'users' : user_list })

from beanie import PydanticObjectId
# 회원 상세정보 /users/read -> users/reads.html
# Path parameters : /users/read/id or /users/read/uniqe_name
@router.get("/read/{object_id}") # 펑션 호출 방식
async def reads(request:Request, object_id:PydanticObjectId):
    print(dict(request._query_params))
    user = await collection_user.get(object_id)
    return templates.TemplateResponse(name="users/reads.html"
                                      , context={'request':request
                                                 , 'user':user})