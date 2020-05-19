__version__ = "0.1.dev3"


def test_function(parameter=1.0):
    """Test the auto-doc feature with sphinx documentations.

    Keyword arguments:
      parameter -- a random test parameter

    :param my_arg: The first of my arguments.
    :param my_other_arg: The second of my arguments.

    :returns: A message (just for me, of course).

    Calls the :py:func:`test_function` if called with **the** parameter 42.

    See https://sphinx-rtd-theme.readthedocs.io/en/latest/demo/api.html
    for syntax examples.
    """
    if parameter == 42:
        test_function()

    return parameter
