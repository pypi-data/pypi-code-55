
class CheckerError(RuntimeError):
    pass


class CheckerVersionError(RuntimeError):
    def __init__(self, target, version):
        super().__init__("Version problem with {}. Expected {}".format(target, version))

