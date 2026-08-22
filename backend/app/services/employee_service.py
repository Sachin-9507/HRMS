from app.database.transaction import transaction

from app.repositories.user_repository import (
    get_user_by_email_cursor,
    create_user_cursor
)

from app.repositories.role_repository import (
    get_role_by_name_cursor,
    assign_role_cursor
)

from app.repositories.employee_repository import (
    generate_employee_code_cursor,
    create_employee_cursor,
    get_active_employee_by_id_cursor
)

from app.repositories.department_repository import (
    get_department_by_id_cursor
)

from app.repositories.designation_repository import (
    get_designation_by_id_cursor
)

from app.auth.password import (
    hash_password,
    generate_temporary_password
)


ALLOWED_EMPLOYMENT_TYPES = {
    "FULL_TIME",
    "PART_TIME",
    "CONTRACT",
    "INTERN",
    "TEMPORARY"
}


def validate_employment_type(
    employment_type: str
):

    employment_type = (
        employment_type.upper()
    )

    if employment_type not in (
        ALLOWED_EMPLOYMENT_TYPES
    ):
        raise ValueError(
            "Invalid employment type"
        )

    return employment_type


def validate_department(
    cursor,
    department_id: int
):

    department = (
        get_department_by_id_cursor(
            cursor,
            department_id
        )
    )

    if not department:

        raise ValueError(
            "Department not found"
        )

    return department


def validate_designation(
    cursor,
    designation_id: int
):

    designation = (
        get_designation_by_id_cursor(
            cursor,
            designation_id
        )
    )

    if not designation:

        raise ValueError(
            "Designation not found"
        )

    return designation


def validate_manager(
    cursor,
    manager_id: int | None
):

    if manager_id is None:
        return None

    manager = (
        get_active_employee_by_id_cursor(
            cursor,
            manager_id
        )
    )

    if not manager:

        raise ValueError(
            "Manager not found or inactive"
        )

    return manager


def create_employee_account(data):

    employment_type = (
        validate_employment_type(
            data.employment_type
        )
    )

    temporary_password = (
        generate_temporary_password()
    )

    password_hash = hash_password(
        temporary_password
    )

    with transaction() as cursor:

        # Check email
        existing_user = (
            get_user_by_email_cursor(
                cursor,
                data.email
            )
        )

        if existing_user:

            raise ValueError(
                "A user with this email already exists"
            )

        # Validate department
        validate_department(
            cursor,
            data.department_id
        )

        # Validate designation
        validate_designation(
            cursor,
            data.designation_id
        )

        # Validate manager
        validate_manager(
            cursor,
            data.manager_id
        )

        # Get employee role
        employee_role = (
            get_role_by_name_cursor(
                cursor,
                "EMPLOYEE"
            )
        )

        if not employee_role:

            raise ValueError(
                "EMPLOYEE role does not exist"
            )

        # Generate employee code
        employee_code = (
            generate_employee_code_cursor(
                cursor
            )
        )

        # Create user
        user = create_user_cursor(
            cursor=cursor,
            email=data.email,
            password_hash=password_hash
        )

        user_id = user[0]

        # Assign role
        assign_role_cursor(
            cursor=cursor,
            user_id=user_id,
            role_id=employee_role[0]
        )

        # Create employee
        employee = create_employee_cursor(
            cursor=cursor,
            employee_code=employee_code,
            user_id=user_id,
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            phone=data.phone,
            date_of_birth=data.date_of_birth,
            gender=data.gender,
            joining_date=data.joining_date,
            department_id=data.department_id,
            designation_id=data.designation_id,
            manager_id=data.manager_id,
            employment_type=employment_type
        )

        return {
            "user": user,
            "employee": employee,
            "temporary_password":
                temporary_password
        }

    return {
    "message": "Employee created successfully",
    "employee": result["employee"],
    "temporary_password":
        result["temporary_password"]
}