from PIL import Image
import cv2
import numpy as np
import base64
from io import BytesIO


def bytes_to_str(b):
    string = b.decode("utf-8")
    return string


def str_to_bytes(string):
    b = string.encode()
    return b


def np_array_to_b64_bytes(array):
    return cv2_to_b64_bytes(array)


def np_array_to_b64_str(array):
    b = np_array_to_b64_bytes(array)
    s = bytes_to_str(b)
    return s


def b64_bytes_to_array(im_b64):
    return b64_bytes_to_cv2(im_b64)


def b64_str_to_array(im_b64):
    im_b64 = str_to_bytes(im_b64)
    array = b64_bytes_to_array(im_b64)
    return array


def pil_to_b64_bytes(im_pil):
    im_file = BytesIO()
    im_pil.save(im_file, format="JPEG")
    im_bytes = im_file.getvalue()  # im_bytes: image in binary format.
    im_b64 = base64.b64encode(im_bytes)
    return im_b64


def pil_to_b64_str(im_pil):
    im_b64 = pil_to_b64_bytes(im_pil)
    im_str = bytes_to_str(im_b64)
    return im_str


def cv2_to_b64_bytes(im_cv2):
    _, im_arr = cv2.imencode('.jpg', im_cv2)  # im_arr: image in Numpy one-dim array format.
    im_bytes = im_arr.tobytes()
    im_b64 = base64.b64encode(im_bytes)
    return im_b64


def cv2_to_b64_str(im_cv2):
    im_b64 = cv2_to_b64_bytes(im_cv2)
    im_str = bytes_to_str(im_b64)
    return im_str


def b64_bytes_to_pil(im_b64):
    im_bytes = base64.b64decode(im_b64)
    im_file = BytesIO(im_bytes)
    img = Image.open(im_file)
    return img


def b64_str_to_pil(im_b64):
    im_b64 = str_to_bytes(im_b64)
    img = b64_bytes_to_pil(im_b64)
    return img


def b64_bytes_to_cv2(im_b64):
    im_bytes = base64.b64decode(im_b64)
    im_arr = np.frombuffer(im_bytes, dtype=np.uint8)
    img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
    return img


def b64_str_to_cv2(im_b64):
    im_b64 = str_to_bytes(im_b64)
    img = b64_bytes_to_cv2(im_b64)
    return img


def file_to_b64_bytes(filename):
    with open(filename, "rb") as f:
        im_b64 = base64.b64encode(f.read())
    return im_b64


def file_to_b64_str(filename):
    b = file_to_b64_bytes(filename)
    s = bytes_to_str(b)
    return s
