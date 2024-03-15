from app.auth.jwt_handler import verify_access_token
from fastapi import Request
# 제외할 URL 경로 목록
EXCLUDE_PATHS = [
    "/css", "/images", "/js", "/downloads",
    "/docs",   # Swagger 문서
    "/openapi.json",  # OpenAPI 스펙
]
# Middleware for token verification
async def auth_middleware(request: Request, call_next):
    request.state.user = None
    # 요청 URL 확인
    if not any(path for path in EXCLUDE_PATHS if request.url.path.startswith(path)):
        authorization = request.cookies.get("Authorization")

        if authorization:
            token = authorization.split(" ")[1]
            # credentials_exception = HTTPException(status_code=401, detail="Could not validate credentials")
            user = await verify_access_token(token)
            request.state.user = user
    response = await call_next(request)
    return response

