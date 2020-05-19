try:
    import h3

    h3.k_ring('841e265ffffffff', 4)
except AttributeError:
    from h3 import h3

import geospin.utilities.h3.misc as misc


def test_get_geojson_dict_of_hex_id_boundary():
    hex_id = '871faec4dffffff'
    expected = {
        "type": "Polygon",
        "coordinates":
            [
                [
                    [7.970835152013785, 50.002141360693734],
                    [7.972541335884122, 49.990465220898706],
                    [7.9899218345671885, 49.98643117374083],
                    [8.005601461930373, 49.994073011636544],
                    [8.00390031820863, 50.00575014440851],
                    [7.986514505881974, 50.009784446715],
                    [7.970835152013785, 50.002141360693734]
                ]
            ]
    }
    result = misc.get_geojson_dict_of_hex_id_boundary(hex_id)
    assert expected == result
