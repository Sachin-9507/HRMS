from fastapi import APIRouter

from backend.app.api.v1.endpoints import root
from backend.app.api.v1.endpoints import health
from backend.app.api.v1.endpoints import database

api_router = APIRouter()

api_router.include_router(
    root.router,
    tags=["Root"]
)

api_router.include_router(
    health.router,
    prefix="/health",
    tags=["Health"]
)

api_router.include_router(
    database.router,
    tags=["Database"]
)