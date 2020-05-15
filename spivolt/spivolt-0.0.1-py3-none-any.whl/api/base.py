import abc
import requests as rq
from typing import Optional
from ..parameters.dates import DateFilter


class APIInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def sites(self, site_id: Optional[str] = None) -> str:
        raise NotImplementedError("Define the 'sites' method of the API interface.")

    @abc.abstractmethod
    def sp(self, site_id: str, date_filter: DateFilter) -> str:
        raise NotImplementedError("Define the 'sp' method of the API interface.")


class DefaultAPI(APIInterface):
    def __init__(self, url: str, code: str):
        self.url = url
        self.code = code

    def sites(self, site_id: Optional[str] = None) -> str:
        if site_id:
            return rq.get(f"{self.url}/sites/{site_id}?{self._code_string()}").text
        else:
            return rq.get(f"{self.url}/sites?{self._code_string()}").text

    def sp(self, site_id: str, date_filter: DateFilter) -> str:
        params = self._code_string() + date_filter.to_api_param()
        return rq.get(f"{self.url}/sp/{site_id}?{params}").text

    def _code_string(self):
        return f"code={self.code}"
