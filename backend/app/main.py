from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.endpoints import auth
from app.api.v1.endpoints import admin
from app.api.v1.endpoints.roles import router as roles_router
from app.api.v1.endpoints.employee import  router as employee_router

from app.api.v1.endpoints.departments import (
    router as department_router
)


from app.api.v1.endpoints.designations import (
    router as designation_router
)

app = FastAPI(
    title="HRMS API",
    version="1.0.0",
    description="Human Resource Management System API",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    auth.router,
    prefix="/api/v1",
)

app.include_router(
    admin.router,
    prefix="/api/v1",
)

app.include_router(
    roles_router,
    prefix="/api/v1"
) 

app.include_router(
    employee_router,
    prefix="/api/v1"
)

@app.get("/")
def root():
    return {
        "message": "HRMS API is running successfully"
    }



@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }

app.include_router(
    department_router,
    prefix="/api/v1"
)

app.include_router(
    designation_router,
    prefix="/api/v1"
)