from fastapi import APIRouter, Depends, HTTPException, Query
import json
from pyotp import TOTP, random_base32

from core.deps import get_current_user

from app.auth.jwt import (
    create_access_token,
    create_refresh_token
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


router = APIRouter(
    prefix="/Auth",
    tags=["Authentication"]
)


def generate_secret() -> str:
    return random_base32()


def verify_totp(secret: str, code: str) -> bool:
    return TOTP(secret).verify(code)


def get_provisioning_uri(
    email: str,
    secret: str,
    issuer: str
) -> str:

    return TOTP(secret).provisioning_uri(
        name=email,
        issuer_name=issuer
    )


# ---------------- REGISTER ----------------

@router.post("/register")
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


# ---------------- LOGIN ----------------

@router.post("/login")
def login(
    email: str = Query(...),
    password: str = Query(...)
):

    return start_login(
        email=email,
        password=password
    )


# ---------------- VERIFY OTP ----------------

@router.post("/verify-otp")
def verify_otp_api(
    user_id: int = Query(...),
    otp: str = Query(...)
):

    return  verify_login_2fa(
        user_id=user_id,
        code=otp
    )

    if not result:
        raise HTTPException(
            status_code=400,
            detail="Invalid OTP"
        )

    access_token = create_access_token(
        {
            "sub": str(user_id)
        }
    )

    refresh_token = create_refresh_token(
        {
            "sub": str(user_id)
        }
    )

    return {
        "verified": True,
        "message": "OTP verified successfully",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


# ---------------- VERIFY 2FA ----------------

@router.post("/verify-2fa")
def verify_2fa(
    user_id: int,
    code: str
):

    return verify_login_2fa(
        user_id=user_id,
        code=code
    )


# ---------------- 2FA SETUP ----------------

@router.post("/2fa/setup")
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


# ---------------- VERIFY 2FA SETUP ----------------

@router.post("/2fa/verify-setup")
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