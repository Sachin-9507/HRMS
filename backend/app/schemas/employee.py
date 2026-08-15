from typing import Optional
from pydantic import BaseModel


class EmployeeCreate(BaseModel):
    employee_code: str
    first_name: str
    last_name: str
    email: str
    joining_date: str
    employment_type: str

    phone: Optional[str] = None
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None

    department_id: Optional[int] = None
    designation_id: Optional[int] = None
    manager_id: Optional[int] = None
    salary: Optional[float] = None

    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None


EmployeeCreateRequest = EmployeeCreate