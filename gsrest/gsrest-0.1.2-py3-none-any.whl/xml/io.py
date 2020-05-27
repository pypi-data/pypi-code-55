# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 Instituto Tecnológico de Canarias, S.A.
#
# This file is part of GsRest
# (see https://github.com/esuarezsantana/gsrest).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
"""XML IO functions and classes.
"""

import dataclasses
import functools
import typing
from xml.etree import ElementTree as Et  # nosec

from ..helper import function as helperfun  # type: ignore
from . import converter as c


@dataclasses.dataclass
class XmlPathElement:
    """Xml Path Element.

    A path element consists of:
      - tag: the name of the xml tag
      - attr: dict of attrs for the xml node (<tag attr1=v1 attr2=v2>)
      - many: a boolean that tells that many nodes are expected to be found for
              this path element. Defaults to False.

    """

    tag: str
    attr: typing.Dict[str, str] = dataclasses.field(default_factory=dict)
    many: bool = False

    def tagformat(self, *args, **kwargs):
        """Format tag string using python format.

        Useful for generic tags.

        """
        self.tag = self.tag.format(*args, **kwargs)

    @staticmethod
    def from_single(whatever):
        "Factory for single object."
        if isinstance(whatever, XmlPathElement):
            return whatever
        if isinstance(whatever, str):
            if "/" in whatever:
                raise Exception("Must be converted to list")
            return XmlPathElement(tag=whatever)
        if isinstance(whatever, dict):
            return XmlPathElement(**whatever)
        raise Exception("Cannot convert to XmlPathElement.")

    @staticmethod
    def from_list(whatever):
        "Factory for list of objects."
        if isinstance(whatever, XmlPathElement):
            return [whatever]
        if isinstance(whatever, str):
            return [
                XmlPathElement.from_single(elem)
                for elem in whatever.split("/")
            ]
        if isinstance(whatever, list):
            return [XmlPathElement.from_single(item) for item in whatever]
        raise Exception("Cannot convert to List of XmlPathElements.")

    @staticmethod
    def separate_list_on_many(xpe_list):
        """Separate a list of XPEs on head and tail based on many.

        Args:
            xpe_list: list of XmlPathElements

        Returns:
            - A head list where many is False for every element.
            - A tail list where many is True for the first element.

        """
        return helperfun.separate_on_pred(xpe_list, lambda xpe: xpe.many)


@dataclasses.dataclass
class XmlAccessor:
    """Generic XmlAccessor.

    This class provides a reader and a writer to read data from and write data
    to an XML.

    Args:
        path: An XPE list about where the data is located in the XML.
        converter: How to convert data to XML string and viceversa.
                   Defaults to StringConverter.
    """

    path: dataclasses.InitVar[typing.Any]
    converter: typing.Type[c.Converter] = dataclasses.field(
        default=c.StringConverter
    )
    xpe_head: typing.List[XmlPathElement] = dataclasses.field(init=False)
    xpe_tail: typing.List[XmlPathElement] = dataclasses.field(init=False)

    def __post_init__(self, path):
        self.xpe_head, self.xpe_tail = XmlPathElement.separate_list_on_many(
            XmlPathElement.from_list(path)
        )

    def read(self, xmltree):
        """Reader function to parse elements from an XML.

        Args:
            xmltree(ElementTree): Xml node to read from.

        Returns:
            Data read from the xml node.

        """

        def _build_path(xpe_list):
            return "./{}".format("/".join(e.tag for e in xpe_list))

        base = (
            xmltree.find(_build_path(self.xpe_head))
            if self.xpe_head
            else xmltree
        )
        if base is None:
            return None
        if self.xpe_tail:
            # we expect a list
            leaves = base.findall(_build_path(self.xpe_tail))
            return [self.converter.from_node(n) for n in leaves]
        # we expect just one value
        return self.converter.from_node(base)

    def read_from_bytes(self, xml_stream):
        """Read data from XML stream.

        Args:
            xml_stream(bytes): the xml stream.

        Returns:
            Data read from the xml stream.
        """
        return self.read(Et.XML(xml_stream))

    def write(self, xmltree, whatever):
        """Writer function to write elements to an XML.

        Args:
            xmltree(ElementTree): Xml node to write to.
            whatever(Any): Data to be written.

        """

        if whatever is None:
            return
        base = (
            self.write_descend(xmltree, self.xpe_head)
            if self.xpe_head
            else xmltree
        )
        values = whatever if self.xpe_tail else [whatever]
        for value in values:
            leaf = self.write_descend(base, self.xpe_tail)
            self.converter.to_node(value, leaf)

    @staticmethod
    def write_descend(node, xpe_list):
        """Write sequence of xml path elements to node.

        Args:
            node: XML node to write to.
            xpe_list: XmlPathElement list to be written

        Returns:
            Inner node.

        """

        return functools.reduce(
            lambda n, xpe: Et.SubElement(n, xpe.tag, xpe.attr), xpe_list, node
        )


@dataclasses.dataclass
class XmlBuilder:
    """Xml Builder.

    Simplifies the creation of XML Trees.

    Args:
        root_name: Tag name for root node.

    """

    root_name: dataclasses.InitVar[str]
    _xmltree: Et.Element = dataclasses.field(init=False)

    def __post_init__(self, root_name):
        self._xmltree = Et.Element(root_name)

    def __str__(self):
        return Et.tostring(self._xmltree, encoding="unicode")

    # TODO: https://github.com/PyCQA/pylint/issues/3599
    def __bytes__(self):  # pylint: disable=invalid-bytes-returned
        return str(self).encode("utf-8")

    @property
    def tree(self):
        "The XML tree itself."
        return self._xmltree

    def write(self, obj, path, converter=c.StringConverter):
        """Write data to Xml tree.

        Args:
            obj(Any): data to write
            path(Any): anything that may be converted to XmlPathElement
            converter(Converter): data converter to xml

        """

        XmlAccessor(path, converter=converter).write(self._xmltree, obj)
