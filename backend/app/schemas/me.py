from datetime import date, datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator
)


class MyProfileResponse(BaseModel):

    user_id: int
    email: str
    role_id: int
    role_name: str
    is_active: bool


class MyProfileUpdateRequest(BaseModel):

    email: str | None = Field(
        default=None,
        min_length=5,
        max_length=255
    )


class MyEmployeeResponse(BaseModel):

    employee_id: int
    employee_code: str

    first_name: str
    last_name: str

    email: str | None
    phone: str | None

    department_id: int | None
    department_name: str | None

    designation_id: int | None
    designation_name: str | None

    is_active: bool

    created_at: datetime
    updated_at: datetime

    
class MyEmployeeUpdateRequest(BaseModel):

    model_config = ConfigDict(
        extra="forbid"
    )

    first_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    last_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    phone: str | None = Field(
        default=None,
        min_length=10,
        max_length=20
    )

    date_of_birth: date | None = None

    gender: str | None = Field(
        default=None,
        max_length=20
    )

    address: str | None = Field(
        default=None,
        max_length=255
    )

    city: str | None = Field(
        default=None,
        max_length=100
    )

    state: str | None = Field(
        default=None,
        max_length=100
    )

    postal_code: str | None = Field(
        default=None,
        max_length=20
    )

    emergency_contact_name: str | None = Field(
        default=None,
        max_length=150
    )

    emergency_contact_phone: str | None = Field(
        default=None,
        max_length=20
    )


@field_validator(
    "phone",
    "emergency_contact_phone"
)
@classmethod
def validate_phone(
    cls,
    value
):

    if value is None:
        return value

    cleaned = value.replace(
        " ",
        ""
    ).replace(
        "-",
        ""
    )

    if cleaned.startswith("+"):
        number = cleaned[1:]
    else:
        number = cleaned

    if not number.isdigit():
        raise ValueError(
            "Phone number must contain only digits"
        )

    if len(number) < 10:
        raise ValueError(
            "Invalid phone number"
        )

    return cleaned

@field_validator("gender")
@classmethod
def validate_gender(
    cls,
    value
):

    if value is None:
        return value

    allowed = {
        "MALE",
        "FEMALE",
        "OTHER",
        "PREFER_NOT_TO_SAY"
    }

    value = value.upper()

    if value not in allowed:

        raise ValueError(
            "Invalid gender value"
        )

    return value

@field_validator("date_of_birth")
@classmethod
def validate_date_of_birth(
    cls,
    value
):

    if value is None:
        return value

    if value >= date.today():

        raise ValueError(
            "Date of birth must be in the past"
        )

    return value

