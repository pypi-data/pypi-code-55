import sys

from numpy.testing import assert_almost_equal as aae

from pytest import raises

sys.path.insert(0, '..')

from calorimeter.scan import scans_from_csvs


def test_read_csv():
    scans = scans_from_csvs('tests/files/6HAW158.csv', 'tests/files/7HAW008-2.csv')
    assert len(scans) == 2


def test_iter():
    a, b = scans_from_csvs('tests/files/6HAW158.csv', 'tests/files/7HAW008-2.csv')
    for temp, heat_flow in a:
        continue
    for temp, heat_flow in a:
        continue


def test_eq():
    a1, b1 = scans_from_csvs('tests/files/6HAW158.csv', 'tests/files/7HAW008-2.csv')
    a2, b2 = scans_from_csvs('tests/files/6HAW158.csv', 'tests/files/7HAW008-2.csv')
    assert a1 == a1
    assert b1 == b1
    assert a1 == a2
    assert b1 == b2
    assert a1 != b1
    assert a1 != b2
    assert a2 != b1
    assert a2 != b2


def test_len():
    a, b = scans_from_csvs('tests/files/6HAW158.csv', 'tests/files/7HAW008-2.csv')
    assert len(a) == 271
    assert len(b) == 240


def test_str():
    a, b = scans_from_csvs('tests/files/6HAW158.csv', 'tests/files/7HAW008-2.csv')
    assert len(str(a).split('\n')) == len(a) + 1
    assert len(str(b).split('\n')) == len(b) + 1


def test_add():
    a, b = scans_from_csvs('tests/files/6HAW158.csv', 'tests/files/7HAW008-2.csv')

    with raises(NotImplementedError):
        a + b

    assert (a + a) == a*2
    assert (b + b) == b*2
    assert a + a != a
    assert b + b != b


def test_sub():
    a, b = scans_from_csvs('tests/files/6HAW158.csv', 'tests/files/7HAW008-2.csv')

    with raises(NotImplementedError):
        a - b

    aae((a - a).heat_flows, 0)
    aae((b - b).heat_flows, 0)


def test_mul():
    a, b = scans_from_csvs('tests/files/6HAW158.csv', 'tests/files/7HAW008-2.csv')

    with raises(NotImplementedError):
        a * b

    a * a
    b * b


def test__heat_flows():
    a, b = scans_from_csvs('tests/files/6HAW158.csv', 'tests/files/7HAW008-2.csv')
    assert a._heat_flows(5) == 2.7403
    assert b._heat_flows(10) == 3.6438

    with raises(IndexError):
        a._heat_flows(-50)

    with raises(IndexError):
        a._heat_flows(100)


def test_copy():
    a, b = scans_from_csvs('tests/files/6HAW158.csv', 'tests/files/7HAW008-2.csv')
    assert a.copy() == a
    assert b.copy() == b
    assert a.copy() + 1 != a


def test_min():
    a, b = scans_from_csvs('tests/files/6HAW158.csv', 'tests/files/7HAW008-2.csv')
    assert a.min == (-10.02, -0.0044)
    assert b.min == (-0.037, 0.0044)


def test_max():
    a, b = scans_from_csvs('tests/files/6HAW158.csv', 'tests/files/7HAW008-2.csv')
    assert a.max == (48.741, 4.3940)
    assert b.max == (49.005, 5.9994)


def test_domain():
    a, b = scans_from_csvs('tests/files/6HAW158.csv', 'tests/files/7HAW008-2.csv')
    assert a.domain == (-10.05, 50.004)
    assert b.domain == (-0.068, 50.004)


def test_correlation():
    a, b = scans_from_csvs('tests/files/6HAW158.csv', 'tests/files/7HAW008-2.csv')
    aae(a.correlation(a), 1)
    aae(b.correlation(b), 1)

    with raises(NotImplementedError):
        a.correlation(b)


def test_smoothed():
    a, b = scans_from_csvs('tests/files/6HAW158.csv', 'tests/files/7HAW008-2.csv')
    assert all(a.smoothed().temps == a.temps)
    aae(a.smoothed().heat_flows, a.heat_flows, 0)
    assert all(b.smoothed().temps == b.temps)
    aae(b.smoothed().heat_flows, b.heat_flows, 0)


def test_baseline_subtracted():
    a, b = scans_from_csvs('tests/files/6HAW158.csv', 'tests/files/7HAW008-2.csv')
    assert all(a.baseline_subtracted().temps == a.temps)
    assert all(b.baseline_subtracted().temps == b.temps)

    assert a.baseline_subtracted() == a + 0.0044
    assert b.baseline_subtracted() == b - 0.0044


def test_set_zero():
    a, b = scans_from_csvs('tests/files/6HAW158.csv', 'tests/files/7HAW008-2.csv')
    assert all(a.set_zero(0).temps == a.temps)
    assert all(b.set_zero(0, 10).temps == b.temps)

    assert a.set_zero(0) == a - 2.5875
    aae(b.set_zero(0, 10).heat_flows, b.heat_flows - 1.55118507)


def test_sliced():
    a, b = scans_from_csvs('tests/files/6HAW158.csv', 'tests/files/7HAW008-2.csv')
    assert a.sliced() == a
    assert all(a.sliced(5).heat_flows == a.heat_flows[111:])

    assert b.sliced() == b
    assert all(b.sliced(5, 30).heat_flows == b.heat_flows[80:155])

    assert b.sliced() == b
    assert all(b.sliced(None, 30).heat_flows == b.heat_flows[:155])


def test_norm():
    a, b = scans_from_csvs('tests/files/6HAW158.csv', 'tests/files/7HAW008-2.csv')
    aae(a.norm, 46.644171825534640)
    aae(b.norm, 60.521320612739444)


def test_normed():
    a, b = scans_from_csvs('tests/files/6HAW158.csv', 'tests/files/7HAW008-2.csv')
    aae(a.normed().heat_flows, a.heat_flows*0.0051397304)
    aae(b.normed('max').heat_flows, b.heat_flows*0.16668333409090907)
    aae(b.normed(5).heat_flows, b.heat_flows*0.29969729545454543)


def test_peaks():
    a, b = scans_from_csvs('tests/files/6HAW158.csv', 'tests/files/7HAW008-2.csv')
    peak_idxs, properties = a.peaks()
    assert len(peak_idxs) == 23
    temps, properties = b.peaks(True)
    assert len(temps) == 16
