r"""
Decorators used in this package.
"""


def static(**kwargs):
    r"""

    Args:
        **kwargs: key value pairs to add as static variables.

    Returns:

    """
    def wrap(func):
        for key, value in kwargs.items():
            setattr(func, key, value)
        return func
    return wrap
