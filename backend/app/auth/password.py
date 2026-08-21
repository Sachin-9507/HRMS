
import bcrypt  # type: ignore
import secrets
import string


def hash_password(password: str) -> str:
    password_bytes = password.encode('utf-8')

    salt = bcrypt.gensalt()
    
    hashed = bcrypt.hashpw(
    password_bytes,
    salt
    )

    return hashed.decode('utf-8')


def verify_password(
        plain_password: str,
        hashed_password: str
) -> bool:


    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )




def generate_temporary_password(
    length: int = 12
):

    characters = (
        string.ascii_letters
        + string.digits
        + "!@#$%^&*"
    )

    return "".join(
        secrets.choice(characters)
        for _ in range(length)
    )