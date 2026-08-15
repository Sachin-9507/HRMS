from app.repositories.employee_repository import (
    create_employee_account as repository_create_employee_account
)

from app.repositories.user_repository import (
    get_user_by_email,
    get_employee_role
)

from app.utils.password import (
    generate_temporary_password
)

from app.auth.password import (
    hash_password
)


def create_employee_account(
    employee_data
):

    existing_user = get_user_by_email(
        employee_data.email
    )

    if existing_user:

        raise ValueError(
            "Email already exists"
        )

    role = get_employee_role()

    if not role:

        raise ValueError(
            "Employee role is not configured"
        )

    temporary_password = (
        generate_temporary_password()
    )

    password_hash = hash_password(
        temporary_password
    )

    user_id, employee = (
        repository_create_employee_account(
            user_email=employee_data.email,
            password_hash=password_hash,
            role_id=role[0],
            employee_code=employee_data.employee_code,
            first_name=employee_data.first_name,
            last_name=employee_data.last_name,
            phone=employee_data.phone,
            date_of_birth=employee_data.date_of_birth,
            gender=employee_data.gender,
            address=employee_data.address,
            city=employee_data.city,
            state=employee_data.state,
            country=employee_data.country,
            postal_code=employee_data.postal_code,
            joining_date=employee_data.joining_date,
            employment_type=employee_data.employment_type,
            department_id=employee_data.department_id,
            designation_id=employee_data.designation_id,
            manager_id=employee_data.manager_id,
            salary=employee_data.salary,
            emergency_contact_name=employee_data.emergency_contact_name,
            emergency_contact_phone=employee_data.emergency_contact_phone
        )
    )

    return {
        "user_id": user_id,
        "employee": employee,
        "temporary_password": temporary_password
    }