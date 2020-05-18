from collections import Counter
import numpy as np


def to_categorical_list(input_list):
    result = [0] * len(input_list)
    keys = {}
    for idx, el in enumerate(input_list):
        if el in keys:
            result[idx] = keys[el]
        else:
            keys[el] = len(keys)
            result[idx] = keys[el]
    return result, keys


def to_categorical_list_2d(input_list, num_of_sort=-1):
    num_list, keys = to_categorical_list(input_list)
    if num_of_sort <= 0:
        result = np.zeros(shape=(len(input_list), len(keys)))
    else:
        result = np.zeros(shape=(len(input_list), num_of_sort))
    for i in range(len(input_list)):
        result[i][num_list[i]] = 1
    return result.astype(int), keys


def change_categorical_pandas(input_pandas, categorize=None):
    num_object = 0
    num_other = 0
    strange_dict = {}
    key_result = {}
    for col_name, col_contents in input_pandas.iteritems():
        tp = col_contents.dtype
        if tp != float and tp != int:
            try:
                tmp = col_contents.astype(float)
                input_pandas[col_name] = tmp
            except ValueError:
                if tp == object:
                    num_object += 1
                else:
                    num_other += 1
                strange_dict[col_name] = Counter(col_contents)
    print("number of object column\t", num_object)
    print("number of other column\t", num_other)
    while True:
        if categorize is not None:
            var = "y"
        else:
            print("The number of columns which are not int or float :", len(strange_dict))
            print("Do you want to inspect?")
            print("y : yes / n : no / s : list of columns name")
            var = input()
        if var == "y":
            for key, value in strange_dict.items():
                while True:
                    if categorize is not None:
                        var = "1"
                    else:
                        print(key, "\t: number of sort : ", len(value))
                        var = input("categorize(1) / want to see(2) / Don't do anything(3) : ")
                    if var == "1":
                        result3, my_keys = to_categorical_list(input_pandas[key])
                        input_pandas[key] = result3
                        key_result[key] = my_keys
                        break
                    elif var == "2":
                        print(value)
                    elif var == "3":
                        break
                    else:
                        print("Press one of three options (1,2,3)")
            break
        elif var == "n":
            break
        elif var == "s":
            print(strange_dict.keys())
        else:
            print("Press one of three options (y, n, s)")
    return key_result


def row_slice1(data: list, length: int, number_of_row_data: int, result_as_starting_pts: bool = False) -> list:
    d = len(data)

    if d < length:
        raise AssertionError("Too big length")
    if number_of_row_data <= 0:
        raise AssertionError("Wrong number_of_row_data : number_of_row_data should be integer larger then 1.")

    if number_of_row_data == 1:
        starting_pt = round((d - length) / 2)
        if result_as_starting_pts:
            return [starting_pt]
        else:
            return [data[starting_pt:starting_pt + length]]
    x = (d - number_of_row_data * length) / (number_of_row_data - 1)
    starting_pts = [round(k * (length + x)) for k in range(number_of_row_data)]
    try:
        assert len(starting_pts) == len(set(starting_pts))
    except AssertionError:
        raise AssertionError("Too many number_of_row_data : duplicate row made")
    if result_as_starting_pts:
        return starting_pts
    else:
        return [data[el: el + length] for el in starting_pts]


def row_slice2(data: list, stride: int, length: int, result_as_starting_pts: bool = False) -> list:
    d = len(data)
    if d < length:
        raise ValueError("Too big length")
    if stride <= 0:
        raise ValueError("stride should be larger than 0")

    starting_pts = list(range(len(data)))[:-length + 1:stride]
    if result_as_starting_pts:
        return starting_pts
    else:
        return [data[el: el + length] for el in starting_pts]


def confusion_matrix(y_true: list, y_pred: list, num_of_sort: int = None, normalize_axis: int = None) -> np.array:
    if len(y_true) != len(y_pred):
        raise ValueError("the length of y_true should be the same as the length of y_pred")
    for el1, el2 in zip(y_true, y_pred):
        if el1 < 0 or el2 < 0:
            raise ValueError("element of list should be positive integer")
    maximum_plus_1 = max(np.max(y_true), np.max(y_pred)) + 1
    if num_of_sort is None:
        result = np.zeros(shape=(maximum_plus_1, maximum_plus_1)).astype(int)
    else:
        if num_of_sort < maximum_plus_1:
            raise ValueError("num_of_sort < maximum + 1")
        result = np.zeros(shape=(num_of_sort, num_of_sort)).astype(int)
    for i in range(len(y_true)):
        result[y_true[i], y_pred[i]] += 1
    length_of_result = len(result)

    if normalize_axis is None:
        return result
    elif normalize_axis is 0:
        result = result.astype(float)
        for i in range(length_of_result):
            row_sum = np.sum(result[i])
            if row_sum != 0:
                result[i] = result[i] / row_sum
        return result
    elif normalize_axis is 1:
        result = result.astype(float)
        for i in range(length_of_result):
            column_sum = np.sum(result[:, i])
            if column_sum != 0:
                result[:, i] = result[:, i] / column_sum
        return result
    else:
        raise ValueError("normalize_axis should be either 0 or 1")


def plot_confusion_matrix(confusion_matrix_input, labels=None, vmin=None, vmax=None, cmap=None, center=None,
                          robust=False, annot=None, fmt='.2g', annot_kws=None, linewidths=0, linecolor='white',
                          cbar=True, cbar_kws=None, cbar_ax=None, square=False, xticklabels='auto', yticklabels='auto',
                          mask=None, ax=None):
    import seaborn as sn
    if labels is None:
        return sn.heatmap(confusion_matrix_input, vmin, vmax, cmap, center, robust, annot, fmt, annot_kws, linewidths,
                          linecolor, cbar, cbar_kws, cbar_ax, square, xticklabels, yticklabels, mask, ax)
    else:
        return sn.heatmap(confusion_matrix_input, vmin, vmax, cmap, center, robust, annot, fmt, annot_kws, linewidths,
                          linecolor, cbar, cbar_kws, cbar_ax, square, labels, labels, mask, ax)
