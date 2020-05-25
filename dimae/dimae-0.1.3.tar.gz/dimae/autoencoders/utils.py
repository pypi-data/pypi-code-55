from sklearn.preprocessing import MinMaxScaler
import numpy as np


def standardize(data):
    indexes = []
    for col in range(data.shape[1]):
        if min(data[:, col]) < 0 or max(data[:, col]) > 1:
            indexes.append(col)

    if len(indexes) > 0:
        to_scale = data[:, indexes]
        not_to_scale = np.delete(data, indexes, axis=1)
        scaled = MinMaxScaler().fit_transform(to_scale)

        minmaxdata = np.concatenate((scaled, not_to_scale), axis = 1)
        return minmaxdata
    else:
        return data
