from app.database.db import get_cursor


def create_employee(
    employee_code,
    user_id,
    first_name,
    last_name,
    email,
    phone,
    date_of_birth,
    gender,
    address,
    city,
    state,
    country,
    postal_code,
    joining_date,
    employment_type,
    department_id,
    designation_id,
    manager_id,
    salary,
    
):
    query = """
        INSERT INTO employees (
            employee_code,
            user_id,
            first_name,
            last_name,
            email,
            phone,
            date_of_birth,
            gender,
            address,
            city,
            state,
            country,
            postal_code,
            joining_date,
            employment_type,
            department_id,
            designation_id,
            manager_id,
            salary
           
        )
        VALUES (
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s
        )
        RETURNING
            id,
            employee_code,
            user_id,
            first_name,
            last_name,
            email,
            phone,
            date_of_birth,
            gender,
            joining_date,
            department_id,
            designation_id,
            manager_id,
            employment_type,
            status,
            created_at,
            updated_at;
    """

    values = (
        employee_code,
        user_id,
        first_name,
        last_name,
        email,
        phone,
        date_of_birth,
        gender,
        address,
        city,
        state,
        country,
        postal_code,
        joining_date,
        employment_type,
        department_id,
        designation_id,
        manager_id,
        salary
        
    )

    with get_cursor() as cursor:
        cursor.execute(query, values)
        return cursor.fetchone()


def get_all_employee(
        search=None,
        department_id=None,
        designation_id=None,
        manager_id=None,
        status=None,
        page=1,
        page_size=10
):
    query = """
        SELECT
            e.id,
            e.employee_code,
            e.user_id,
            e.first_name,
            e.last_name,
            e.email,
            e.phone,
            e.joining_date,
            e.employment_type,
            e.department_id,
            d.name AS department,
            e.designation_id,
            des.name AS designation,
            e.manager_id,
            e.salary,
            e.status,
            e.created_at
        FROM employees e

        LEFT JOIN departments d
            ON d.id = e.department_id

        LEFT JOIN designations des
            ON des.id = e.designation_id

        ORDER BY e.id;
    """

    with get_cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchall()


def get_employee_by_id(employee_id: int):
    query = """
        SELECT
            e.id,
            e.employee_code,
            e.user_id,
            e.first_name,
            e.last_name,
            e.email,
            e.phone,
            e.date_of_birth,
            e.gender,
            e.address,
            e.city,
            e.country,
            e.postal_code,
            e.joining_date,
            e.employment_type,
            e.department_id,
            d.name AS department,
            e.designation_id,
            des.name AS designation,
            e.manager_id,
            e.salary,
            e.status,
            e.created_at,
            e.updated_at
        FROM employees e

        LEFT JOIN departments d
            ON d.id = e.department_id

        LEFT JOIN designations des
            ON des.id = e.designation_id

        WHERE e.id = %s

        LIMIT 1;
    """

    with get_cursor() as cursor:
        cursor.execute(
            query,
            (employee_id,)
        )
        return cursor.fetchone()


def update_employee(
    employee_id,
    first_name,
    last_name,
    phone,
    date_of_birth,
    gender,
    address,
    city,
    state,
    country,
    postal_code,
    department_id,
    designation_id,
    manager_id,
    salary,
    employment_type,
    status,
    
):
    query = """
        UPDATE employees
        SET
            first_name = %s,
            last_name = %s,
            phone = %s,
            date_of_birth = %s,
            gender = %s,
            address = %s,
            city = %s,
            state = %s,
            country = %s,
            postal_code = %s,
            department_id = %s,
            designation_id = %s,
            manager_id = %s,
            salary = %s,
            employment_type = %s,
            status = %s,
           
            updated_at = CURRENT_TIMESTAMP
        WHERE id = %s

        RETURNING
            id,
            employee_code,
            first_name,
            last_name,
            email,
            status,
            updated_at;
    """

    values = (
        first_name,
        last_name,
        phone,
        date_of_birth,
        gender,
        address,
        city,
        state,
        country,
        postal_code,
        department_id,
        designation_id,
        manager_id,
        salary,
        employment_type,
        status,
        employee_id,
    )

    with get_cursor() as cursor:
        cursor.execute(query, values)
        return cursor.fetchone()


