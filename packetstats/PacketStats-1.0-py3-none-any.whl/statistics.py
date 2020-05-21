import pandas as pd
import itertools


#
def get_range_of_data(percentage_list, move=0, percentage=20):
    """Generating range of data with custom percentage

    :param percentage_list: list of str

    :param move: int
        defines the position of data (default is 0)
        0 -> top,
        1 -> last,
        -1 -> range
    :param percentage: int
        percent value [0-100] of how many data is needed  (default is 20)
    :return: list range of data based on custom percentage
    :rtype: list
        """
    data = []
    i = 0 if move == 0 else len(percentage_list) - 1

    if move == 0 or move == 1:
        while sum(item[1] for item in data) < percentage:
            data.append(percentage_list[i])
            i += 1 if move == 0 else -1
    else:
        i = 0
        while sum(item[1] for item in data) < percentage:
            data.append(percentage_list[i])
            i += 1

        data2 = []
        i = len(percentage_list) - 1
        while sum(item[1] for item in data2) < percentage:
            data2.append(percentage_list[i])
            i -= 1

        return [item for item in percentage_list if item not in data and item not in data2]

    return data


# Generating percentage for each row
def calculate_percentage(series):
    result = sorted(list(series), key=lambda x: x[1], reverse=True)
    sum = (sum(item[1] for item in result))
    resultPercentage = [(i[0], 100.0 * i[1] / sum) for i in result]
    return resultPercentage


# Generate statistics
def statistics(f_name, header_names):
    dataset = pd.read_csv(f_name, delimiter='\t')

    # Delete time
    if len(header_names) > 4: header_names.pop(0)

    # Prepare data formats
    dataset = dataset.astype({"length": int, "port-source": int, "port-dest": int})
    dataset["ip-src"] = dataset["ip-src"].apply(lambda a: a.split(',')[0] if ',' in a else a)

    # Statistics
    print(dataset.describe())

    # Data counts
    series_list = []
    for name in header_names:
        # print("\n--------------- %s ---------------\n" %(name))
        series_list.append(calculate_percentage(dataset[name].value_counts().items()))

    return series_list


# Print data with percentage
def print_data(series_list, header_names, move=0, percentage=20):
    i = 0
    for series in series_list:
        print(header_names[i])
        result = get_range_of_data(series, move, percentage)
        # print(result)
        print(sum(it[1] for it in result))
        for id, val in result:
            print("%s\t%s" % (id, val))
        i += 1


def non_increasing(values, length):
    if length == 1:
        for value in values:
            yield value,
    else:
        for index, value in enumerate(values, 1):
            for rest in non_increasing(values[:index], length - 1):
                yield (value,) + rest


def gen_combos(values, length):
    max_val = max(values),
    min_val = min(values),
    for first_chunk in non_increasing(values, 8):
        for second_chunk in non_increasing(values, length - 10):
            yield max_val + first_chunk + second_chunk + min_val


def permutations(series_list, header_names, move=0, percentage=20):
    result = [[item[0] for item in get_range_of_data(series, move, percentage)] for series in series_list]
    print(result)
    return itertools.product(*result)
