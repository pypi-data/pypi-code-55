def purge_none(data):
    """
    Delete keys with the value ``None`` in a dictionary, recursively.

    fixed a stackoverflow algo
    """
    for key, value in list(data.items()):
        if isinstance(value, dict):
            purge_none(value)
        if value:
            continue
        else:
            del data[key]
