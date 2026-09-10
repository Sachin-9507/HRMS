from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    phone: str | None = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class VerifyOtpRequest(BaseModel):
    user_id: int
    otp: str = Field(
        min_length=6,
        max_length=6
    )


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str