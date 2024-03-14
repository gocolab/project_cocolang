from app.auth.hash_password import HashPassword
from app.auth.jwt_handler import create_access_token
from app.database.connection import Database
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.models.users import User, TokenResponse

router = APIRouter(
    tags=["User"],
)

from fastapi.templating import Jinja2Templates
from fastapi import Request

templates = Jinja2Templates(directory="templates/")

from app.database.connection import Database
from app.models.users import User
collection_user = Database(User)

hash_password = HashPassword()

# 회원 등록
@router.post("/signup")
async def sign_user_up(request:Request):
    user_dict = dict(await request.form())
    # 저장
    user = User(**user_dict)
    user_exist = await User.find_one(User.email == user.email)

    if user_exist:
        # 사용자 정의 에러 처리로 변경
        context = {'request': request, 'error': "User with email provided exists already."}
        return templates.TemplateResponse(name="users/form.html", context=context)
    
    hashed_password = hash_password.create_hash(user.password)
    user.password = hashed_password
    result = await collection_user.save(user)
    return templates.TemplateResponse(name="securities/login.html"
                        , context={'request':request})

# 회원 가입 폼
@router.get("/form") 
async def insert(request:Request):
    # print(dict(request._query_params))
    return templates.TemplateResponse(name="users/form.html"
                                      , context={'request':request})

from typing import Optional
@router.get("/list/{page_number}")
@router.get("/list") # 검색 with pagination
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
        conditions = {user_dict['key_name'] : { '$regex': user_dict["word"] }}
    except:
        pass

    user_list, pagination = await collection_user.getsbyconditionswithpagination(conditions
                                                                     ,page_number)
    return templates.TemplateResponse(name="users/list.html"
                                      , context={'request':request
                                                 , 'users' : user_list
                                                  ,'pagination' : pagination })
from beanie import PydanticObjectId
# 회원 상세정보 /users/read -> users/read.html
# Path parameters : /users/read/id or /users/read/uniqe_name
@router.get("/read/{object_id}")
async def read(request:Request, object_id:PydanticObjectId):
    print(dict(request._query_params))
    user = await collection_user.get(object_id)
    return templates.TemplateResponse(name="users/read.html"
                                      , context={'request':request
                                                 , 'user':user})

@router.post("/{object_id}")
async def read(request:Request, object_id:PydanticObjectId):
    delete_check = await collection_user.delete(object_id)
    return templates.TemplateResponse(name="users/list.html"
                                      , context={'request':request})