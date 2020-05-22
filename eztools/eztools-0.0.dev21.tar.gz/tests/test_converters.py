from eztools import converters


def test_to_int():
    assert converters.to_int(123) == 123
