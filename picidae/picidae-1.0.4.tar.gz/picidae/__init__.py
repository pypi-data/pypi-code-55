def echo(x):
    """
    takes an object and returns it. Useful in the case where a dummy operation is needed to satisfy an interface
    :param x: object to echo
    :return: x
    """
    return x

def lazily_echo(x):
    """
    lazily takes an object and returns it. Useful in the case where a dummy operation is needed to satisfy an interface
    :param x: object to echo
    :return: x
    """
    def nested(_):
        return x
    return nested

def compose(x, *funcs):
    """
    takes an initial value and a list of functions and composes those functions on the initial value
    :param x: object to call the composed functions on
    :param funcs: list of functions to compose
    :return: final output of composition
    """
    for func in funcs:
        x = func(x)
    return x

def lazily_compose_given_functions(*functions):
    """
    takes a list of functions and returns a function that takes an initial value to composes those functions on
    :param functions: list of functions to compose
    :return: nested function to be called with initial value to compose on
    """
    def nested(x):
        return compose(x, *functions)
    return nested

def lazily_compose_given_value(x):
    """
    takes an initial value and returns a function that takes a list of functions and composes those functions on the initial value
    :param x: object to call te composed functions on
    :return: nested function to be called with functions to compose
    """
    def nested(*functions):
        return compose(x, *functions)
    return nested


def access_attribute(attribute_name, pre_operation=echo, post_operation=echo):
    """
    a higher order function that returns a nested function which attempt to access an attribute on an object passed into it
    :param attribute_name: name of the attribute to access
    :param pre_operation: an operation on object before processing
    :param post_operation: an operation on object after processing
    :return: an object returned by the attribute to access
    """
    def nested(x):
        pre = pre_operation(x)
        ret = getattr(pre, attribute_name)
        return post_operation(ret)
    return nested

def to_bool(x, pre_operation=echo, post_operation=echo):
    """
    explicitly calls bool on object
    :param x: object to call bool on
    :param pre_operation: an operation on object before processing
    :param post_operation: an operation on object after processing
    :return: 
    """
    pre = pre_operation(x)
    ret = bool(pre)
    return post_operation(ret)