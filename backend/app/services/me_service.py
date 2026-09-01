from app.database.transaction import transaction


from app.repositories.me_repository import (
    get_my_profile_cursor,
    get_my_employee_cursor,
    get_user_by_email_cursor,
    update_my_email_cursor,
    update_my_employee_cursor
)

def get_my_profile(
    user_id: int
):

    with transaction() as cursor:

        row = get_my_profile_cursor(
            cursor,
            user_id
        )

    if not row:

        raise ValueError(
            "User not found"
        )

    return {
        "user_id": row[0],
        "email": row[1],
        "role_id": row[2],
        "role_name": row[3],
        "is_active": row[4]
    }

def get_my_employee(
    user_id: int
):

    with transaction() as cursor:

        row = get_my_employee_cursor(
            cursor,
            user_id
        )

    if not row:

        raise ValueError(
            "Employee profile not found"
        )

    return {
        "employee_id": row[0],
        "employee_code": row[1],

        "first_name": row[2],
        "last_name": row[3],

        "email": row[4],
        "phone": row[5],

        "department_id": row[6],
        "department_name": row[7],

        "designation_id": row[8],
        "designation_name": row[9],

        "is_active": row[10],

        "created_at": row[11],
        "updated_at": row[12]
    }

def update_my_email(
    user_id: int,
    email: str
):

    email = email.strip().lower()

    with transaction() as cursor:

        existing = get_user_by_email_cursor(
            cursor,
            email
        )

        if (
            existing
            and existing[0] != user_id
        ):

            raise ValueError(
                "Email already exists"
            )

        row = update_my_email_cursor(
            cursor,
            user_id,
            email
        )

    if not row:

        raise ValueError(
            "User not found"
        )

    return {
        "user_id": row[0],
        "email": row[1],
        "role_id": row[2],
        "is_active": row[3]
    }

def update_my_employee(
    user_id: int,
    data
):

    update_data = data.model_dump(
        exclude_unset=True
    )

    if not update_data:

        raise ValueError(
            "No fields provided for update"
        )

    with transaction() as cursor:

        row = update_my_employee_cursor(
            cursor,
            user_id,
            update_data
        )

        if not row:

            raise ValueError(
                "Employee profile not found"
            )

        employee = get_my_employee_cursor(
            cursor,
            user_id
        )

    return {
        "employee_id": employee[0],
        "employee_code": employee[1],

        "first_name": employee[2],
        "last_name": employee[3],

        "email": employee[4],
        "phone": employee[5],

        "department_id": employee[6],
        "department_name": employee[7],

        "designation_id": employee[8],
        "designation_name": employee[9],

        "is_active": employee[10],

        "created_at": employee[11],
        "updated_at": employee[12]
    }