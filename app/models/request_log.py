from beanie import Document
from typing import Optional, Dict
from datetime import datetime

class RequestLog(Document):
    request: Dict
    response: Dict
    create_timestamp: datetime = datetime.now()
    duration : datetime
    user :Optional[Dict]=None

    class Settings:
        name = "request_logs"