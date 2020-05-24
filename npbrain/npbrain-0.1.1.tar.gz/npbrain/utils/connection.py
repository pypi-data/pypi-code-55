import numpy as np

__all__ = [
    'get_conn_by_name',
    'correspondence',

    'one2one', 'all2all',

    'grid_four', 'grid_eight', 'grid_N',

    'gaussian',
    'dog',

    'fixed_prob',

    'fixed_prenum',

    'fixed_postnum',

    'scale_free', 'small_world',
]


def get_conn_by_name(name, num_pre, num_post, *args, **kwargs):
    if name in ['one_to_one', 'one2one']:
        i, j = one2one(num_pre, num_post)
    elif name in ['all_to_all', 'all2all']:
        i, j = all2all(num_pre, num_post, *args, **kwargs)

    elif name in ['grid_four', 'grid4']:
        i, j = grid_four(*args, **kwargs)
    elif name in ['grid_eight', 'grid8']:
        i, j = grid_eight(*args, **kwargs)
    elif name in ['grid_N', ]:
        i, j = grid_N(*args, **kwargs)

    elif name in ['fixed_prob', ]:
        i, j = fixed_prob(num_pre, num_post, *args, **kwargs)
    elif name in ['fixed_prenum']:
        i, j = fixed_prenum(num_pre, num_post, *args, **kwargs)
    elif name in ['fixed_postnum']:
        i, j = fixed_postnum(num_pre, num_post, *args, **kwargs)

    else:
        raise ValueError()
    return i, j


def correspondence(num_pre, num_post, i, j):
    assert len(i) == len(j)
    pre_indexes = {i_: [] for i_ in range(num_pre)}
    post_indexes = {j_: [] for j_ in range(num_post)}
    for index, i_ in enumerate(i):
        i_ = i_
        j_ = j[index]
        pre_indexes[i_].append(index)
        post_indexes[j_].append(index)
    return pre_indexes, post_indexes


def one2one(num_pre, num_post, **kwargs):
    assert num_pre == num_post
    i = list(range(num_pre))
    j = list(range(num_post))
    return i, j


def all2all(num_pre, num_post, include_self=True, **kwargs):
    i, j = [], []
    for i_ in range(num_pre):
        for j_ in range(num_post):
            if (not include_self)  and (i_ == j_):
                continue
            else:
                i.append(i_)
                j.append(j_)
    return i, j


def grid_four(height, width, include_self=False):
    conn_i = []
    conn_j = []
    for row in range(height):
        for col in range(width):
            i_index = (row * width) + col
            if 0 <= row - 1 < height:
                j_index = ((row - 1) * width) + col
                conn_i.append(i_index)
                conn_j.append(j_index)
            if 0 <= row + 1 < height:
                j_index = ((row + 1) * width) + col
                conn_i.append(i_index)
                conn_j.append(j_index)
            if 0 <= col - 1 < width:
                j_index = (row * width) + col - 1
                conn_i.append(i_index)
                conn_j.append(j_index)
            if 0 <= col + 1 < width:
                j_index = (row * width) + col + 1
                conn_i.append(i_index)
                conn_j.append(j_index)
            if include_self:
                conn_i.append(i_index)
                conn_j.append(i_index)
    return conn_i, conn_j


def grid_eight(height, width, include_self=False):
    return grid_N(height, width, 1, include_self)


def grid_N(height, width, N=1, include_self=False):
    conn_i = []
    conn_j = []
    for row in range(height):
        for col in range(width):
            i_index = (row * width) + col
            for row_diff in [-N, 0, N]:
                for col_diff in [-N, 0, N]:
                    if (not include_self) and (row_diff == col_diff == 0):
                        continue
                    if 0 <= row + row_diff < height and 0 <= col + col_diff < width:
                        j_index = ((row + row_diff) * width) + col + col_diff
                        conn_i.append(i_index)
                        conn_j.append(j_index)
    return conn_i, conn_j


def gaussian(num_pre, num_post, **kwargs):
    i, j = [], []
    return i, j


def dog(num_pre, num_post, **kwargs):
    i, j = [], []
    return i, j


def fixed_prob(num_pre, num_post, prob, include_self=True, **kwargs):
    assert isinstance(num_pre, int)
    assert isinstance(num_post, int)
    assert isinstance(prob, (int, float))
    conn_i = []
    conn_j = []
    for i in range(num_pre):
        random_vals = np.random.random(num_post)
        idx_selected = list(np.where(random_vals < prob)[0])
        if (not include_self) and (i in idx_selected):
            idx_selected.remove(i)
        size_post = len(idx_selected)
        conn_i.extend([i] * size_post)
        conn_j.extend(idx_selected)
    return conn_i, conn_j


def fixed_prenum(num_pre, num_post, num, include_self=True, **kwargs):
    assert isinstance(num_pre, int)
    assert isinstance(num_post, int)
    assert isinstance(num, int)

    conn_i = []
    conn_j = []
    for j in range(num_post):
        idx_selected = np.random.choice(num_pre, num, replace=False).tolist()
        if (not include_self) and (j in idx_selected):
            idx_selected.remove(j)
        size_pre = len(idx_selected)
        conn_i.extend(idx_selected)
        conn_j.extend([j] * size_pre)
    return conn_i, conn_j


def fixed_postnum(num_pre, num_post, num, include_self=True, **kwargs):
    assert isinstance(num_pre, int)
    assert isinstance(num_post, int)
    assert isinstance(num, int)

    conn_i = []
    conn_j = []
    for i in range(num_pre):
        idx_selected = np.random.choice(num_post, num, replace=False).tolist()
        if (not include_self) and (i in idx_selected):
            idx_selected.remove(i)
        size_post = len(idx_selected)
        conn_i.extend([i] * size_post)
        conn_j.extend(idx_selected)
    return conn_i, conn_j


def scale_free(num_pre, num_post, **kwargs):
    conn_i = []
    conn_j = []
    return conn_i, conn_j


def small_world(num_pre, num_post, **kwargs):
    conn_i = []
    conn_j = []
    return conn_i, conn_j


if __name__ == '__main__':
    from npbrain.utils import Dict

    # ii, jj = one_to_one(6, 6)
    # ii, jj = all_to_all(6, 6)
    # ii, jj = all_to_all_no_equal(6, 6)

    # ii, jj = grid_eight(2, 2)
    # ii, jj = grid_eight(3, 3)
    # ii, jj = grid_four(3, 3)

    # ii, jj = fixed_prob(10, 10, 0.2)
    # ii, jj = fixed_prob(10, 10, 0.35)
    # ii, jj = fixed_prob_neq(10, 10, 0.2)
    # ii, jj = fixed_prob_neq(10, 10, 0.35)

    # ii, jj = fixed_prenum(10, 10, 2)
    # ii, jj = fixed_prenum_neq(10, 10, 2)

    ii, jj = fixed_postnum(10, 10, 2)
    # ii, jj = fixed_postnum_neq(10, 10, 2)

    print('ii =', ii)
    print("jj =", jj)
    print('length =', len(ii))
