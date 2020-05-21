def psia_to_Paa(P):
    """

    :param P: pressure in psia
    :return: pressure in Pa (absolute)
    """
    return P / 14.5038 * 1e5


def Paa_to_psia(P):
    """

    :param P: pressure in Pa (absolute)
    :return: pressure in psia
    """
    return P / 1e5 * 14.5038


def Rankine_to_Kelvin(T):
    """

    :param T: temperature in Rankine
    :return: temperature in Kelvin
    """
    return T / 1.8


def Kelvin_to_Rankine(T):
    """

    :param T: temperature in Kelvin
    :return: temperature in Rankine
    """
    return T * 1.8
