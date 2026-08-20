from app.repositories.user_repository import (
    get_user_by_email,
    update_password
)
from app.auth.password import hash_password


email = "sourabh@gmail.com"
new_password = "Sourabh@123"


user = get_user_by_email(email)

if not user:
    print("User not found:", email)
else:
    user_id = user[0]

    password_hash = hash_password(new_password)

    result = update_password(
        user_id=user_id,
        password_hash=password_hash
    )

    print("Password reset successfully!")
    print("Email:", email)
    print("New password:", new_password)
    print("User ID:", user_id) 