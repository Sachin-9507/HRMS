from fastapi import FastAPI

from app.api.v1.endpoints.auth import router as auth_router


app = FastAPI(
    title="HRMS API"
)


app.include_router(
    auth_router,
    prefix="/api/v1"
)


@app.get("/")
def root():
    return {
        "message": "HRMS API is running"
    }