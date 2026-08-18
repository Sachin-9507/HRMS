import secrets


def generate_backup_codes(
    count: int = 10
):

    codes = []

    for _ in range(count):

        code = (
            secrets.token_hex(4)
            .upper()
        )

        codes.append(code)

    return codes