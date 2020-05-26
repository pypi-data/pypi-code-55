from functools import reduce

_join_function = lambda v, f: f(v)

def compose(*functions):
    return lambda val: reduce(_join_function, functions[::-1], val)

def rcompose(*functions):
    return lambda val: reduce(_join_function, functions, val)
