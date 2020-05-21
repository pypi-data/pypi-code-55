from pathlib import Path

_LEAP_SECONDS = 37.0  # as of 2018
_DUT1 = 0.0  # delta-UT = UT1-UTC


class TaiUtc:
    """Provider for the delta time TAI-UTC
    File can be downloaded at: ftp://cddis.gsfc.nasa.gov/pub/products/iers
    """

    def __init__(self, path):

        self.path = Path(path)
        self.data = []

        with self.path.open() as fhandler:
            lines = fhandler.read().splitlines()

        for line in lines:
            if not line:
                continue

            line = line.split()
            mjd = int(float(line[4]) - 2400000.5)
            value = float(line[6])
            self.data.append((mjd, value))

    def __getitem__(self, date):
        for mjd, value in reversed(self.data):
            if mjd <= date:
                return value

    def get_last_next(self, date):
        """Provide the last and next leap-second events relative to a date
        Args:
            date (float): Date in MJD
        Return:
            tuple:
        """
        past, future = (None, None), (None, None)

        for mjd, value in reversed(self.data):
            if mjd <= date:
                past = (mjd, value)
                break
            future = (mjd, value)

        return past, future

    def set(self, leap):
        _LEAP_SECONDS = leap