def deactivate_employee(employee_id: int):
    query = """
        UPDATE employees
        SET
            status = 'INACTIVE',
            updated_at = CURRENT_TIMESTAMP
        WHERE id = %s

        RETURNING
            id,
            employee_code,
            status;
    """

    with get_cursor() as cursor:
        cursor.execute(
            query, 
            (employee_id,)
        )
        return cursor.fetchone()

def activate_employee(employee_id: int):
    query = """
        UPDATE employees
        SET
            status = 'ACTIVE',
            updated_at = CURRENT_TIMESTAMP
        WHERE id = %s

        RETURNING
            id,
            employee_code,
            status;
    """

    with get_cursor() as cursor:
        cursor.execute(
            query,
            (employee_id,)
        )

        return cursor.fetchone()


def create_employee_account(
    user_email,
    password_hash,
    role_id,
    employee_code,
    first_name,
    last_name,
    phone,
    date_of_birth,
    gender,
    address,
    city,
    state,
    country,
    postal_code,
    joining_date,
    employment_type,
    department_id,
    designation_id,
    manager_id,
    salary,
   
):
    user_query = """
        INSERT INTO users (email, password_hash, first_name, last_name, phone_number, role_id)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id;
    """

    employee_query = """
        INSERT INTO employees (
            employee_code,
            user_id,
            first_name,
            last_name,
            email,
            phone,
            date_of_birth,
            gender,
            address,
            city,
            state,
            country,
            postal_code,
            joining_date,
            employment_type,
            department_id,
            designation_id,
            manager_id,
            salary
           
        )
        VALUES (
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s
        )
        RETURNING
            id,
            employee_code,
            user_id,
            first_name,
            last_name,
            email,
            status,
            created_at;
    """

    with get_cursor() as cursor:
        # 1. Create user
        cursor.execute(
            user_query,
            (
                user_email,
                password_hash,
                first_name,
                last_name,
                phone,
                role_id,
            )
        )

        user_id = cursor.fetchone()[0]

        # 2. Create employee
        cursor.execute(
            employee_query,
            (
                employee_code,
                user_id,
                first_name,
                last_name,
                user_email,
                phone,
                date_of_birth,
                gender,
                address,
                city,
                state,
                country,
                postal_code,
                joining_date,
                employment_type,
                department_id,
                designation_id,
                manager_id,
                salary
               
            )
        )

        employee = cursor.fetchone()

        return user_id, employee

    from app.database.db import get_cursor


def get_employee_by_user_id(user_id: int):

    query = """
        SELECT
            e.id,
            e.user_id,
            e.employee_code,
            e.first_name,
            e.last_name,
            e.email,
            e.phone,
            e.date_of_birth,
            e.gender,
            e.address,
            e.city,
            e.country,
            e.postal_code,
            e.joining_date,
            e.employment_type,
            e.department_id,
            e.designation_id,
            e.manager_id,
            e.salary,
            e.status,
            e.created_at,
            e.updated_at
            FROM employees e
        WHERE e.user_id = %s
        LIMIT 1;
    """

    with get_cursor() as cursor:
        cursor.execute(
            query,
            (user_id,)
        )
        return cursor.fetchone()



