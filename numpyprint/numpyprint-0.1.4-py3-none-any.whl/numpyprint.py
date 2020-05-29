from prettytable import PrettyTable, MSWORD_FRIENDLY, PLAIN_COLUMNS, DEFAULT, FRAME, HEADER, ALL, NONE
import numpy as np
from functools import reduce
from operator import mul


defaults=dict({
    'row_numbers': True,
    'column_numbers': False,
    'precision': None,
    'style': 'default',
    'odd_vertical': True
})

class printableObject():

    def __init__(self, data_to_print=''):
        self.data_to_print = data_to_print

    def __str__(self):
        return self.data_to_print.get_string()

    def _repr_(self):
        return self.data_to_print

    def _repr_html_(self):
        return self.data_to_print.get_html_string()


def get_table(rows, precision, row_numbers, column_numbers, style):
    x = PrettyTable(header=column_numbers, align='r')

    if precision is not None:
        x.float_format='.' + str(precision)

    if style == 'plain':
        x.header = False
        column_numbers = False
        row_numbers = False
        x.hrules = NONE
        x.vrules = NONE

    if column_numbers:
        names = []
        if row_numbers:
            names.append('-')
        names.extend(list(range(0, len(rows[0]))))
        x.field_names = names

    for i, row in enumerate(rows):
        temp = []
        if row_numbers:
            temp.append(i)
        temp.extend(row)

        x.add_row(temp)

    return x


def np_format(array, precision=None, row_numbers=None, column_numbers=None, odd_vertical=None, style=None):
    array = np.asarray(array)

    if precision is None:
        precision = defaults['precision']
    if row_numbers is None:
        row_numbers = defaults['row_numbers']
    if column_numbers is None:
        column_numbers = defaults['column_numbers']
    if odd_vertical is None:
        odd_vertical = defaults['odd_vertical']
    if style is None:
        style = defaults['style']

    print(defaults, row_numbers)
    shape = np.array(array.shape)
    is_even = len(shape) % 2 == 0

    if not is_even:
        if odd_vertical:
            array = array.reshape(np.append(shape, 1))
        else:
            array = array.reshape(np.insert(shape, -1, 1))
        shape = np.array(array.shape)

    groups = np.array_split(shape, np.math.ceil(len(shape) / 2))
    groups.reverse()

    if precision is not None:
        array = np.around(array, precision)

    tables = array
    for i, group in enumerate(groups):
        fac = reduce(mul, shape[:-1 - i * 2])

        if len(groups) > i + 1:
            split = fac / groups[i][0]
        else:
            split = 1

        rows = np.array_split(np.array(tables).reshape(int(fac), group[1]), split)

        tables = []
        for array in rows:
            tables.append(get_table(array, precision, row_numbers, column_numbers, style))

    return tables[0]


def np_display(array, precision=None, row_numbers=None, column_numbers=None, odd_vertical=None, style=None):
    display(printableObject(np_format(array, precision, row_numbers, column_numbers, odd_vertical, style)))


def np_print(array, precision=None, row_numbers=None, column_numbers=None, odd_vertical=None, style=None):
    print(printableObject(np_format(array, precision, row_numbers, column_numbers, odd_vertical, style)))
