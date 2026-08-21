from app.repositories.employee_repository import (
    create_employee_account as repository_create_employee_account,
    create_employee, 
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

from app.repositories.department_repository import (
    get_department_by_id
)

from app.database.db import get_cursor

from app.repositories.designation_repository import (
    get_designation_by_id
)

from app.repositories.employee_repository import (
    get_employee_by_id,
    get_employee_by_user_id,
    get_employees,
    count_employees
)

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
    create_employee_cursor
)

from app.auth.password import (
    hash_password,
    generate_temporary_password
)



def validate_department_designation(
    department_id: int,
    designation_id: int
):

    department = get_department_by_id(
        department_id
    )

    if not department:

        raise ValueError(
            "Department not found"
        )

    if not department[4]:

        raise ValueError(
            "Department is inactive"
        )

    designation = get_designation_by_id(
        designation_id
    )

    if not designation:

        raise ValueError(
            "Designation not found"
        )

    if not designation[6]:

        raise ValueError(
            "Designation is inactive"
        )

    designation_department_id = (
        designation[4]
    )

    if (
        designation_department_id
        != department_id
    ):

        raise ValueError(
            "Designation does not belong to selected department"
        )

    return True




def validate_manager(
    manager_id: int | None,
    employee_id: int | None = None
):

    if manager_id is None:

        return True

    if employee_id is not None:

        if manager_id == employee_id:

            raise ValueError(
                "Employee cannot be their own manager"
            )

    manager = get_employee_by_id(
        manager_id
    )

    if not manager:

        raise ValueError(
            "Manager employee not found"
        )

    if manager[16] != "ACTIVE":

        raise ValueError(
            "Manager is not active"
        )

    return True


def list_employees(
    search=None,
    department_id=None,
    designation_id=None,
    status=None,
    page=1,
    page_size=20
):

    if page < 1:

        page = 1

    if page_size < 1:

        page_size = 20

    if page_size > 100:

        page_size = 100

    employees = get_employees(
        search=search,
        department_id=department_id,
        designation_id=designation_id,
        status=status,
        page=page,
        page_size=page_size
    )

    total = count_employees(
        search=search,
        department_id=department_id,
        designation_id=designation_id,
        status=status
    )

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


def get_employee(
    employee_id: int
):

    employee = get_employee_by_id(
        employee_id
    )

    if not employee:

        raise ValueError(
            "Employee not found"
        )

    return employee



def get_current_employee(
    user_id: int
):

    employee = get_employee_by_user_id(
        user_id
    )

    if not employee:

        raise ValueError(
            "Employee profile not found"
        )

    return employee


def generate_employee_code():

    query = """
        SELECT
            COALESCE(
                MAX(id),
                0
            ) + 1
        FROM employees;
    """

    with get_cursor() as cursor:

        cursor.execute(query)

        next_id = cursor.fetchone()[0]

    return f"EMP{next_id:06d}"

def create_new_employee(
    data,
    user_id
):

    validate_department_designation(
        data.department_id,
        data.designation_id
    )

    validate_manager(
        data.manager_id
    )

    employee_code = (
        generate_employee_code()
    )

    return create_employee(
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
        employment_type=data.employment_type
    )


def create_employee_account(data):

    temporary_password = (
        generate_temporary_password()
    )

    password_hash = hash_password(
        temporary_password
    )

    with transaction() as cursor:

        # 1. Check email

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

        # 2. Find EMPLOYEE role

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

        # 3. Generate employee code

        employee_code = (
            generate_employee_code_cursor(
                cursor
            )
        )

        # 4. Create user
   
    user = create_user_cursor(
            cursor=cursor, 
            email=data.email,
            password_hash=password_hash,
            first_name=data.first_name,
            last_name=data.last_name,
            phone_number=data.phone,
            role_id=data.role_id
        )

    user_id = user[0]

        # 5. Assign EMPLOYEE role

    assign_role_cursor(
            cursor=cursor,
            user_id=user_id,
            role_id=employee_role[0]
        )

        # 6. Create employee

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
            employment_type=data.employment_type
        )

    return {
            "user": user,
            "employee": employee,
            "temporary_password":
                temporary_password
        }