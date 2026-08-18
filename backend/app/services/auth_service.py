from fastapi import HTTPException, status
from datetime import datetime, timezone
import secrets
from app.auth.password import(
     hash_password,
      verify_password,
)
from app.auth.otp import (
       verify_otp,
       OTP_MAX_ATTEMPTS
)
from app.auth.jwt import (
    create_access_token,
    create_refresh_token, 
    get_refresh_token_expiry,
    
)

from app.repositories.user_repository import (
    create_refresh_token_record
)

from app.services.otp_service import create_login_otp, verify_login_otp



from app.services.otp_service import LOGIN_2FA


from app.repositories.user_repository import(
    create_user,
    get_role_by_name,
    get_user_by_email,
    get_user_by_id, 
    get_latest_otp,
    mark_otp_used,
    increment_otp_attempts,
    update_password,
    save_two_factor_secret,
    confirm_two_factor,
)


def validate_password(password: str) -> tuple[bool, str]:
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"

    if not any(char.isupper() for char in password):
        return False, "Password must contain at least one uppercase letter"

    if not any(char.islower() for char in password):
        return False, "Password must contain at least one lowercase letter"

    if not any(char.isdigit() for char in password):
        return False, "Password must contain at least one digit"

    return True, "Password is valid"


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


def create_login_tokens(user):

    user_id = user[0]
    email = user[1]
    role_id = user[6]

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
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": 1800
    }

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

    print("START_LOGIN IS RUNNING")
    print("debug 2fa:", is_2fa_enabled)

    if is_2fa_enabled:

        # Generate and save OTP
        create_login_otp(
            user_id=user_id,
            email=user_email
        )

        return {
            "requires_2fa": True,
            "user_id": user_id,
            "message": "OTP sent for verification"
        }

    # 2FA disabled → normal login
    tokens = create_login_tokens(user)

    return {
        "requires_2fa": False,
        "user_id": user_id,
        "message": "Login successful",
        "tokens": tokens
    }

def verify_login_2fa(
    user_id: int,
    code: str,
):
    """
    Verify the OTP after successful password login.

    Flow:
    1. Get latest LOGIN_2FA OTP
    2. Check OTP exists
    3. Check OTP is not already used
    4. Check OTP expiry
    5. Check maximum attempts
    6. Verify OTP
    7. Mark OTP as used
    8. Generate access token
    """

    # -----------------------------------
    # 1. GET LATEST LOGIN OTP
    # -----------------------------------

    otp_record = get_latest_otp(
        user_id=user_id,
        purpose=LOGIN_2FA,
    )

    if not otp_record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OTP not found",
        )

    otp_id = otp_record[0]
    otp_hash = otp_record[1]
    expires_at = otp_record[2]
    attempts = otp_record[3]
    is_used = otp_record[4]

    # -----------------------------------
    # 2. CHECK OTP ALREADY USED
    # -----------------------------------

    if is_used:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OTP already used",
        )

    # -----------------------------------
    # 3. CHECK OTP EXPIRY
    # -----------------------------------

    now = datetime.now(timezone.utc)

    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(
            tzinfo=timezone.utc
        )

    if expires_at < now:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OTP has expired",
        )

    # -----------------------------------
    # 4. CHECK MAXIMUM ATTEMPTS
    # -----------------------------------

    if attempts >= OTP_MAX_ATTEMPTS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum OTP attempts exceeded",
        )

    # -----------------------------------
    # 5. VERIFY OTP
    # -----------------------------------

    try:
        valid_otp = verify_otp(
            otp=code,
            otp_hash=otp_hash,
        )
    except Exception:
        valid_otp = False

    if not valid_otp:

        increment_otp_attempts(
            otp_id=otp_id,
        )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid OTP",
        )

    # -----------------------------------
    # 6. MARK OTP AS USED
    # -----------------------------------

    mark_otp_used(
        otp_id=otp_id,
    )

    # -----------------------------------
    # 7. CHECK USER
    # -----------------------------------

    user = get_user_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    # -----------------------------------
    # 8. CREATE ACCESS TOKEN
    # -----------------------------------

    access_token = create_access_token(
        {
            "sub": str(user_id),
        }
    )

    # -----------------------------------
    # 9. SUCCESS
    # -----------------------------------

    return {
        "message": "2FA verification successful",
        "access_token": access_token,
        "token_type": "bearer",
    }

def change_user_password(
    user_id: int,
    current_password: str,
    new_password: str
):

    user = get_user_by_id(
        user_id
    )

    if not user:

        raise ValueError(
            "User not found"
        )

    if not verify_password(
        current_password,
        user["password_hash"]
    ):

        raise ValueError(
            "Current password is incorrect"
        )

    valid, message = validate_password(
        new_password
    )

    if not valid:

        raise ValueError(
            message
        )

    password_hash = hash_password(
        new_password
    )

    update_password(
        user_id,
        password_hash
    )

    return {
        "message":
            "Password changed successfully"
    }

def generate_secrets() -> str:
    return secrets.token_urlsafe(32)

def generate_backup_codes(count: int = 10) -> list[str]:
    return [
        secrets.token_hex(4).upper()
        for _ in range(count)
    ]