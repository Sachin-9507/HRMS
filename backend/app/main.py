from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from app.api.v1.endpoints import auth
from app.api.v1.endpoints import admin
from app.api.v1.endpoints.roles import router as roles_router
from app.api.v1.endpoints.employee import  router as employee_router
from app.api.v1.endpoints.permissions import (
    router as permission_router
)
from app.middleware.security import SecurityHeadersMiddleware
from app.api.v1.endpoints.departments import (
    router as department_router
)
from core.exceptions import AppException
from core.exception_handlers import (
    app_exception_handler,
    unexpected_exception_handler,
)

from app.api.v1.endpoints.designations import (
    router as designation_router
)

from app.api.v1.endpoints.me import (
    router as me_router
)

from app.api.v1.endpoints.attendance import (
    router as attendance_router
)

from app.api.v1.endpoints.admin_attendance import (
    router as admin_attendance_router
)

from app.api.v1.endpoints.leaves import router as leaves_router

from app.api.v1.endpoints.admin_leaves import (
    router as admin_leaves_router
)

from app.api.v1.endpoints.dashboard import (
    router as dashboard_router,
)

from app.api.v1.endpoints.admin_dashboard import (
    router as admin_dashboard_router,
)

from app.api.v1.endpoints.reports import (
    router as reports_router,
)

from app.api.v1.endpoints.audit import (
    router as audit_router,
)


app = FastAPI(
    title="HRMS API",
    version="1.0.0",
    description="Human Resource Management System API",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

app.add_middleware(SecurityHeadersMiddleware)

app.add_exception_handler(
    AppException,
    app_exception_handler,
)

app.add_exception_handler(
    Exception,
    unexpected_exception_handler,
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

app.include_router(
    permission_router,
    prefix="/api/v1"
)

app.include_router(
    me_router,
    prefix="/api/v1"
)

app.include_router(
    attendance_router,
    prefix="/api/v1"
)

app.include_router(
    admin_attendance_router,
    prefix="/api/v1"
)


app.include_router(
    leaves_router,
    prefix="/api/v1"
)

app.include_router(
    admin_leaves_router,
    prefix="/api/v1"
)


app.include_router(
    dashboard_router,
    prefix="/api/v1",
)

app.include_router(
    admin_dashboard_router,
    prefix="/api/v1",
)

app.include_router(
    reports_router,
    prefix="/api/v1",
)

app.include_router(
    audit_router,
    prefix="/api/v1",
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