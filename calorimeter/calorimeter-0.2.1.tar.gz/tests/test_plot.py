import sys

import matplotlib.pyplot as plt
sys.path.insert(0, '..')

from calorimeter.plot import cycle_values, plotter, setup_axis
from calorimeter.scan import scans_from_csvs


def setup():
    pass


def teardown():
    pass


def test_setup_axis():
    fig, ax = plt.subplots()

    setup_axis(ax)
    setup_axis(ax, None, xticks=range(100), xlim=(0, 100))


def test_cycle_values():
    assert next(cycle_values(None)) is None
    assert next(cycle_values(1)) == 1

    it = cycle_values([0, 1, 2])
    assert next(it) == 0
    assert next(it) == 1
    assert next(it) == 2
    assert next(it) == 0


def test_plotter(tmp_path):
    scans = scans_from_csvs('tests/files/6HAW158.csv', 'tests/files/7HAW008-2.csv')

    fig, ax = plt.subplots()
    plotter(
        scans,
        title='Hello World', style=None,
        baseline_subtracted=True, set_zero=False, normalized=False, smoothed=False, peaks=None,
        plot=(fig, ax), xlim=(0, 50), xticks_minor=True, yticks_minor=2,
        legend=True, colors=None, markers=None, linestyles=None,
        savefig=f'{tmp_path}/my_scans_figure.svg',
    )
