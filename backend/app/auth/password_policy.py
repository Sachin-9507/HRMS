import re


MIN_PASSWORD_LENGTH = 8


def validate_password(password: str) -> None:
    if len(password) < MIN_PASSWORD_LENGTH:
        raise ValueError(
            "Password must contain at least 8 characters"
        )

    if not re.search(r"[A-Z]", password):
        raise ValueError(
            "Password must contain at least one uppercase letter"
        )

    if not re.search(r"[a-z]", password):
        raise ValueError(
            "Password must contain at least one lowercase letter"
        )

    if not re.search(r"\d", password):
        raise ValueError(
            "Password must contain at least one number"
        )

    if not re.search(r"[^A-Za-z0-9]", password):
        raise ValueError(
            "Password must contain at least one special character"
        )