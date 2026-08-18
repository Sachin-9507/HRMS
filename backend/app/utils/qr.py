import io

import qrcode


def generate_qr_code(
    data: str
):

    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5
    )

    qr.add_data(data)

    qr.make(
        fit=True
    )

    image = qr.make_image()

    buffer = io.BytesIO()

    image.save(
        buffer,
        format="PNG"
    )

    buffer.seek(0)

    return buffer