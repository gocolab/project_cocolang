from fastapi import Request
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException
from pydantic import ValidationError

templates = Jinja2Templates(directory="app/templates/")

async def http_exception_handler(request: Request, exc: Exception):
    status_code = 500
    message = ''

    if isinstance(exc, HTTPException):
        status_code = exc.status_code
        message = exc.detail
    elif isinstance(exc, RequestValidationError) or isinstance(exc, ValidationError):
        status_code = 400
        message = "Validation Error"
    elif isinstance(exc, StarletteHTTPException):
        status_code = exc.status_code
        message = exc.detail
    else:
        message = "Internal Server Error"

    return templates.TemplateResponse("/errors/errors.html", {"request": request, "message": message}, status_code=status_code)

def setup_error_handlers(app):
    app.add_exception_handler(RequestValidationError, http_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(ValidationError, http_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, http_exception_handler)
