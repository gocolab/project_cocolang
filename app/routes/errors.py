from fastapi import FastAPI, APIRouter, Request, HTTPException, status, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["Errors"])
templates = Jinja2Templates(directory="app/templates/")

# Define a route for the "permission denied" page
@router.get("/permission-denied", response_class=HTMLResponse)
async def permission_denied(request: Request):
    # Render a "permission denied" page, for example, using Jinja2
    return HTMLResponse(content="Permission Denied", status_code=403)