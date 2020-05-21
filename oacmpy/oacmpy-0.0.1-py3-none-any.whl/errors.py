class OacmError(Exception):

    pass


class _Unknown(OacmError):
    def __init__(self, name):
        self.name = name

    @property
    def type(self):
        return self.__class__.__name__[7:-5].lower()

    def __str__(self):
        return "Unknown {} '{}'".format(self.type, self.name)


class UnknownFrameError(_Unknown):
    """Unknown frame (ITRF, EME2000, etc.)
    """

    pass


class FrameError(_Unknown):
    """   """

    pass


class DateError(OacmError):
    pass


class TimeSystemError(OacmError):
    pass


class UnknownScaleError(_Unknown):
    pass


class EopError(OacmError):

    pass
