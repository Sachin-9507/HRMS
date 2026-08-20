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
    emergency_contact_name,
    emergency_contact_phone,
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
            salary,
            emergency_contact_name,
            emergency_contact_phone
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
            employment_status,
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
        salary,
        emergency_contact_name,
        emergency_contact_phone,
    )

    with get_cursor() as cursor:
        cursor.execute(query, values)
        return cursor.fetchone()


def get_all_employee():
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
            e.employment_status,
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
            e.state,
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
            e.employment_status,
            e.emergency_contact_name,
            e.emergency_contact_phone,
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
    employment_status,
    emergency_contact_name,
    emergency_contact_phone,
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
            employment_status = %s,
            emergency_contact_name = %s,
            emergency_contact_phone = %s,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = %s

        RETURNING
            id,
            employee_code,
            first_name,
            last_name,
            email,
            employment_status,
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
        employment_status,
        emergency_contact_name,
        emergency_contact_phone,
        employee_id,
    )

    with get_cursor() as cursor:
        cursor.execute(query, values)
        return cursor.fetchone()


def deactivate_employee(employee_id: int):
    query = """
        UPDATE employees
        SET
            employment_status = 'INACTIVE',
            updated_at = CURRENT_TIMESTAMP
        WHERE id = %s

        RETURNING
            id,
            employee_code,
            employment_status;
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
    emergency_contact_name,
    emergency_contact_phone
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
            salary,
            emergency_contact_name,
            emergency_contact_phone
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
            employment_status,
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
                salary,
                emergency_contact_name,
                emergency_contact_phone,
            )
        )

        employee = cursor.fetchone()

        return user_id, employee

    from app.database.db import get_cursor


def get_employee_by_user_id(
    user_id: int
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
            ds.name AS designation_name,

            e.manager_id,

            CONCAT(
                m.first_name,
                ' ',
                COALESCE(m.last_name, '')
            ) AS manager_name,

            e.employment_type,
            e.status

        FROM employees e

        LEFT JOIN departments d
            ON d.id = e.department_id

        LEFT JOIN designations ds
            ON ds.id = e.designation_id

        LEFT JOIN employees m
            ON m.id = e.manager_id

        WHERE e.user_id = %s;
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
            e.first_name,
            e.last_name,
            e.email,
            e.phone,

            e.department_id,
            d.name AS department_name,

            e.designation_id,
            ds.name AS designation_name,

            e.manager_id,

            CONCAT(
                m.first_name,
                ' ',
                COALESCE(m.last_name, '')
            ) AS manager_name,

            e.joining_date,
            e.employment_type,
            e.employment_status

        FROM employees e

        LEFT JOIN departments d
            ON d.id = e.department_id

        LEFT JOIN designations ds
            ON ds.id = e.designation_id

        LEFT JOIN employees m
            ON m.id = e.manager_id

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
            AND e.employment_status = %s
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
            AND e.employment_status = %s
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


