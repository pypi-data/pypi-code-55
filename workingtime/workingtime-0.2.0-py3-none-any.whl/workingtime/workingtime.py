import pandas as pd
import datetime as dt
from datetime import timedelta


def _dates_between_dates(start, end):
    return list(pd.date_range(start + timedelta(1),
                              end - timedelta(1),
                              freq='d'))


def _is_overlapping(x1, x2, y1, y2):
    return not (x1 > y2 or y1 > x2)


def _is_overlapping_bis(x1, x2, y1, y2):
    return not (max(x1, y1) <= min(x2, y2))


def overlap(x1, x2, y1=None, y2=None):
    if y1 is None and y2 is None:
        return x2 - x1

    if y1 is None:
        y1 = Time.min

    if x1 == x2 or y1 == y2:
        return timedelta(0)

    if y2 is None:
        y2 = Time.max

    if not _is_overlapping(x1, x2, y1, y2):
        raise ValueError("Intervals does not overlaps")

    return min(x2, y2) - max(x1, y1)


class Time(dt.time):
    def seconds(self):
        return self.hour * 3600 + self.minute * 60 + self.second

    @staticmethod
    def from_seconds(seconds):
        secs = seconds % 60
        mins = int(seconds / 60) % 60
        hours = int(seconds / 3600) % 24
        return Time(hours, mins, secs)

    @staticmethod
    def from_time(dtime):
        return Time(dtime.hour, dtime.minute, dtime.second)

    @staticmethod
    def from_dt(dtime):
        return Time.from_time(dtime.time())

    def __sub__(self, other):
        return timedelta(seconds=self.seconds() - other.seconds())

    def __rsub__(self, other):
        return Time.from_time(other) - self


class WorkingTime:
    def __init__(self, weekends=None, holidays=None):
        # TODO check the variables
        self.weekends = weekends
        self.holidays = holidays

    def working_time(self, start, end, work_hours=None):
        if work_hours is None:
            work_hours = (Time(8), Time(16))

        work_hours = (Time.from_time(work_hours[0]),
                      Time.from_time(work_hours[1]))

        # If start > end, workingtime will be negative
        if start > end:
            return -1 * self.working_time(end, start, work_hours)

        # If the day changes between your workhours, its easier to calculate
        # the time your note working and substract
        if work_hours[0] > work_hours[1]:
            return ((end - start) -
                    self.working_time(start, end,
                                      tuple(reversed(work_hours))))

        # If the start time and the end time are the same we
        # return the workhours * days between. But it can't be done
        # like this because start date or end date could be weekend or holiday

        if start.date() == end.date():
            # TODO implementar esta  cosica
            return overlap(Time.from_dt(start), Time.from_dt(end), *work_hours)

        middle_time = (len(_dates_between_dates(start, end)) *
                       (work_hours[1] - work_hours[0]))

        return (overlap(*work_hours, Time.from_dt(start)) +
                middle_time +
                overlap(*work_hours, None, Time.from_dt(end)))
