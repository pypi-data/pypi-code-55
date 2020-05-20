from .use_cases import GetFeature


def flag_on(key: str) -> bool:
    """Enable or disable a feature.

    Example:
    ::
        if flag_on('MY_KEY'):
            pass

    Args:
        key (str):

    Returns:
        bool:
    """
    use_case = GetFeature()
    return use_case.handle(key)
