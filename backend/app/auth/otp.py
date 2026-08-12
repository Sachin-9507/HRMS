import os
import secrets

from dotenv import load_dotenv

from app.auth.password import (
    hash_password,
    verify_password
)


load_dotenv()


OTP_LENGTH = 6

OTP_EXPIRE_MINUTES = int(
    os.getenv(
        "OTP_EXPIRE_MINUTES",
        "5"
    )
)

OTP_MAX_ATTEMPTS = int(
    os.getenv(
        "OTP_MAX_ATTEMPTS",
        "5"
    )
)


def generate_otp() -> str:

    return "".join(
        str(secrets.randbelow(10))
        for _ in range(OTP_LENGTH)
    )


def hash_otp(otp: str) -> str:

    return hash_password(otp)


def verify_otp(
    otp: str,
    otp_hash: str
) -> bool:

    return verify_password(
        otp,
        otp_hash
    )