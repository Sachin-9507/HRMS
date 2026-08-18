import pyotp


def generate_secret() -> str:
    return pyotp.random_base32()


