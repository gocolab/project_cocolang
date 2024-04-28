import os
from dotenv import load_dotenv

# .env 파일의 절대 경로를 구성합니다.
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

# 명시적으로 .env 파일 경로를 load_dotenv 함수에 전달합니다.
load_dotenv(dotenv_path)

CLIENT_ID = os.environ.get('client-id', None)
CLIENT_SECRET = os.environ.get('client-secret', None)
pass