import numpy as np


def get_transf_matrix_from_res(pix_sizes):
    """ Create transformation matrix in mm
    from a dictionary of pixel sizes in um
    :param pix_sizes:
    :return:
    """
    transformation_matrix = np.eye(4)
    for i, axis in enumerate(("x", "y", "z")):
        transformation_matrix[i, i] = pix_sizes[axis] / 1000
    return transformation_matrix


def flip_multiple(data, flips):
    """Flips over each axis from list of booleans
    indicating if one axis has to be flipped
    :param data:
    :param flips:
    :return:
    """

    for axis_idx, flip_axis in enumerate(flips):
        if flip_axis:
            data = np.flip(data, axis_idx)

    return data