def get_employees(
    search=None,
    department_id=None,
    designation_id=None,
    status=None,
    page=1,
    page_size=20
):

    offset = (
        page - 1
    ) * page_size

    query = """
    SELECT
        e.id,
        e.employee_code,
        e.user_id,
        u.first_name,
        u.last_name,
        u.email,
        u.phone_number,
        e.date_of_joining,
        e.employment_type,
        e.department_id,
        d.name AS department_name,
        e.designation_id,
        des.name AS designation_name,
        e.salary,
        e.status,
        e.created_at
    FROM employees e
    JOIN users u ON u.id = e.user_id
    LEFT JOIN departments d ON d.id = e.department_id
    LEFT JOIN designations des ON des.id = e.designation_id
    WHERE 1=1
"""
    params = []

    if search:

        query += """
            AND (
                e.employee_code ILIKE %s
                OR e.first_name ILIKE %s
                OR e.last_name ILIKE %s
                OR e.email ILIKE %s
            )
        """

        search_value = f"%{search}%"

        params.extend([
            search_value,
            search_value,
            search_value,
            search_value
        ])

    if department_id:

        query += """
            AND e.department_id = %s
        """

        params.append(
            department_id
        )

    if designation_id:

        query += """
            AND e.designation_id = %s
        """

        params.append(
            designation_id
        )

    if status:

        query += """
            AND e.status = %s
        """

        params.append(
            status
        )

    query += """
        ORDER BY e.id DESC

        LIMIT %s
        OFFSET %s;
    """

    params.extend([
        page_size,
        offset
    ])

    with get_cursor() as cursor:

        cursor.execute(
            query,
            tuple(params)
        )

        return cursor.fetchall()



def count_employees(
    search=None,
    department_id=None,
    designation_id=None,
    status=None
):

    query = """
        SELECT COUNT(*)

        FROM employees e

        WHERE 1 = 1
    """

    params = []

    if search:

        query += """
            AND (
                e.employee_code ILIKE %s
                OR e.first_name ILIKE %s
                OR e.last_name ILIKE %s
                OR e.email ILIKE %s
            )
        """

        search_value = f"%{search}%"

        params.extend([
            search_value,
            search_value,
            search_value,
            search_value
        ])

    if department_id:

        query += """
            AND e.department_id = %s
        """

        params.append(
            department_id
        )

    if designation_id:

        query += """
            AND e.designation_id = %s
        """

        params.append(
            designation_id
        )

    if status:

        query += """
            AND e.status = %s
        """

        params.append(
            status
        )

    with get_cursor() as cursor:

        cursor.execute(
            query,
            tuple(params)
        )

        result = cursor.fetchone()

        return result[0]


def generate_employee_code_cursor(
    cursor
):

    cursor.execute(
        """
        SELECT nextval(
            'employee_code_seq'
        )
        """
    )

    number = cursor.fetchone()[0]

    return f"EMP{number:06d}"

def create_employee_cursor(
    cursor,
    employee_code,
    user_id,
    first_name,
    last_name,
    email,
    phone,
    date_of_birth,
    gender,
    joining_date,
    department_id,
    designation_id,
    manager_id,
    employment_type
):

    query = """
        INSERT INTO employees (
            employee_code,
            user_id,
            first_name,
            last_name,
            email,
            phone,
            date_of_birth,
            gender,
            joining_date,
            department_id,
            designation_id,
            manager_id,
            employment_type,
            status
        )
        VALUES (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            'ACTIVE'
        )
        RETURNING
            id,
            employee_code,
            user_id,
            first_name,
            last_name,
            email,
            phone,
            date_of_birth,
            gender,
            joining_date,
            department_id,
            designation_id,
            manager_id,
            employment_type,
            status,
            created_at,
            updated_at
    """

    cursor.execute(
        query,
        (
            employee_code,
            user_id,
            first_name,
            last_name,
            email,
            phone,
            date_of_birth,
            gender,
            joining_date,
            department_id,
            designation_id,
            manager_id,
            employment_type
        )
    )

    return cursor.fetchone()

def get_active_employee_by_id_cursor(
    cursor,
    employee_id: int
):
    query = """
        SELECT
            id,
            employee_code,
            user_id,
            first_name,
            last_name,
            status
        FROM employees
        WHERE id = %s
          AND status = 'ACTIVE'
        LIMIT 1
    """

    cursor.execute(
        query,
        (employee_id,)
    )

    return cursor.fetchone()


