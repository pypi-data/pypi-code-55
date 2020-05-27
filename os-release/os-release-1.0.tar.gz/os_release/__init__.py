import errno
import os
from pathlib import Path
from typing import NamedTuple, Tuple, Dict

from os_release.parser import PARSER, parse_file, parse_str

KNOWN_PATHS = [
    Path('/etc/os-release'),
    Path('/usr/lib/os-release'),
]


class OsRelease(NamedTuple):
    """Represents the fields of a systemd ``os-release`` file.

    :py:class:`OsRelease` is a :py:class:`typing.NamedTuple`.
    """

    name: str
    """Equivalent to the |os-release#NAME|_ field in ``os-release``.
    
        .. |os-release#NAME| replace:: ``NAME``
        .. _os-release#NAME: https://www.freedesktop.org/software/systemd/man/os-release.html#NAME=
    
        As per `os-release(5)`_, this property will default to ``Linux`` if ``NAME`` is not present in ``os-release``.
    """

    version: str
    """Equivalent to the |os-release#VERSION|_ field in ``os-release``.
    
        .. |os-release#VERSION| replace:: ``VERSION``
        .. _os-release#VERSION: https://www.freedesktop.org/software/systemd/man/os-release.html#VERSION=
    
        This property is optional and will default to :py:const:`None` if ``VERSION`` is not present in ``os-release``.
    """

    id: str
    """Equivalent to the |os-release#ID|_ field in ``os-release``.
    
        .. |os-release#ID| replace:: ``ID``
        .. _os-release#ID: https://www.freedesktop.org/software/systemd/man/os-release.html#ID=
    
        As per `os-release(5)`_, this property will default to ``linux`` if ``ID`` is not present in ``os-release``.
    """

    id_like: Tuple[str]
    """Equivalent to the |os-release#ID_LIKE|_ field in ``os-release``.
    
        .. |os-release#ID_LIKE| replace:: ``ID_LIKE``
        .. _os-release#ID_LIKE: https://www.freedesktop.org/software/systemd/man/os-release.html#ID_LIKE=
    
        The value of ``ID_LIKE`` is automatically split on whitespace into a tuple.
        
        This property is optional and will default to an empty tuple if ``ID_LIKE`` is not present in ``os-release``.
    """

    version_codename: str
    """Equivalent to the |os-release#VERSION_CODENAME|_ field in ``os-release``.
    
        .. |os-release#VERSION_CODENAME| replace:: ``VERSION_CODENAME``
        .. _os-release#VERSION_CODENAME: https://www.freedesktop.org/software/systemd/man/os-release.html#VERSION_CODENAME=
        
        This property is optional and will default to :py:const:`None` if ``VERSION_CODENAME`` is not present in ``os-release``.
    """

    version_id: str
    """Equivalent to the |os-release#VERSION_ID|_ field in ``os-release``.
    
        .. |os-release#VERSION_ID| replace:: ``VERSION_ID``
        .. _os-release#VERSION_ID: https://www.freedesktop.org/software/systemd/man/os-release.html#VERSION_ID=
        
        This property is optional and will default to :py:const:`None` if ``VERSION_ID`` is not present in ``os-release``.
    """

    pretty_name: str
    """Equivalent to the |os-release#PRETTY_NAME|_ field in ``os-release``.
    
        .. |os-release#PRETTY_NAME| replace:: ``PRETTY_NAME``
        .. _os-release#PRETTY_NAME: https://www.freedesktop.org/software/systemd/man/os-release.html#PRETTY_NAME=
            
        As per `os-release(5)`_, this property will default to ``Linux`` if ``PRETTY_NAME`` is not present in ``os-release``.
    """

    ansi_color: str
    """Equivalent to the |os-release#ANSI_COLOR|_ field in ``os-release``.
    
        .. |os-release#ANSI_COLOR| replace:: ``ANSI_COLOR``
        .. _os-release#ANSI_COLOR: https://www.freedesktop.org/software/systemd/man/os-release.html#ANSI_COLOR=
        
        This property is optional and will default to :py:const:`None` if ``ANSI_COLOR`` is not present in ``os-release``.
    """

    cpe_name: str
    """Equivalent to the |os-release#CPE_NAME|_ field in ``os-release``.
    
        .. |os-release#CPE_NAME| replace:: ``CPE_NAME``
        .. _os-release#CPE_NAME: https://www.freedesktop.org/software/systemd/man/os-release.html#CPE_NAME=
        
        This property is optional and will default to :py:const:`None` if ``CPE_NAME`` is not present in ``os-release``.
     """

    build_id: str
    """Equivalent to the |os-release#BUILD_ID|_ field in ``os-release``.
    
        .. |os-release#BUILD_ID| replace:: ``BUILD_ID``
        .. _os-release#BUILD_ID: https://www.freedesktop.org/software/systemd/man/os-release.html#BUILD_ID=
        
        This property is optional and will default to :py:const:`None` if ``BUILD_ID`` is not present in ``os-release``.
    """

    variant: str
    """Equivalent to the |os-release#VARIANT|_ field in ``os-release``.
    
        .. |os-release#VARIANT| replace:: ``VARIANT``
        .. _os-release#VARIANT: https://www.freedesktop.org/software/systemd/man/os-release.html#VARIANT=
        
        This property is optional and will default to :py:const:`None` if ``VARIANT`` is not present in ``os-release``.
    """

    variant_id: str
    """Equivalent to the |os-release#VARIANT_ID|_ field in ``os-release``.
    
        .. |os-release#VARIANT_ID| replace:: ``VARIANT_ID``
        .. _os-release#VARIANT_ID: https://www.freedesktop.org/software/systemd/man/os-release.html#VARIANT_ID=
        
        This property is optional and will default to :py:const:`None` if ``VARIANT_ID`` is not present in ``os-release``.
    """

    logo: str
    """Equivalent to the |os-release#LOGO|_ field in ``os-release``.
    
        .. |os-release#LOGO| replace:: ``LOGO``
        .. _os-release#LOGO: https://www.freedesktop.org/software/systemd/man/os-release.html#LOGO=
        
        This property is optional and will default to :py:const:`None` if ``LOGO`` is not present in ``os-release``.
    """

    urls: 'OsRelease.Urls'
    """See :py:class:`OsRelease.Urls`.
    
        This property will always be an instance of :py:class:`OsRelease.Urls`, even if no ``*_URL`` fields are present
        in ``os-release``.
    """

    vendor_extra: Dict[str, str]
    """A dict of vendor-specific fields (fields that are unknown to `os-release`)."""

    class Urls(NamedTuple):
        """Represents the various ``*_URL`` fields in ``os-release``.
        """
        home: str
        """Equivalent to the ``HOME_URL`` field in ``os-release``."""

        documentation: str
        """Equivalent to the ``DOCUMENTATION_URL`` field in ``os-release``."""

        support: str
        """Equivalent to the ``SUPPORT_URL`` field in ``os-release``."""

        bug_report: str
        """Equivalent to the ``BUG_REPORT_URL`` field in ``os-release``."""

        privacy_policy: str
        """Equivalent to the ``PRIVACY_POLICY_URL`` field in ``os-release``."""

        @staticmethod
        def from_dict(d: dict) -> 'OsRelease.Urls':
            return OsRelease.Urls(
                **{f: d.pop(f'{f.upper()}_URL', None) for f in OsRelease.Urls._fields},
            )

    @staticmethod
    def from_dict(d: dict) -> 'OsRelease':
        return OsRelease(
            **{f: d.pop(f.upper(), None) for f in (set(OsRelease._fields) - {'name', 'id', 'pretty_name', 'id_like', 'urls', 'vendor_extra'})},

            # defaults, according to os-release(5)
            name=d.pop('NAME', 'Linux'),
            id=d.pop('ID', 'linux'),
            pretty_name=d.pop('PRETTY_NAME', 'Linux'),

            # split ID_LIKE into a tuple
            id_like=tuple(d.pop('ID_LIKE', '').split()),

            # organise URLs into a sub-tuple
            urls=OsRelease.Urls.from_dict(d),

            # everything else...
            vendor_extra=d
        )

    @staticmethod
    def read(path: Path) -> 'OsRelease':
        """"""
        data = parse_file(path)
        return OsRelease.from_dict(data)

    @staticmethod
    def from_str(s: str) -> 'OsRelease':
        """"""
        data = parse_str(s)
        return OsRelease.from_dict(data)

    def is_like(self, query: str) -> bool:
        """Returns :py:const:`True` if the operating system represented by this :py:class:`OsRelease` has an
            :py:attr:`id` or :py:attr:`id_like` that matches the passed :paramref:`query`.

            :param query: the id to test
        """

        if self.id == id:
            return True

        return id in self.id_like


def current_release() -> OsRelease:
    """Return an :py:class:`OsRelease` tuple representing the contents of the ``os-release`` file for the current
        operating system.

        Tries to read the following files, in order (as per `os-release(5)`_):

        * ``/etc/os-release``
        * ``/usr/lib/os-release``

        :raises FileNotFoundError: if no ``os-release`` file can be found.
        :raises OsReleaseParseException: if the ``os-release`` file cannot be parsed.
    """
    for path in KNOWN_PATHS:
        try:
            return OsRelease.read(path)

        except FileNotFoundError:
            pass

    raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), [str(p) for p in KNOWN_PATHS])