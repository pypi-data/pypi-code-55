from re import search


def decimal_degree_validate(coordinate):
    """
    Tests if a decimal degree coordinate is in a valid format and is a valid number.

    Parameters
    ----------
    coordinate : str or int or float
        example: "-71.070951"

    Returns
    -------
    valid_coordinate : float
        Valid coordinate as a float

    """

    error_msg = f"Coordinate '{coordinate}' is not a valid Decimal Degree coordinate."

    if isinstance(coordinate, str):
        match = search(r"\A[-+]?\d+\.?\d*", coordinate)

        if match is None:
            raise ValueError(error_msg)
        else:
            valid_portion = match.group(0)

        if len(valid_portion) == len(coordinate):
            valid_coordinate = float(valid_portion)
        else:
            raise ValueError(error_msg)

    elif isinstance(coordinate, (float, int)):
        valid_coordinate = coordinate

    else:
        raise ValueError(error_msg)

    return valid_coordinate
