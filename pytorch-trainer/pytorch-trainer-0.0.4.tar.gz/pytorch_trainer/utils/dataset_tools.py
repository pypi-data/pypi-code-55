import random
import numpy as np
import torch
import cv2

def resize(img, boxes, size, max_size=1000):
    '''Resize the input cv2 image to the given size.

    Args:
      img: (cv2) image to be resized.
      boxes: (tensor) object boxes, sized [#ojb,4].
      size: (tuple or int)
        - if is tuple, resize image to the size.
        - if is int, resize the shorter side to the size while maintaining the aspect ratio.
      max_size: (int) when size is int, limit the image longer size to max_size.
                This is essential to limit the usage of GPU memory.
    Returns:
      img: (cv2) resized image.
      boxes: (tensor) resized boxes.
    '''
    height, width, _ = img.shape
    if isinstance(size, int):
        size_min = min(width, height)
        size_max = max(width, height)
        scale_w = scale_h = float(size) / size_min
        if scale_w * size_max > max_size:
            scale_w = scale_h = float(max_size) / size_max
        new_width = int(width * scale_w + 0.5)
        new_height = int(height * scale_h + 0.5)
    else:
        new_width, new_height = size
        scale_w = float(new_width) / width
        scale_h = float(new_height) / height

    return cv2.resize(img, (new_height, new_width)), \
           boxes * torch.Tensor([scale_w, scale_h, scale_w, scale_h])


def random_flip(img, bbox):
    '''Randomly flip the given image tensor

    Args:
        img (tensor): image tensor. shape (3, height, width)
        bbox (tensor): bounding box tensor

    Returns:
        img (tensor): randomaly fliped image tensor.
        bbox (tensor): randomaly fliped bounding box tensor
    '''
    if random.random() < 0.5:

        _, width = img.shape[-2:]
        img = img.flip(-1)
        bbox[:, [0, 2]] = width - bbox[:, [2, 0]]
        
    return img, bbox


def collate_fn(batch):
    return tuple(zip(*batch))