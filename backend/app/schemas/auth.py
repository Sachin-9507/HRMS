from pydantic import BaseModel


class RegisterData( BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
    phone_number: str | None
    role_id: int

class LoginData( BaseModel):
    email: str
    password: str


