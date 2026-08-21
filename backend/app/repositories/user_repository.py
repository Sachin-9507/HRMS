from app.database.db import get_cursor
from app.auth.password import hash_password 


def get_user_by_email(email):
    query = """
        SELECT
            id,
            email,
            password_hash,
            first_name,
            last_name,
            phone_number,
            role_id,
            is_active,
            is_email_verified,
            is_2fa_enabled,
            failed_login_attempts,
            locked_until,
            last_login,
            created_at,
            updated_at
        FROM public.users
        WHERE email = %s
    """

    with get_cursor() as cursor:
        cursor.execute(query, (email,))
        return cursor.fetchone()

def create_user(
    email:str,
    password_hash: str,
    first_name: str,
    last_name: str,
    phone: str | None,
    role_id: int
 ):
  query  =  """
    INSERT INTO users (
      email,
      password_hash,
      first_name,
      last_name,
      phone_number,
      role_id
    ) VALUES (%s, %s, %s, %s, %s, %s)
    RETURNING
      id,
      email,
      first_name,
      last_name,
      phone_number,
      role_id,
      is_active,
      is_email_verified,
      is_2fa_enabled,
      created_at;
  """

  with get_cursor() as cursor:
    cursor.execute(
    query, 
    (
       email,
       password_hash,
        first_name, 
        last_name,
          phone,
            role_id
        )
    )
    return cursor.fetchone() 




def get_role_by_name(role_name: str):
    query = """
        SELECT id, name
        FROM roles
        WHERE name = %s
          AND is_active = TRUE
        LIMIT 1;
    """

    with get_cursor() as cursor:
        cursor.execute(query, (role_name,))
        return cursor.fetchone()


def create_refresh_token_record(
    user_id: int,
    token_hash: str,
    expires_at
):
    query = """
        INSERT INTO refresh_tokens (
            user_id,
            token_hash,
            expires_at
        )
        VALUES (%s, %s, %s)
        RETURNING
            id,
            user_id,
            expires_at,
            created_at;
    """

    with get_cursor() as cursor:
        cursor.execute(
            query,
            (
                user_id,
                token_hash,
                expires_at
            )
        )
        return cursor.fetchone()


def get_refresh_token(token_hash: str):
    query = """
        SELECT
            id,
            user_id,
            token_hash,
            expires_at,
            revoked_at
        FROM refresh_tokens
        WHERE token_hash = %s
        LIMIT 1;
    """

    with get_cursor() as cursor:
        cursor.execute(
            query,
            (token_hash,)
        )
        return cursor.fetchone()


def revoke_refresh_token(token_hash: str):
    query = """
        UPDATE refresh_tokens
        SET revoked_at = CURRENT_TIMESTAMP
        WHERE token_hash = %s
          AND revoked_at IS NULL;
    """

    with get_cursor() as cursor:
        cursor.execute(
            query,
            (token_hash,)
        )


def create_otp(
    user_id: int,
    otp_hash: str,
    purpose: str,
    expires_at
):
    query = """
    INSERT INTO users_otps (
        user_id,
        otp_code_hash,
        purpose,
        expires_at
    )
    VALUES (%s, %s, %s, %s)
    RETURNING
        id,
        user_id,
        purpose,
        expires_at,
        created_at;
    """

    with get_cursor() as cursor:
        cursor.execute(
            query,
            (
                user_id,
                otp_hash,
                purpose,
                expires_at
            )
        )
        return cursor.fetchone()


def get_latest_otp(
    user_id: int,
    purpose: str
):
    query = """
    SELECT
        id,
        otp_code_hash,
        expires_at,
        attempts,
        id_used
    FROM users_otps
    WHERE user_id = %s
      AND purpose = %s
      AND id_used = FALSE
    ORDER BY created_at DESC
    LIMIT 1;
    """

    with get_cursor() as cursor:
        cursor.execute(
            query,
            (
                user_id,
                purpose
            )
        )
        return cursor.fetchone()


def mark_otp_used(
    otp_id: int
):
    query = """
    UPDATE users_otps
    SET id_used = TRUE
    WHERE id = %s;
    """

    with get_cursor() as cursor:
        cursor.execute(
            query,
            (otp_id,)
        )


def increment_otp_attempts(
    otp_id: int
):
    query = """
    UPDATE users_otps
    SET attempts = attempts + 1
    WHERE id = %s;
    """

    with get_cursor() as cursor:
        cursor.execute(
            query,
            (otp_id,)
        )


