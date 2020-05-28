from text_viewer.alphabet import alphabet
from text_viewer.operations import join_horizontally


def display(*args, **kwargs):
    print(*args, sep='\n', end='\n\n', **kwargs)


def prepare_table(table, converters=None):
    converters = converters if converters else [str] * len(table[0])
    return tuple(tuple(converters[i](element) for i, element in enumerate(row)) for row in table)


def text_table(table, spacing=2, converters='required'):
    if not table:
        return ()

    if converters == 'required':
        converters = (str, ) * len(table[0])

    if converters:
        return text_table(prepare_table(table, converters), spacing, converters=None)

    columns_sizes = [0] * len(table[0])

    for row in table:
        for i, element in enumerate(row):
            if len(element) > columns_sizes[i]:
                columns_sizes[i] = len(element)

    return tuple(
        (' ' * spacing).join(
            element + (columns_sizes[i] - len(element)) * ' ' for i, element in enumerate(row)
        ) for row in table
    )


def text_text(text):
    return join_horizontally(alphabet[letter] for letter in text.lower())


def text_natural_function(*values):
    maximal = max(values)
    return join_horizontally(((' ', ) * (maximal - v) + ('#', ) * v for v in values), spacing=0)
