from fastapi import FastAPI

from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.admin import router as admin_router

app = FastAPI(
    title="HRMS API",
    version="0.1.0"
)

app.include_router(
    auth_router,
    prefix="/api/v1"
)

app.include_router(
    admin_router,
    prefix="/api/v1/admin",
    tags=["Administration"]
)

@app.get("/")
def root():
    return {
        "message": "HRMS API is running"
    }