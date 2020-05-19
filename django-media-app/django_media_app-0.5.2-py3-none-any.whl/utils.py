import os
from io import BytesIO

from PIL import Image
from django.core.files import File


def resize_image(image, quality=85, size=(256, 256), path=None):
    """Makes thumbnails of given size from given image"""

    im = Image.open(image)

    rgb_im = im.convert('RGB')  # convert mode

    rgb_im.thumbnail(size)  # resize image

    thumb_io = BytesIO()  # create a BytesIO object

    rgb_im.save(thumb_io, 'JPEG', quality=quality)  # save image to BytesIO object
    name, extension = os.path.splitext(path or image.name)
    thumbnail = File(thumb_io, name=f"{name}.{size[0]}x{size[1]}.jpg")  # create a django friendly File object

    return thumbnail
