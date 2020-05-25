# from PIL import Image
# import numpy as np
import cv2


def read_image(filename, **kwargs):
    return read_image_cv2(filename, **kwargs)


def write_image(filename, img, **kwargs):
    return write_image_cv2(filename, img, **kwargs)


def read_image_cv2(filename, flag_rgb=True, **kwargs):
    image = cv2.imread(filename, **kwargs)
    if flag_rgb:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image


def write_image_cv2(filename, img, params=None, flag_rgb=True):
    if flag_rgb:
        cv2.imwrite(filename, cv2.cvtColor(img, cv2.COLOR_RGB2BGR), params=params)
    else:
        cv2.imwrite(filename, img, params=params)


# def read_image_pil(filename) :
#     img = Image.open(filename)
#     img.load()
#     data = np.asarray(img, dtype="int32")
#     return data
#
#
# def write_image_pil(filename, np_arr):
#     img = Image.fromarray(np.asarray(np.clip(np_arr, 0, 255), dtype="uint8"), "L")
#     img.save(filename)
