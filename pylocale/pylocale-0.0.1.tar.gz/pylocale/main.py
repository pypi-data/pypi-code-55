# -*- coding: utf-8 -*-

"""
pylocale library.
A Python 3 library that allows adding static files
with translations to the application,
and then apply them to dynamically change text in the application.
:copyright: (c) 2020 Mavedev
:licence: MIT, see LICENCE for more details.
"""

import pylocale.errors as errors
import pylocale.aliases as aliases
from pylocale.parser import parse


class PyLocale:
    """Main class providing translations."""

    def __init__(
        self,
        *,
        at: aliases.Path,
        root: aliases.Locale,
        silent=False
    ) -> None:
        self._locales_path = at
        self._silent = silent
        self._vocabulary: aliases.Vocabulary = {}
        self._load_locales(at, root, first_time=True)
        self._root = self._vocabulary.copy()

    def _load_locales(
        self, locales_path: aliases.Path,
        locale: aliases.Locale,
        first_time=False
    ) -> None:
        try:
            self._vocabulary = parse(locales_path, locale)
            if not first_time:
                self._cover_root()
        except FileNotFoundError:
            if not self._silent:
                raise errors.NoSuchLocaleError(
                    'The locale "{}" was not found at the specified path'
                    .format(locale)
                )
        except errors.ParserInvalidLineError as parse_error:
            if not self._silent:
                # Reraise the error if not in silent mode.
                raise parse_error
            else:
                self._vocabulary = {} if first_time else self._root.copy()

    def switch(self, locale: str) -> None:
        self._load_locales(self._locales_path, locale)

    def __getitem__(self, key: str) -> str:
        if not self._vocabulary.get(key):
            if not self._silent:
                raise errors.NoSuchKeyError(
                    'There is no key "{}"'.format(key)
                )
            else:
                return ''
        return self._vocabulary[key]

    def _cover_root(self) -> None:
        for key in self._root.keys():
            if key not in self._vocabulary.keys():
                self._vocabulary[key] = self._root[key]