def get_employee_cursor(
    cursor,
    search: str | None = None,
    department_id: int | None = None,
    designation_id: int | None = None,
    status: str | None = None,
    page: int = 1,
    page_size: int = 10
):

    conditions = []
    params = []

    if search:

        conditions.append("""
            (
                LOWER(e.first_name)
                    LIKE LOWER(%s)

                OR LOWER(e.last_name)
                    LIKE LOWER(%s)

                OR LOWER(e.email)
                    LIKE LOWER(%s)

                OR LOWER(e.employee_code)
                    LIKE LOWER(%s)
            )
        """)

        search_value = f"%{search}%"

        params.extend([
            search_value,
            search_value,
            search_value,
            search_value
        ])

    if department_id is not None:

        conditions.append(
            "e.department_id = %s"
        )

        params.append(
            department_id
        )

    if designation_id is not None:

        conditions.append(
            "e.designation_id = %s"
        )

        params.append(
            designation_id
        )

    if status:

        conditions.append(
            "e.status = %s"
        )

        params.append(
            status.upper()
        )

    where_clause = ""

    if conditions:

        where_clause = (
            "WHERE "
            + " AND ".join(conditions)
        )

    count_query = f"""
        SELECT COUNT(*)
        FROM employees e
        JOIN users u
            ON u.id = e.user_id

        {where_clause}
    """

    cursor.execute(
        count_query,
        tuple(params)
    )

    total = cursor.fetchone()[0]

    offset = (
        (page - 1) * page_size
    )

    query = f"""
        SELECT
            e.id,
            e.employee_code,
            e.user_id,

            e.first_name,
            e.last_name,

            e.email,
            e.phone,

            e.date_of_birth,
            e.gender,
            e.joining_date,

            e.department_id,
            d.name AS department_name,

            e.designation_id,
            des.name AS designation_name,

            e.manager_id,

            CONCAT(
                manager.first_name,
                ' ',
                COALESCE(
                    manager.last_name,
                    ''
                )
            ) AS manager_name,

            e.employment_type,
            e.status,

            u.is_active,

            e.created_at

        FROM employees e

        JOIN users u
            ON u.id = e.user_id

        LEFT JOIN departments d
            ON d.id = e.department_id

        LEFT JOIN designations des
            ON des.id = e.designation_id

        LEFT JOIN employees manager
            ON manager.id = e.manager_id

        {where_clause}

        ORDER BY e.id DESC

        LIMIT %s
        OFFSET %s
    """

    query_params = params + [
        page_size,
        offset
    ]

    cursor.execute(
        query,
        tuple(query_params)
    )

    rows = cursor.fetchall()

    return rows, total


def get_employee_by_id_cursor(
    cursor,
    employee_id: int
):

    query = """
        SELECT
            e.id,
            e.employee_code,
            e.user_id,

            e.first_name,
            e.last_name,

            e.email,
            e.phone,

            e.date_of_birth,
            e.gender,
            e.joining_date,

            e.department_id,
            d.name AS department_name,

            e.designation_id,
            des.name AS designation_name,

            e.manager_id,

            CONCAT(
                manager.first_name,
                ' ',
                COALESCE(
                    manager.last_name,
                    ''
                )
            ) AS manager_name,

            e.employment_type,
            e.status,

            u.is_active,
            u.is_verified,
            u.must_change_password,

            e.created_at,
            e.updated_at

        FROM employees e

        JOIN users u
            ON u.id = e.user_id

        LEFT JOIN departments d
            ON d.id = e.department_id

        LEFT JOIN designations des
            ON des.id = e.designation_id

        LEFT JOIN employees manager
            ON manager.id = e.manager_id

        WHERE e.id = %s

        LIMIT 1
    """

    cursor.execute(
        query,
        (employee_id,)
    )

    return cursor.fetchone()

def get_employee_for_update_cursor(
    cursor,
    employee_id: int
):

    query = """
        SELECT
            e.id,
            e.user_id,
            e.email,
            e.status
        FROM employees e
        WHERE e.id = %s
        LIMIT 1
    """

    cursor.execute(
        query,
        (employee_id,)
    )

    return cursor.fetchone()

def update_employee_status(
    employee_id: int,
    status: str
):
    query = """
        UPDATE employees
        SET
            status = %s,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = %s
        RETURNING
            id,
            employee_code,
            status,
            updated_at;
    """

    with get_cursor() as cursor:
        cursor.execute(
            query,
            (
                status.upper(),
                employee_id
            )
        )

        return cursor.fetchone()

