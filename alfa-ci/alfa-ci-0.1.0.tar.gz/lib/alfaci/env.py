"""generic environment module"""


class Env:
    """environment base class"""
    def __init__(self, repo):
        """ctor"""
        self._repo = repo

    @property
    def repo(self):
        """prop"""
        return self._repo

    @property
    def installed(self):
        """prop"""
        return False

    def install(self):
        """abstract install"""
        raise NotImplementedError('<override me>')

    def __repr__(self):
        return '<override me>'
