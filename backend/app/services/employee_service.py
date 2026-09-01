from app.database.transaction import transaction

from app.repositories.user_repository import (
    get_user_by_email_cursor,
    create_user_cursor,
    get_user_by_email_except_user_cursor,
    update_user_email_cursor,
    update_user_active_status_cursor
)

from app.repositories.role_repository import (
    get_role_by_name_cursor
)

from app.repositories.employee_repository import (
    generate_employee_code_cursor,
    create_employee_cursor,
    get_active_employee_by_id_cursor,
    get_employee_cursor,
    get_employee_by_id_cursor,
    get_employee_for_update_cursor,
    update_employee as repository_update_employee,
    update_employee_status
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

    query = """
        SELECT id
        FROM departments
        WHERE id = %s
          AND is_active = TRUE
        LIMIT 1
    """

    cursor.execute(
        query,
        (department_id,)
    )

    row = cursor.fetchone()

    if not row:

        raise ValueError(
            "Department not found or inactive"
        )


def validate_designation(
    cursor,
    designation_id: int
):

    query = """
        SELECT id
        FROM designations
        WHERE id = %s
          AND is_active = TRUE
        LIMIT 1
    """

    cursor.execute(
        query,
        (designation_id,)
    )

    row = cursor.fetchone()

    if not row:

        raise ValueError(
            "Designation not found or inactive"
        )


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
                "Employee"
            )
        )

        if not employee_role:

            raise ValueError(
                "Employee role does not exist"
            )

        # Generate employee code
        employee_code = (
            generate_employee_code_cursor(
                cursor
            )
        )

        # Create user
        user_result = create_user_cursor(
            cursor=cursor,
            email=data.email,
            password_hash=password_hash,
            first_name=data.first_name,
            last_name=data.last_name,
            phone_number=data.phone,
            role_id=employee_role[0]

        )

        user_id = user_result[0]

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
            "user_id": user_id,
            "employee": employee,
            "temporary_password":
                temporary_password
        }

def map_employee_row(row):

    return {
        "id": row[0],
        "employee_code": row[1],
        "user_id": row[2],
        "first_name": row[3],
        "last_name": row[4],
        "email": row[5],
        "phone": row[6],
        "date_of_birth": row[7],
        "gender": row[8],
        "joining_date": row[9],
        "department_id": row[10],
        "department_name": row[11],
        "designation_id": row[12],
        "designation_name": row[13],
        "manager_id": row[14],
        "manager_name": row[15],
        "employment_type": row[16],
        "status": row[17],
        "is_active": row[18],
        "created_at": row[19]
    }

def list_employees(
    search=None,
    department_id=None,
    designation_id=None,
    status=None,
    page=1,
    page_size=10
):

    with transaction() as cursor:

        rows, total = (
            get_employee_cursor(
                cursor=cursor,
                search=search,
                department_id=department_id,
                designation_id=designation_id,
                status=status,
                page=page,
                page_size=page_size
            )
        )

    employees = [
        map_employee_row(row)
        for row in rows
    ]

    total_pages = (
        (total + page_size - 1)
        // page_size
    )

    return {
        "items": employees,
        "page": page,
        "page_size": page_size,
        "total": total,
        "total_pages": total_pages
    }

def map_employee_details_row(row):

    return {
        "id": row[0],
        "employee_code": row[1],
        "user_id": row[2],
        "first_name": row[3],
        "last_name": row[4],
        "email": row[5],
        "phone": row[6],
        "date_of_birth": row[7],
        "gender": row[8],
        "joining_date": row[9],
        "department_id": row[10],
        "department_name": row[11],
        "designation_id": row[12],
        "designation_name": row[13],
        "manager_id": row[14],
        "manager_name": row[15],
        "employment_type": row[16],
        "status": row[17],
        "is_active": row[18],
        "is_verified": row[19],
        "must_change_password": row[20],
        "created_at": row[21],
        "updated_at": row[22]
    }

def get_employee(
    employee_id: int
):

    with transaction() as cursor:

        row = (
            get_employee_by_id_cursor(
                cursor,
                employee_id
            )
        )

    if not row:

        raise ValueError(
            "Employee not found"
        )

    return map_employee_details_row(
        row
    )

def update_employee(
    employee_id: int,
    data
):

    with transaction() as cursor:

        print(
            "1. Before employee lookup:",
            cursor.closed,
            cursor.connection.closed
        )

        employee = get_employee_for_update_cursor(
            cursor,
            employee_id
        )

        print(
            "2. After employee lookup:",
            cursor.closed,
            cursor.connection.closed
        )

        if not employee:
            raise ValueError(
                "Employee not found"
            )

        user_id = employee[1]

        # -------------------------
        # Email validation
        # -------------------------

        if "email" in data:

            existing_user = (
                get_user_by_email_except_user_cursor(
                    cursor,
                    data["email"],
                    user_id
                )
            )

            if existing_user:
                raise ValueError(
                    "Email is already used by another user"
                )

        # -------------------------
        # Department validation
        # -------------------------

        if "department_id" in data:

            validate_department(
                cursor,
                data["department_id"]
            )

        # -------------------------
        # Designation validation
        # -------------------------

        if "designation_id" in data:

            validate_designation(
                cursor,
                data["designation_id"]
            )

        # -------------------------
        # Manager validation
        # -------------------------

        if "manager_id" in data:

            if data["manager_id"] == employee_id:
                raise ValueError(
                    "Employee cannot be their own manager"
                )

            validate_manager(
                cursor,
                data["manager_id"]
            )

        # -------------------------
        # Employment type
        # -------------------------

        if "employment_type" in data:

            data["employment_type"] = (
                validate_employment_type(
                    data["employment_type"]
                )
            )

        # -------------------------
        # Update employee
        # -------------------------

        updated_employee = (
            repository_update_employee(
                cursor,
                employee_id,
                data
            )
        )

        if not updated_employee:
            raise ValueError(
                "Employee update failed"
            )

        # -------------------------
        # Sync user email
        # -------------------------

        if "email" in data:

            update_user_email_cursor(
                cursor,
                user_id,
                data["email"]
            )

        return updated_employee

            
def update_employee_status(
    employee_id: int,
    status: str
):

    status = status.upper()

    if status not in {
        "ACTIVE",
        "INACTIVE"
    }:
        raise ValueError(
            "Invalid employee status. Use ACTIVE or INACTIVE"
        )

    with transaction() as cursor:

        employee = get_employee_for_update_cursor(
            cursor,
            employee_id
        )

        if not employee:
            raise ValueError(
                "Employee not found"
            )

        user_id = employee[1]

        is_active = (
            status == "ACTIVE"
        )

        # Update employees.status
        updated_employee = update_employee_status(
            cursor,
            employee_id,
            status
        )

        # Keep users.is_active synchronized
        update_user_active_status_cursor(
            cursor,
            user_id,
            is_active
        )

        return {
            "employee_id": employee_id,
            "status": status,
            "is_active": is_active
        }