import base64
from PIL import Image
import io

def encode(filepath):
    """
    Takes in a filepath

    Returns a string representation of base64 encoded bytes
    """
    with open(filepath, "rb") as image_file:
        return str(base64.b64encode(image_file.read()))

def decode(encoded_string):
    """
    Takes an encoded encoded_string

    Returns a PIL Image
    """
    return Image.open(io.BytesIO(base64.decodestring(encoded_string[2:].encode("utf-8"))))
