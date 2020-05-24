def to_php(x):
    if type(x) == str:
        return '\'{0}\''.format(x)
    if type(x) == bool:
        if x:
            return 'TRUE'
        else:
            return 'FALSE'
    if x is None:
        return 'null'
    raise ValueError('dont know how to translate type', type(x), x)
