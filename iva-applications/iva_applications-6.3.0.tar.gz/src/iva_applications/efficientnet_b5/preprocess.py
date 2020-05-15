# -*- coding=utf-8 -*-
"""Efficientnet_b5 preprocessing."""
import numpy as np
from PIL import Image
from iva_applications.imagenet.images_utils import crop_and_resize


def image_to_tensor(image: Image) -> np.ndarray:
    """
    Realise preprocess for an input pillow image and convert it to numpy array.

    Parameters
    ----------
    image
        An input image to be processed.

    Returns
    -------
        Preprocessed numpy array.
    """
    mean = [0.485, 0.456, 0.406]
    std = [0.229, 0.224, 0.225]
    image = image.convert('RGB')
    tensor = np.asarray(image)
    tensor = crop_and_resize(tensor, 456)
    tensor = tensor / 255.
    tensor[..., 0] -= mean[0]
    tensor[..., 1] -= mean[1]
    tensor[..., 2] -= mean[2]
    tensor[..., 0] /= std[0]
    tensor[..., 1] /= std[1]
    tensor[..., 2] /= std[2]
    assert tensor.shape == (456, 456, 3)
    return tensor
