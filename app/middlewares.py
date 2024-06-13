from fastapi import Request, Response
from fastapi.responses import RedirectResponse
from typing import List
from app.auth.authenticate import userfromauthenticate
from app.models.request_log import RequestLog  # Import the log model
import time

# Excluded URL paths
EXCLUDE_PATHS = [
    "/errors",
    '/users/form',
    '/mains/list',
    "/devtemplates/list",
    "/teams/list",
    "/comodules/main", "/comodules/list", '/comodules/v1', '/comodules/r',
    "/communities/list", '/communities/r',
    '/securities',
    '/boards',
    # "/docs",   # Swagger documentation
    # "/openapi.json",  # OpenAPI spec
]

# Role-based URL access configuration
ROLE_BASED_ACCESS = {
    "GUEST": ["/comodules", '/users/read', '/communities'],
    "PARTNER": ["/devtemplates", "/teams"],
    "ADMIN": ["/admins", '/commoncodes', '/users']
}

# Paths to static files mounted using app.mount
STATIC_FILE_PATHS = ["/css", "/images", "/js",
    "/favicon.ico",]

# Middleware for token verification
async def auth_middleware(request: Request, call_next):
    # Check if the request path is a static file path
    if any(request.url.path.startswith(path) for path in STATIC_FILE_PATHS):
        return await call_next(request)
        
    user = await userfromauthenticate(request)
    request.state.user = user

    if not (any(request.url.path.startswith(path) for path in EXCLUDE_PATHS) 
            or request.url.path == '/'):
        # Role-based access control
        user_roles: List[str] = user.get("roles", [])
        path_allowed = False
        for role in user_roles:
            if any(request.url.path.startswith(path) for path in ROLE_BASED_ACCESS.get(role, [])):
                path_allowed = True
                break
        
        if not path_allowed:
            # Redirect user to a "permission denied" page if they have no access
            # return RedirectResponse(url="/errors/permission-denied")
            return RedirectResponse(url="/securities/login_google")

    # Continue with the next middleware or route handler
    response = await call_next(request)
    await log_request_response(request, response, user)
    return response

# Middleware for logging requests and responses
async def log_request_response(request: Request, response: Response, user):
    # Start time measurement before processing request
    start_time = time.time()
 
    # Extract parameters based on the request method
    parameters = {}
    if request.method == "GET":
        parameters = dict(request.query_params)
    
    end_time = time.time()
    duration = end_time - start_time
    
    # Prepare and save log data
    log_data = RequestLog(
        request={
            "method": request.method,
            'header': dict(request.headers),
            "parameters": parameters,
            # "body": (await request.body())
        },
        response={
            "status_code": response.status_code,
            # "body": response_body,  # Use appropriate encoding instead of 'utf-8' if necessary
        },
        duration=duration,
        user=user
    )

    # Save log data to MongoDB
    await log_data.insert()

from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

# Setup middlewares function to include in FastAPI app
def setup_middlewares(app):
    origins = ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(SessionMiddleware, secret_key="add any string...")
    
    # Add custom authentication middleware
    app.middleware("http")(auth_middleware)