def invalidate_previous_otps(
    user_id: int,
    purpose: str
):
    query = """
    UPDATE users_otps
    SET id_used = TRUE
    WHERE user_id = %s
    AND purpose = %s
    AND id_used = FALSE;
    """
 
    with get_cursor() as cursor:
        cursor.execute(
            query,
            (
                user_id,
                purpose
            )
        )


def get_user_by_id(user_id: int):
    query = """
    SELECT
        id,
        email,
        password_hash,
        first_name,
        last_name,
        phone_number,
        role_id,
        is_active,
        is_email_verified,
        is_2fa_enabled,
        two_factor_secret,
        failed_login_attempts,
        locked_until,
        last_login,
        created_at,
        updated_at
    FROM public.users
    WHERE id = %s
    LIMIT 1;
    """

    with get_cursor() as cursor:
        cursor.execute(
            query,
            (user_id,)
        )

        return cursor.fetchone()

def get_employee_role():

    query = """
        SELECT
            id,
            name
        FROM roles
        WHERE name = 'Employee'
          AND is_active = TRUE
        LIMIT 1;
    """

    with get_cursor() as cursor:

        cursor.execute(query)

        return cursor.fetchone()

def get_user_auth_data(
    email: str
):

    query = """
        SELECT
            u.id,
            u.email,
            u.password_hash,
            u.role_id,
            u.is_active,
            u.is_email_verified,
            u.is_2fa_enabled,
            u.two_factor_secret,
            u.two_factor_verified,
            u.two_factor_backup_codes,
            u.must_change_password
        FROM users u
        WHERE u.email = %s
        LIMIT 1;
    """

    with get_cursor() as cursor:

        cursor.execute(
            query,
            (email,)
        )

        return cursor.fetchone()

def update_password(
    user_id: int,
    password_hash: str
):

    query = """
        UPDATE users

        SET
            password_hash = %s,
            must_change_password = FALSE,
            password_changed_at = CURRENT_TIMESTAMP,
            password_expires_at =
                CURRENT_TIMESTAMP
                + INTERVAL '90 days'

        WHERE id = %s

        RETURNING
            id,
            email,
            must_change_password,
            password_changed_at,
            password_expires_at;
    """

    with get_cursor() as cursor:

        cursor.execute(
            query,
            (
                password_hash,
                user_id
            )
        )

        return cursor.fetchone() 

def save_two_factor_secret(
    user_id: int,
    secret: str
):

    query = """
        UPDATE users

        SET
            two_factor_secret = %s,
            two_factor_verified = FALSE

        WHERE id = %s

        RETURNING
            id,
            email,
            two_factor_secret;
    """

    with get_cursor() as cursor:

        cursor.execute(
            query,
            (
                secret,
                user_id
            )
        )

        return cursor.fetchone()

def confirm_two_factor(
    user_id: int,
    backup_codes: str
):

    query = """
        UPDATE users

        SET
            is_2fa_enabled = TRUE,
            two_factor_verified = TRUE,
            two_factor_backup_codes = %s

        WHERE id = %s

        RETURNING
            id,
            email,
            is_2fa_enabled,
            two_factor_verified;
    """

    with get_cursor() as cursor:

        cursor.execute(
            query,
            (
                backup_codes,
                user_id
            )
        )

        return cursor.fetchone()

def get_user_by_email_cursor(
    cursor,
    email: str
):

    query = """
        SELECT
            id,
            email,
            password_hash,
            is_active,
            is_verified,
            must_change_password
        FROM users
        WHERE LOWER(email) = LOWER(%s)
        LIMIT 1
    """

    cursor.execute(
        query,
        (email,)
    )

    return cursor.fetchone()

from app.database.db import get_cursor


def create_user_cursor(
    cursor,
    email,
    password_hash,
    first_name,
    last_name,
    phone_number,
    role_id
):
    with get_cursor() as cursor:

        query = """
            INSERT INTO users
            (
                email,
                password_hash,
                first_name,
                last_name,
                phone_number,
                role_id
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id;
        """

        cursor.execute(
            query,
            (
                email,
                password_hash,
                first_name,
                last_name,
                phone_number,
                role_id
            )
        )

        user_id = cursor.fetchone()[0]

        return user_id