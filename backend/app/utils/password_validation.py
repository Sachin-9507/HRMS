def validate_password(
    password: str
):

    if len(password) < 8:

        return False, (
            "Password must contain "
            "at least 8 characters"
        )

    if not any(
        char.isupper()
        for char in password
    ):

        return False, (
            "Password must contain "
            "an uppercase letter"
        )

    if not any(
        char.islower()
        for char in password
    ):

        return False, (
            "Password must contain "
            "a lowercase letter"
        )

    if not any(
        char.isdigit()
        for char in password
    ):

        return False, (
            "Password must contain "
            "a number"
        )

    if not any(
        not char.isalnum()
        for char in password
    ):

        return False, (
            "Password must contain "
            "a special character"
        )

    return True, None