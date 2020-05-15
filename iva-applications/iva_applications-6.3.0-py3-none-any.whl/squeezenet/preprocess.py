# -*- coding=utf-8 -*-
"""SQUEEZENET preprocess."""
import numpy as np
from PIL import Image


def image_to_tensor(image: Image) -> np.ndarray:
    """
    Realise preprocess for an input pillow image and convert it to numpy array.

    Parameters
    ----------
    image
        An input image to be processed.

    Returns
    -------
    tensor
        Preprocessed numpy array.
    """
    mean = [103.939, 116.779, 123.68]
    image = image.resize((227, 227))
    image = image.convert('RGB')
    tensor = np.asarray(image)
    tensor = tensor[..., ::-1]
    tensor = tensor - np.array(mean)
    assert tensor.shape == (227, 227, 3)
    return tensor
