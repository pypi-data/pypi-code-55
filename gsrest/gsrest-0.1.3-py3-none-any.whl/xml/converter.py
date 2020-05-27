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
"""Converter classes for Geoserver XML data.
"""

import abc
import xml.etree.ElementTree as Et  # nosec


class Converter(abc.ABC):
    "Abstract Base Class Converter."

    def from_bytes(self, xml_stream):
        """Convert string from XML stream to data.

        Args:
            xml_stream(bytes) : the XML stream

        Returns:
            Any data.
        """
        return self.from_node(Et.XML(xml_stream))

    @staticmethod
    @abc.abstractmethod
    def from_node(node):
        """Convert string from xml node to data.

        Args:
            node: XML leaf node.

        Returns:
            Any data.

        """

    @staticmethod
    @abc.abstractmethod
    def to_node(obj, node):
        """Convert data to string and write to subelement node.

        Args.
            obj: the data
            node: XML node to write data to

        """


class StringConverter(Converter):
    "String Converter."

    @staticmethod
    def from_node(node):
        """Returns string from xml node.

        Args:
            node: XML leaf node.

        Returns:
            The string.

        """

        return node.text

    @staticmethod
    def to_node(obj, node):
        """Convert data to string using 'str' and write to subelement node.

        Args.
            obj: the data
            node: XML node to write data to

        """
        node.text = str(obj)


class BoolConverter(Converter):
    "Bool Converter."

    @staticmethod
    def from_node(node):
        """Returns bool from xml node.

        Args:
            node: XML leaf node.

        Returns:
            The string.

        Raises:
            Exception when not a valid bool is found in the XML.

        """
        boolstr = node.text
        if boolstr not in ("true", "false"):
            raise ValueError("Invalid bool value in XML.")
        return boolstr == "true"

    @staticmethod
    def to_node(obj, node):
        """Convert data to bool (if not yet) and write to subelement node.

        Args.
            obj: the data
            node: XML node to write data to

        """
        node.text = str(bool(obj)).lower()


class IntegerConverter(Converter):
    "Integer Converter."

    @staticmethod
    def from_node(node):
        """Returns integer from xml node.

        Args:
            node: XML leaf node.

        Returns:
            The string.

        Raises:
            ValueError when not a valid integer is found in the XML.

        """
        return int(node.text)  # would raise ValueError

    @staticmethod
    def to_node(obj, node):
        """Write number to subelement node.

        Args.
            obj(int): the integer
            node: XML node to write data to

        """
        node.text = str(obj)


class DoubleConverter(Converter):
    "Double Converter."

    @staticmethod
    def from_node(node):
        """Returns double from xml node.

        Args:
            node: XML leaf node.

        Returns:
            The string.

        Raises:
            ValueError when not a valid double is found in the XML.

        """
        return float(node.text)  # would raise ValueError

    @staticmethod
    def to_node(obj, node):
        """Write number to subelement node.

        Args.
            obj(float): the double
            node: XML node to write data to

        """
        node.text = str(obj)


class ColonLastTokenConverter(Converter):
    "Colon Sanitize Converter."

    @staticmethod
    def from_node(node):
        """Returns last token from xml node text after colon splitting.

        Args:
            node: XML leaf node.

        Returns:
            The last token string.

        Raises:
            ValueError when not a valid double is found in the XML.

        """
        return node.text.split(":")[-1]

    @staticmethod
    def to_node(obj, node):
        """Write last token of colon separated text to subelement node.

        Args.
            obj(str): colon separated string
            node: XML node to write data to

        """
        node.text = str(obj).split(":")[-1]
