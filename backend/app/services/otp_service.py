from datetime import datetime, timedelta, timezone

from app.auth.otp import (
    OTP_EXPIRE_MINUTES,
    OTP_MAX_ATTEMPTS,
    generate_otp,
    hash_otp,
    verify_otp
)

from app.repositories.user_repository import (
    create_otp,
    get_latest_otp,
    increment_otp_attempts,
    invalidate_previous_otps,
    mark_otp_used
)


LOGIN_2FA = "LOGIN_2FA"


def generate_login_otp(
    user_id: int
):
    invalidate_previous_otps(
        user_id=user_id,
        purpose=LOGIN_2FA
    )

    otp = generate_otp()

    otp_hash = hash_otp(otp)

    expires_at = (
        datetime.now(timezone.utc)
        + timedelta(
            minutes=OTP_EXPIRE_MINUTES
        )
    )

    create_otp(
        user_id=user_id,
        otp_hash=otp_hash,
        purpose=LOGIN_2FA,
        expires_at=expires_at
    )

    return otp


def send_login_otp(
    email: str,
    otp: str
):
    print("\n================================")
    print("HRMS LOGIN OTP")
    print("Email:", email)
    print("OTP:", otp)
    print(
        "Expires in:",
        OTP_EXPIRE_MINUTES,
        "minutes"
    )
    print("================================\n")


def create_login_otp(
    user_id: int,
    email: str
):
    otp = generate_login_otp(
        user_id=user_id
    )

    send_login_otp(
        email=email,
        otp=otp
    )

    return True


def verify_login_otp(
    user_id: int,
    otp: str
):
    otp_record = get_latest_otp(
        user_id=user_id,
        purpose=LOGIN_2FA
    )

    if not otp_record:
        return False, "OTP not found"

    (
        otp_id,
        stored_user_id,
        otp_hash,
        purpose,
        expires_at,
        attempts,
        is_used,
        created_at
    ) = otp_record

    if is_used:
        return False, "OTP has already been used"

    current_time = datetime.now(timezone.utc)

    if expires_at <= current_time:
        return False, "OTP has expired"

    if attempts >= OTP_MAX_ATTEMPTS:
        return False, "Maximum OTP attempts exceeded"

    if not verify_otp(
        otp,
        otp_hash
    ):
        increment_otp_attempts(
            otp_id
        )

        return False, "Invalid OTP"

    mark_otp_used(
        otp_id
    )

    return True, "OTP verified successfully"