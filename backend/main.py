from fastapi import FastAPI

from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.admin import router as admin_router
from fastapi.openapi.utils import get_openapi

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

from fastapi import APIRouter, Depends, HTTPException
import json
from pydantic import BaseModel, Field


from core.deps import get_current_user
from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    VerifyotpRequest
)

from app.services.auth_service import ( 
    register_user,
    start_login,
    verify_login_otp,
    
)


router = APIRouter(
    prefix="/Auth",
    tags=["Authentication"]
)


@router.post("/register", summary=" ")
def register(
    email: str,
    password: str,
    first_name: str,
    last_name: str,
    phone: str | None = None
):
    return register_user(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        phone=phone
    )

    return {
        "message": "User registered successfully",
        "user": {
            "id": user[0],
            "email": user[1],
            "first_name": user[2],
            "last_name": user[3],
            "phone": user[4],
            "role_id": user[5]
        }
    }


@router.post("/login", summary=" ")
def login(
    email: str,
    password: str
):

    

        return start_login(
            email=email,
            password=password
        )

       

@router.post("/verify-otp", summary=" ")
def verify_otp(
    user_id: int,
    code: str
):
    return verify_login_otp(
        user_id=user_id,
        code=code
    )

