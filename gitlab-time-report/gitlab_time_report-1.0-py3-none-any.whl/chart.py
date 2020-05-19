def time_in_hours(spent_time):
    """Converts a given string, that contains time-data in this format '%h %m %s', into a floating number.

        :param spent_time: GitLab time in hours, minutes and seconds, as a string.

        :return: Amount of hours as float.
    """
    times = spent_time.split()
    hours = 0.0
    for time in times:
        time_unit = time[-1]
        time_amount = int(time[:-1])
        if time_unit == "h":
            hours += time_amount
        elif time_unit == "m":
            hours += time_amount / 60
        elif time_unit == "s":
            hours += time_amount / 3600
    return hours


class Chart:
    title = "Undefined"
