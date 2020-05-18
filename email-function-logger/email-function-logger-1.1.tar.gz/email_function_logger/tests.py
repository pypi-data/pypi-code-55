from .function_logger import log_function


@log_function
def mult(x, y):
    # Function text output
    print(x)
    print(y)

    # Value returned by function
    return x * y


mult(9, 7)
