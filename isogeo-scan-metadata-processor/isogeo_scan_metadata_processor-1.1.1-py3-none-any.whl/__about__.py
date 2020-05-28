#! python3  # noqa: E265

"""
    Metadata bout the package to easily retrieve informations about it.
    See: https://packaging.python.org/guides/single-sourcing-package-version/
"""

from datetime import date

__all__ = [
    "__author__",
    "__copyright__",
    "__email__",
    "__executable_name__",
    "__license__",
    "__package_name__",
    "__summary__",
    "__title__",
    "__uri__",
    "__version__",
]


__author__ = "Isogeo"
__copyright__ = "2019 - {0}, {1}".format(date.today().year, __author__)
__email__ = "contact@isogeo.com"
__executable_name__ = "Isogeo_ScanOffline.exe"
__license__ = "GNU Lesser General Public License v3.0"
__package_name__ = "scan_metadata_processor"
__pypi_name__ = "isogeo-scan-metadata-processor"
__summary__ = (
    "Command-line to read metadata produced by FME scripts of Isogeo Scan, "
    "convert it into Isogeo model, apply rules and export it to a database or Isogeo."
)
__title__ = "Isogeo Metadata Processor"
__title_clean__ = "".join(e for e in __title__ if e.isalnum())
__uri__ = "https://github.com/isogeo/scan-metadata-processor/"

__version__ = "1.1.1"
__version_info__ = tuple(
    [
        int(num) if num.isdigit() else num
        for num in __version__.replace("-", ".", 1).split(".")
    ]
)
