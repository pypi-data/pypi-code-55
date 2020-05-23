from Version.VersionException import VersionException


class Version:
    _MAX_LEN = 4

    def __init__(self, version):
        if isinstance(version, str):
            version = self._parse_string(version)
        if len(version) < 1 or len(version) > 4:
            raise VersionException()
        self._version = tuple(version)

    def get_version(self, length=None):
        if length is None:
            return self._version
        ver = (list(self._version) + [0] * Version._MAX_LEN)[:length]
        return tuple(ver)

    def __len__(self):
        return len(self._version)

    def __eq__(self, other):
        ver1 = self.get_version(length=Version._MAX_LEN)
        ver2 = other.get_version(length=Version._MAX_LEN)
        return ver1 == ver2

    def compare(self, other, length=None):
        if length is None:
            length = max(len(self), len(other))
        ver1 = self.get_version(length=length)
        ver2 = other.get_version(length=length)
        return ver1 == ver2

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        raise NotImplementedError()

    def __gt__(self, other):
        raise NotImplementedError()

    def __le__(self, other):
        raise NotImplementedError()

    def __ge__(self, other):
        raise NotImplementedError()

    @staticmethod
    def _parse_string(text):
        try:
            text = text.strip().split(" ")[0]
            result = text.strip().split(".")
            result = [int(a) for a in result]
        except Exception:
            raise VersionException()
        return result

    def __repr__(self):
        return ".".join([str(a) for a in self._version])

    def __str__(self):
        return self.__repr__()
