import pytest

from geospin.utilities.geometry import VG250GeometryParser


def test_contains():
    """
    Are the given locations correctly identified to (not) be in Germany?
    """
    from geospin.utilities.geometry import Germany

    lat, lon = 47.988375, 7.844821  # Freiburg
    g = Germany()
    assert g.contains(lat, lon) is True
    g = Germany(coarse=False)
    assert g.contains(lat, lon) is True

    lat, lon = 48.845455, 2.353175  # Paris
    g = Germany()
    assert g.contains(lat, lon) is False
    g = Germany(coarse=False)
    assert g.contains(lat, lon) is False


@pytest.mark.parametrize(
    'ags, expected',
    [
        ('00000000', 'STA'),
        ('06412000', 'KRS')
    ]
)
def test_vg250geometryparser_get_admin_level_suffix_from_ags_code(
        ags, expected):
    parser = VG250GeometryParser(None, None)
    result = parser._get_admin_level_suffix_from_ags_code(ags)
    assert expected == result
