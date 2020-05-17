
from furl import furl


class URL:

    def __init__(self, url: str):
        self._url = url

    @property
    def url(self):
        return self._url

    @property
    def first_path_part(self):
        return self.path_parts[0]

    @property
    def path_parts(self):
        return self.furl.path.segments

    @property
    def furl(self):
        return furl(self.url)



