from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):

    email: EmailStr
    password: str
    first_name: str
    last_name: str
    phone: str | None = None


class LoginRequest(BaseModel):

    email: EmailStr
    password: str


class Verify2FARequest(BaseModel):

   
    code: str

class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str