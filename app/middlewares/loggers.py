import time
from app.models.request_log import RequestLog  # 로그 모델 임포트
from fastapi import Request
# 미들웨어를 사용하여 요청과 응답 로그를 MongoDB에 저장
async def log_request_response(request: Request, call_next):
    # 요청 처리 전 시간 측정
    start_time = time.time()

    # 요청 처리
    original_response  = await call_next(request)

    # 요청 처리 후 시간 측정
    end_time = time.time()

    # 처리 시간 계산 (초 단위)
    duration = end_time - start_time

    # 응답의 본문을 읽음 (스트리밍 응답을 처리하기 위해)
    response_body = b''
    async for chunk in original_response.body_iterator:
        response_body += chunk
    # 새로운 응답 생성
    new_response = Response(content=response_body
                            , status_code=original_response.status_code
                            , headers=dict(original_response.headers))
    
    # 로그 데이터 준비 및 저장
    log_data = RequestLog(
        request={
            "method": request.method,
            "url": str(request.url),
            "body": (await request.body())
        },
        response={
            "status_code": original_response.status_code,
            "body": response_body,  # 여기서는 'utf-8' 대신 적절한 인코딩을 사용해야 할 수도 있음
        }
        ,duration=duration
    )

    # MongoDB에 로그 데이터 저장
    await log_data.insert()

    return new_response

