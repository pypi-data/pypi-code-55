import operator
from http import HTTPStatus
from typing import Dict

import requests
from cachetools import cachedmethod, TTLCache
from shuttlis.serialization import serialize

from ats_sdk.error import ClientError
from ats_sdk.translation import fetch_translatable_strings, translate

_LOCAL_CACHE_MAX_SIZE = 1024
_LOCAL_CACHE_TTL_IN_SECONDS = 60 * 60


class AlternateTextService:
    def __init__(self, url: str, cache_size: int = None, cache_expiry: int = None):
        self._url = url
        self._cache = TTLCache(
            maxsize=cache_size or _LOCAL_CACHE_MAX_SIZE,
            ttl=cache_expiry or _LOCAL_CACHE_TTL_IN_SECONDS,
        )

    def translate_and_serialize(self, resource: Dict, locale: str):
        translatable_strings = set(fetch_translatable_strings(resource=resource))

        if not translatable_strings:
            return serialize(resource)

        translated_strings = self.get_static_translation(
            locale=locale, keys=",".join(translatable_strings)
        )

        return serialize(
            translate(resource=resource, translated_strings=translated_strings)
        )

    @cachedmethod(operator.attrgetter("_cache"))
    def get_static_translation(self, locale: str, keys: str):
        response = requests.get(
            f"{self._url}/api/v1/translate/static",
            params={"locale": locale, "keys": keys},
        )
        if response.status_code != HTTPStatus.OK:
            raise ClientError(response.text)

        return response.json()["data"]


_alternate_text_service = None


def get_alternate_text_service(
    url: str, cache_size: int = None, cache_expiry: int = None
):
    global _alternate_text_service

    if not _alternate_text_service:
        _alternate_text_service = AlternateTextService(
            url=url, cache_size=cache_size, cache_expiry=cache_expiry
        )

    return _alternate_text_service
