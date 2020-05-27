import numpy as np

from imlib.cells.cells import pos_from_file_name

# planes to rotate around, for x, y, z
AXES = [(1, 2), (0, 2), (0, 1)]


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


def rotate_multiple(data, rotation_string):
    rotation_numbers = pos_from_file_name(rotation_string)
    for i in zip(AXES, rotation_numbers):
        data = rotate(data, i[0], i[1])
    return data


def rotate(data, axes, k):
    data = np.rot90(np.asanyarray(data), axes=axes, k=k)
    # data = np.swapaxes(data, 0, 1)
    return data
