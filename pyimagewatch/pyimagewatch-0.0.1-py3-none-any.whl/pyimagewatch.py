"""
Image processing debugger similar to Image Watch for Visual Studio.
"""

from functools import wraps

import cv2 as cv

# * ------------------------------------------------------------------------------ # *
# * DECORATION HELPER * #


def decorate_functions(function_names, decorator):
    "Decorates a list of functions in the cv module with a decorator."
    for function_name in function_names:
        function = getattr(cv, function_name)
        setattr(cv, function_name, decorator(function))


# * ------------------------------------------------------------------------------ # *
# * TRACKBAR * #

# * ------------------------------------------------------------------------------ # *
# * DECORATORS * #


def show(f):
    """Decorator that shows the result of a cv module function."""

    @wraps(f)
    def wrapper(*args, **kwargs):
        result = f(*args, **kwargs)
        cv.imshow(f.__name__, result)
        cv.waitKey()
        return result

    return wrapper
