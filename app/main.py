from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from app.middlewares import setup_middlewares
from app.routers import setup_routers
from app.database.database import init_db
from app.error_handlers import setup_error_handlers

app = FastAPI()

# Middleware setup
setup_middlewares(app)

# Router setup
setup_routers(app)

# Error handlers setup
setup_error_handlers(app)

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.get("/")
async def root(request: Request):
    # return RedirectResponse(url=f"/comodules/main")
    return RedirectResponse(url=f"/mains/list")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
