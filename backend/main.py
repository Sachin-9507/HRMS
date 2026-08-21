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
from pyotp import TOTP, random_base32

from core.deps import get_current_user
from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    Verify2FARequest
)

from app.services.auth_service import ( 
    register_user,
    start_login,
    verify_login_2fa,
    generate_secrets,
    get_user_by_id,
    generate_backup_codes,
    save_two_factor_secret,
    confirm_two_factor,
)


def generate_secret() -> str:
    return random_base32()

def verify_totp(secret: str, code: str) -> bool:
    return TOTP(secret).verify(code)

def get_provisioning_uri(email: str, secret: str, issuer: str) -> str:
    return TOTP(secret).provisioning_uri(name=email, issuer_name=issuer)


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

       

@router.post("/verify-2fa", summary=" ")
def verify_2fa(
    user_id: int,
    code: str
):
    return verify_login_2fa(
        user_id=user_id,
        code=code
    )

@router.post("/2fa/setup", summary=" ")
def setup_2fa(
    current_user=Depends(get_current_user)
):
    secret = generate_secret()

    save_two_factor_secret(
        current_user[0],
        secret
    )

    uri = get_provisioning_uri(
        email=current_user[1],
        secret=secret,
        issuer="HRMS"
    )

    return {
        "secret": secret,
        "provisioning_uri": uri
    }

@router.post("/2fa/verify-setup", summary=" ")
def verify_2fa_setup(
    code: str,
    current_user=Depends(get_current_user)
):
    user = get_user_by_id(
        current_user[0]
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    secret = user[10]

    if not secret:
        raise HTTPException(
            status_code=400,
            detail="2FA secret is not configured"
        )

    if not verify_totp(
        secret,
        code
    ):
        raise HTTPException(
            status_code=400,
            detail="Invalid authentication code"
        )

    backup_codes = generate_backup_codes()

    confirm_two_factor(
        current_user[0],
        json.dumps(backup_codes)
    )

    return {
        "message": "2FA enabled successfully",
        "backup_codes": backup_codes
    }