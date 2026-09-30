from fastapi import APIRouter, Depends, HTTPException, Query
import json


from core.deps import get_current_user

from app.auth.jwt import (
    create_access_token,
    create_refresh_token
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
    result = verify_login_otp(
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



