from xml.etree.ElementTree import ParseError


class CcsdsError(ParseError, KeyError):
    def __init__(self, message=None):
        self.message = message

    def __str__(self):
        if self.message:
            return "CcsdsError: {0}".format(self.message)
        return "CcsdsError"


class CcsdsObjectNotFoundError(CcsdsError, KeyError):
    pass


class CcsdsParameterNotFoundError(CcsdsError, KeyError):
    pass
