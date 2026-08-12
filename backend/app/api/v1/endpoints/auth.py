from fastapi import APIRouter

from app.services.auth_service import (
    register_user,
    start_login
)

from app.services.auth_service import (
    complete_2fa_login
)

router = APIRouter(
    prefix="/Auth",
    tags=["Authentication"] 
)


@router.post("/register")
def register(
    email: str,
    password: str,
    first_name: str,
    last_name: str,
    phone: str | None = None
):

    user = register_user(
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


@router.post("/login")
def login(
    email: str,
    password: str
):

    result = start_login(
        email=email,
        password=password
    )

    return result


from app.services.otp_service import (
    create_login_otp,
    verify_login_otp
)

from app.services.auth_service import (
    start_login,
    complete_2fa_login 

)

@router.post("/verify-otp")
def verify_otp_endpoint(
    user_id: int,
    otp: str
):

    result = complete_2fa_login(
        user_id=user_id,
        otp=otp
    )

    if not result["success"]:

        return result

    return result 