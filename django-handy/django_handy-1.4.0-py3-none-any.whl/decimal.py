from decimal import Decimal


def d_round(value, places=2):
    """Decimal version of round() builtin"""
    assert isinstance(places, int)
    quantize_to = Decimal(10) ** (-places)
    return Decimal(value).quantize(quantize_to)
