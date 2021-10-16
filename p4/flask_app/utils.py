from datetime import datetime
import io
import base64


def current_time() -> str:
    return datetime.now().strftime("%B %d, %Y at %H:%M:%S")


def get_b64_img(picture):
    bytes_im = io.BytesIO(picture.read())
    image = base64.b64encode(bytes_im.getvalue()).decode()
    return image
