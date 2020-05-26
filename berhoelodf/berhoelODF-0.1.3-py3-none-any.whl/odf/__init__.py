#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Give access to ods files.
"""

# Standard libraries.
from typing import Union
from pathlib import Path
from zipfile import ZipFile

# Third party libraries.
import lxml
from lxml import etree

__date__ = "2020/05/26 22:46:57 hoel"
__author__ = "Berthold Höllmann"
__copyright__ = "Copyright © 2020 by Berthold Höllmann"
__credits__ = ["Berthold Höllmann"]
__maintainer__ = "Berthold Höllmann"
__email__ = "berhoel@gmail.com"

try:
    from ._version import __version__
except ImportError:
    __version__ = "0.0.0+unknown0"


class OdfXml:
    def __init__(self, elem: etree._Element):
        """
Parameters:
    element (etree._Element): XML Element
        """
        self.root = elem
        self.nsmap = (
            self.root.nsmap if hasattr(elem, "nsmap") else self.root.getroot().nsmap
        )

    def find(self, tag: str) -> etree._Element:
        "Find `tag` in this element."
        return self.root.find(tag, namespaces=self.nsmap)

    def findall(self, tag: str) -> list:
        "Find all of `tag`."
        return self.root.findall(tag, namespaces=self.nsmap)

    def _attrib_map(self, attrib: str) -> str:
        "Helper for `get`: provide namespace."
        ns, tag = attrib.split(":")
        return f"{{{self.nsmap[ns]}}}{tag}"

    def get(self, attrib: str) -> str:
        "Get atribute of this element, honors namespace."
        return self.root.get(self._attrib_map(attrib))


class Odf(OdfXml):
    "Base class for OpenDocument Format files."

    def __init__(self, path: Union[str, Path]):
        """
        Open ODF file from `path`.
        """
        with ZipFile(path) as odf_zip:
            with odf_zip.open("content.xml") as content:
                doc = etree.parse(content)
        super().__init__(doc)


# Local Variables:
# mode: python
# compile-command: "poetry run tox"
# time-stamp-pattern: "30/__date__ = \"%:y/%02m/%02d %02H:%02M:%02S %u\""
# End:
