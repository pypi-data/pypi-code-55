import copy

from komapy.utils import compute_middletime, time_to_offset, to_pydatetime

from .constants import get_phase_dates


def filter_date_in_range(phase_dates, starttime, endtime):
    """
    Exclude phases date outside range, and handle its date boundary.
    """
    phases = copy.deepcopy(phase_dates)
    for item in phases:
        if not (item[0] >= starttime and item[0] < endtime):
            item[0] = None
        if not (item[1] > starttime and item[1] <= endtime):
            item[1] = None

    new_phases = [
        item for item in phases if not (item[0] is None and item[1] is None)
    ]
    new_phases[0][0] = starttime
    new_phases[-1][1] = endtime
    return new_phases


def calculate_middle_date(phase_dates):
    """
    Calculate middle time from phase dates entry.
    """
    phases = []
    for item in phase_dates:
        phases.append([compute_middletime(item[0], item[1]), item[2]])
    return phases


def plot_activity_phases(axis, **options):
    """
    Plot activity phases labels on current axis.

    Note that this function requires 'starttime' and 'endtime' to be set on the
    series options to determine which labels to render in the plot figure.

    Phase text can be overrided by providing labels on series options.
    """

    def get_value_or_none(data, index):
        try:
            return data[index]
        except IndexError:
            return None

    default_offset_value = 1.1
    labels = options.pop('labels', [])
    starttime = to_pydatetime(options.pop('starttime')).replace(tzinfo=None)
    endtime = to_pydatetime(options.pop('endtime')).replace(tzinfo=None)

    PHASE_DATES = get_phase_dates()
    phase_dates = filter_date_in_range(PHASE_DATES, starttime, endtime)
    middle_time = calculate_middle_date(phase_dates)

    offsets = [
        [
            time_to_offset(starttime, endtime, item[0]),
            get_value_or_none(labels, index) or item[1]
        ] for index, item in enumerate(middle_time)
    ]
    offset = options.pop('offset', default_offset_value)
    for item in offsets:
        axis.text(item[0],
                  offset,
                  item[1],
                  horizontalalignment='center',
                  verticalalignment='center',
                  transform=axis.transAxes, **options)
