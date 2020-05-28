# SPDX-FileCopyrightText: 2020 G2Elab / MAGE
#
# SPDX-License-Identifier: Apache-2.0

import autograd.numpy as np
def flatten(seq):
    res = []
    shape =[]
    for item in seq:
        if (isinstance(item, np.numpy_boxes.ArrayBox)):
            if item.size == 1:
                res.append(item)
                shape.append(0)
            else:
                sub_res, sub_shap = flatten(item)
                if len(sub_res) != item.size:
                    raise ValueError('only 2 levels ragged list: scalar and vector allowed')
                shape.append(item.size)  # TODO le recursif ne fonctionne que pour des scalaires et vecteurs
                res.extend(sub_res)
        else :
            if (isinstance(item, (tuple, list, np.ndarray))):
                sub_res, sub_shap = flatten(item)
                if len(sub_res)!=len(item):
                    raise ValueError('only 2 levels ragged list: scalar and vector allowed')
                shape.append(len(item)) #TODO le recursif ne fonctionne que pour des scalaires et vecteurs
                res.extend(sub_res)
            else:
                res.append(item)
                shape.append(0)
    return res, shape



def unflatten(seq, shape):
    res = []
    i = 0
    for size in shape:
        if size==0:
            res.append(seq[i])
            i = i+1
        else:
            res.append(seq[i:i+size])
            i = i + size
    return res


if __name__ == "__main__":
    seq = [1, [1], [2,3], 4, [5, 6, 7], np.array([1, 2])] #, [[1], 2, [3, [4]]]]
    print("original:\t", seq)
    res, shap = flatten(seq)
    print("flattened:\t", res)
    print("shape:\t\t", shap)

    seq2 = unflatten(res, shap)
    print("unflattened:", seq2)
