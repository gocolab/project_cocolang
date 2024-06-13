from app.routes.users import router as user_router
from app.routes.common_codes import router as common_codes_router
from app.routes.comodules import router as comodules_router
from app.routes.mains import router as mains_router
from app.routes.securities import router as securities_router
from app.routes.errors import router as errors_router
from app.routes.communities import router as communities_router
from app.routes.boards import router as boards_router

def setup_routers(app):
    app.include_router(user_router, prefix="/users")
    app.include_router(common_codes_router, prefix="/commoncodes")
    app.include_router(comodules_router, prefix="/comodules")
    app.include_router(comodules_router, prefix="/devtemplates")
    app.include_router(comodules_router, prefix="/teams")
    app.include_router(mains_router, prefix="/mains")
    app.include_router(securities_router, prefix="/securities")
    app.include_router(errors_router, prefix="/errors")
    app.include_router(communities_router, prefix="/communities")
    app.include_router(boards_router, prefix="/boards")
