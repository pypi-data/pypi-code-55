#! python3  # noqa: E265

"""
    Metadata bout the package to easily retrieve informations about it.
    See: https://packaging.python.org/guides/single-sourcing-package-version/
"""

from datetime import date

__all__ = [
    "__title__",
    "__summary__",
    "__uri__",
    "__version__",
    "__author__",
    "__email__",
    "__license__",
    "__copyright__",
]


__author__ = "Isogeo"
__copyright__ = "2019 - {0}, {1}".format(date.today().year, __author__)
__email__ = "contact@isogeo.com"
__license__ = "GNU Lesser General Public License v3.0"
__summary__ = (
    "Command-line to read metadata produced by FME scripts of Isogeo Scan, "
    "convert it into Isogeo model, apply rules and export it to a database or Isogeo."
)
__title__ = "Isogeo Scan Metadata Processor"
__uri__ = "https://github.com/isogeo/scan-metadata-processor/"

__version__ = "1.0.7"
