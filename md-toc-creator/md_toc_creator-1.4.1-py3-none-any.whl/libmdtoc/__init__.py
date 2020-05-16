#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
    mdtoc: Generates a table of contents for a markdown document in markdown.
    """
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


# import the sys module for standard IO and the re module for parsing regular expressions.
import sys
import re
# We'll also need the line separator which varies depending on your operating system.
from os import linesep

# Import some bits and pieces from the typing module to be used with type hints.
from typing import List, IO, Union, Type
from types import FunctionType

__author__ = "Michael Connor Buchan"
__copyright__ = "Copyright (C) 2019-2020" + __author__
__credits__ = __author__
__license__ = "GPL-3.0-OR-LATER"
__version__ = "1.4.1"
__maintainer__ = __author__
__email__ = "mikeybuchan@hotmail.co.uk"
__status__ = "Production"

Strings: 'defines a list of words' = List[str]
File: 'defines Either a path of a file object' = Union[str, IO['TextIO']]


def get_file_contents(file: File) -> Strings:
    """ Takes either a path or a file object, returning the file's contents. """
    # Check if the passed 'file' argument is a string.
    if isinstance(file, str):
        # It is, so open a file with this path.
        file: IO['TextIO'] = open(file, "r")
    # We've got a file object regardless now, so return it's contents as a list of lines.
    # We're also trapping and gracefully exiting from keyboardInterrupts
    # here, in case the file is stdin.
    try:
        text: str = file.read()
    except KeyboardInterrupt:
        sys.exit(1)
    lines: Strings = text.split("\n")
    return lines


class MDTOCItem:
    """ Represents an item of a table of contents. """

    def __init__(
            self, level: int, title: Strings,
            min_indent: int = 1, max_indent: int = 6,
            whitespace: str = "\t", separator: str = ' '):
        """ Sets up the object """
        # Set some important properties.
        self.title: Strings = title
        self.level: int = level
        self.min_indent: int = max(0, min_indent)
        self.max_indent: int = max(0, max_indent)
        self.whitespace: str = whitespace
        self.separator: str = separator
        # This computed physical level is the actual indentation level of the item,
        # with min and max indents taken into account.
        self.physical_level: int = min(
            self.level - self.min_indent, self.max_indent)

    def get_list_item_nonlinked(self) -> str:
        """ Returns a non-linked list item representing this TOC item. """
        # First, get a textual representation of the title.
        title_text: str = ' '.join(self.title)
# Next, create white space based on the computed physical level.
        whitespace: str = self.whitespace * self.physical_level
# Finally, return the full list item.
        return f"{whitespace}*{self.separator}{title_text}"

    def get_list_item_linked(self) -> str:
        """ Returns a linked list item representing this TOC item. """
        # First, get a textual representation of the title.
        title_text: str = ' '.join(self.title)
# Also, get a textual representation of a link reference to this heading.
        title_reference: str = "#" + '-'.join(self.title).lower()
# Next, create white space based on the computed physical level.
        whitespace: str = self.whitespace * self.physical_level
# Finally, return the full list item.
        return f"{whitespace}*{self.separator}[{title_text}]({title_reference})"


class MDTOC:
    """ Parses the markdown document and creates an array of MDTOCItem objects
        representing each TOC item. """

    def __init__(
            self, file: File, linked: bool = False,
            min_indent: int = 1, max_indent: int = 6, excluded_levels: List[int] = [],
            whitespace: str = "\t", separator: str = " "):
        """ Create a new MDTOC object, automatically parsing the input file. """
        # Set some important properties.
        self.linked: bool = linked
        self.min_indent: int = max(0, min_indent)
        self.max_indent: int = max(0, max_indent)
        self.excluded_levels: List[int] = excluded_levels
        self.whitespace: str = whitespace
        self.separator: str = separator
        # Set the lines' property based on the return value of the get_file_contents function.
        self.lines: Strings = get_file_contents(file)
        # Create the regexp object used to match lines.
        self.heading_re: re.Pattern = re.compile(r"^\s*#+\s.*$")
# Call the 'get_headings' function to get all headings from the document.
        # This list will hold each matched line.
        self.headings: Strings = self.get_headings()
        # Next, get a list of MDTOCItems using the 'get_items' function.
        self.items = self.get_items()

    def get_headings(self) -> Strings:
        """ Uses the pre-defined regular expression to find all headings within
            the markdown document. """
        # Initialise the list of headings.
        headings: Strings = []
        # Loop through all the lines of the file.
        for line in self.lines:
            # Trim out any unneeded whitespace.
            line = line.strip()
            # Match the line to the heading re.
            match: re.Match = self.heading_re.match(line)
            # Check if this line matches the heading pattern.
            if bool(match):
                # We have a match, so add it to our list of headings.
                headings.append(line)
# Return the list of headings.
        return headings

    def get_items(self) -> List[MDTOCItem]:
        """ Generates and returns a list of MDTOCItem objects to be used to
            generate the table of contents. """
        # Initialise the items list.
        items: List[MDTOCItem] = []
        # Now that we have all the headings in the document, loop through them.
        for heading in self.headings:
            # Find out what level of heading this is by getting the amount of
            # '#' characters at the start.
            whitespace_re: re.Pattern = re.compile(r"\s")
            words: Strings = whitespace_re.split(heading.strip())
            level: int = len(words[0])
            # If this level of heading has been excluded, continue and ignore it.
            if level in self.excluded_levels:
                continue
            # Otherwise, create an MDTOCItem object representing this item.
            li: MDTOCItem = MDTOCItem(
                level, words[1:], self.min_indent, self.max_indent, self.whitespace, self.separator)
            items.append(li)
        # Finally, return the list of list items.
        return items

    def get_toc(self) -> Strings:
        """ Returns the markdown representation of the table of contents. """
        # Initiate the text variable to hold the returned TOC.
        text: str = ""
        # Loop through all of the list items in the items list.
        for item in self.items:
            # Check whether we need to return linked or non-linked list items as part of the TOC.
            if self.linked:
                # If we do want links:
                # Append the returned text of the current item's to the lines list.
                text += item.get_list_item_linked() + linesep
                # If we don't want links
            else:
                # Append the returned text of the current item's to the lines list.
                text += item.get_list_item_nonlinked() + linesep
        # Finally, return the text.
        return text
