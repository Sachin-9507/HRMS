from fastapi import HTTPException, status
from datetime import datetime, timezone

from app.auth.password import hash_password, verify_password
from app.repositories.user_repository import(
    create_user,
    get_role_by_name,
    get_user_by_email,
    get_user_by_id, 
)


def register_user(
        email:str,
        password: str,
        first_name: str,
        last_name:str,
        phone:str |None = None
):

    email = email.strip().lower()

    existing_user = get_user_by_email(email)

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    employee_role = get_role_by_name("Employee")

    if not employee_role:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Employee role is not configured"
        )

    role_id = employee_role[0]

    password_hash = hash_password(password)


    user = create_user(
        email=email,
        password_hash=password_hash,
        first_name=first_name.strip(),
        last_name=last_name.strip(),
        phone=phone,
        role_id=role_id
    )

    return user


def authenticate_user(
        email:str,
        password:str
):

    email = email.strip().lower()

    user = get_user_by_email(email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    (
        user_id,
        user_email,
        password_hash,
        first_name,
        last_name,
        phone,
        role_id,
        is_active,
        is_email_verified,
        is_2fa_enabled,
        failed_login_attempts,
        locked_until,
        last_login_at,
        created_at,
        updated_at,
    ) = user

    if not is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive"
        )

    if locked_until is not None:

        current_time = datetime.now(timezone.utc)

        if locked_until > current_time:

            raise HTTPException(
                status_code=status.HTTP_423_LOCKED,
                detail="Account is temporarily locked"
            )

    if not verify_password(password, password_hash):

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    return user 


from app.auth.jwt import (
    create_access_token,
    create_refresh_token,
    get_refresh_token_expiry
)

from app.repositories.user_repository import (
    create_refresh_token_record
)

def create_login_tokens(user):

    user_id = user[0]
    email = user[1]
    role_id = user[6]

    access_token = create_access_token(
        user_id=user_id,
        email=email,
        role_id=role_id
    )

    refresh_token, refresh_token_hash = (
        create_refresh_token()
    )

    refresh_expiry = (
        get_refresh_token_expiry()
    )

    create_refresh_token_record(
        user_id=user_id,
        token_hash=refresh_token_hash,
        expires_at=refresh_expiry
    )
 
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": 1800
    }

from app.services.otp_service import create_login_otp, verify_login_otp

def start_login(
    email: str,
    password: str
):

    user = authenticate_user(
        email=email,
        password=password
    )

    user_id = user[0]
    user_email = user[1]
    is_2fa_enabled = user[9]

    print ("START_LOGIN IN RUNNING")
    print("debug 2fa:",is_2fa_enabled)

    if is_2fa_enabled:

        create_login_otp(
            user_id=user_id,
            email=user_email
        )

        return {
            "requires_2fa": True,
            "user_id": user_id,
            "message": "OTP sent for verification"
        }

    tokens = create_login_tokens(
        user
    )

    return {
        "requires_2fa": False,
        "user_id": user_id,
        "message": "Login successful",
        "tokens": tokens
    }


def complete_2fa_login(
    user_id: int,
    otp: str
):

    success, message = verify_login_otp(
        user_id=user_id,
        otp=otp
    )

    if not success:

        return {
            "success": False,
            "message": message
        }

    user = get_user_by_id(
        user_id
    )

    if not user:

        return {
            "success": False,
            "message": "User not found"
        }

    tokens = create_login_tokens(
        user
    ) 

    return {
        "success": True,
        "message": "Two-step verification successful",
        "tokens": tokens
    }