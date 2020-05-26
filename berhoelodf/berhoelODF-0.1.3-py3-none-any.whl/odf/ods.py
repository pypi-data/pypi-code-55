#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Processing ods (OpenDocument spreadsheets).
"""

# Standard libraries.
import re
import typing
import datetime
import functools

from . import Odf, OdfXml

__date__ = "2020/05/26 23:21:45 hoel"
__author__ = "Berthold Höllmann"
__copyright__ = "Copyright © 2020 by Berthold Höllmann"
__credits__ = ["Berthold Höllmann"]
__maintainer__ = "Berthold Höllmann"
__email__ = "berhoel@gmail.com"

# 'of:=HYPERLINK("http://www.imdb.com/title/tt0094612/";"Action Jackson")'
IMDB_HYPERLINK = re.compile(
    r"of:=HYPERLINK\(\s*"
    r'"(?P<url>https?://www.imdb.com/title/tt[0-9]+)'
    r'(?:/?(?:[?]ref_=(?:[a-z]{2}_)+(?:[0-9]{1,3}|[a-z]{1,3})|(?:episodes))?)?"\s*;\s*'
    r'"(?P<name>.+)"\s*\)'
)

# of:=-['k&v'.F207]
LINKED_CELL = re.compile(
    r"of:=-(:?[-+]?[0-9]*\.?[0-9]*[-+*/])*\[\$?'k\&v'\.F(?P<line>[0-9]+)]"
)


class P(OdfXml):
    "Representing a paragraph in a cell."

    @property
    def text(self) -> typing.Optional[str]:
        "Return paragraph text."
        res = " ".join([i for i in self.root.itertext()])
        return res if res.strip() else None


class Cell(OdfXml):
    "Representing a cell in a table row."

    @property
    def text(self) -> typing.Optional[str]:
        "Return text associated with cell."
        if self.root is None:
            return None
        res = self.find("text:p")
        return None if res is None else P(res).text

    @property
    def date(self) -> typing.Optional[datetime.date]:
        "Return date value of cell if avaliable."
        val = self.get("office:date-value")
        return (
            None if val is None else datetime.datetime.strptime(val, "%Y-%m-%d").date()
        )

    @property
    def value(self) -> typing.Optional[str]:
        "return value of cell."
        return self.get("office:value")

    @property
    def float(self) -> typing.Optional[float]:
        "Return float value of cell."
        return None if self.value is None else float(self.value)

    @property
    def int(self) -> typing.Optional[int]:
        "Return integer value of cell."
        return None if self.value is None else int(self.value)

    @property
    def url(self) -> typing.Optional[str]:
        "Return URL associated with cell from hyperlink function."
        s_val: str = self.get("table:formula")
        val = None if s_val is None else IMDB_HYPERLINK.match(s_val)
        return None if val is None else val.group("url")

    @property
    def link(self) -> typing.Optional[typing.Dict[str, str]]:
        "Provide Link information."
        dvd_link: str = self.get("table:formula")
        if dvd_link is not None:
            match = LINKED_CELL.match(dvd_link)
            if match is not None:
                return match.groupdict()
        return None


class Row(OdfXml):
    "Representing table row."

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.content_cell: str = self._attrib_map("table:table-cell")
        self.covered_cell: str = self._attrib_map("table:covered-table-cell")
        self.columns_repeated: str = self._attrib_map("table:number-columns-repeated")

    @functools.cached_property
    def cells(self) -> typing.List[typing.Optional[Cell]]:
        "Provide list of cells in row."
        res: typing.List[typing.Optional[Cell]] = []
        for i, cell in enumerate(self.root):
            if cell.tag == self.content_cell:
                elem = Cell(cell)
                res.extend(
                    [elem]
                    * (
                        int(elem.get("table:number-columns-repeated"))
                        if self.columns_repeated in cell.attrib
                        else 1
                    )
                )
            elif cell.tag == self.covered_cell:
                elem = Cell(cell)
                res.extend(
                    [None]
                    * (
                        int(elem.get("table:number-columns-repeated"))
                        if self.columns_repeated in cell.attrib
                        else 1
                    )
                )
            else:
                import pdb

                pdb.set_trace()
                pass

        return res


class Table(OdfXml):
    "Representation of spreadsheet table"

    @functools.cached_property
    def name(self) -> str:
        "Return name attriute of table-"
        return self.get("table:name")

    @functools.cached_property
    def rows(self) -> typing.List[Row]:
        "Retrun rows in table."
        return [Row(e) for e in self.findall("table:table-row")]

    @functools.cached_property
    def style_name(self) -> str:
        """Return table style-name.

I Know of `ta1` for ordinary tables, and `ta2` for hidden tables."""
        return self.get("table:style-name")

    @property
    def hidden(self) -> bool:
        "Return whether table is hidden."
        return self.style_name == "ta2"


class Ods(Odf):
    "Processing ODS files."

    def __init__(self, *args, **kw):
        """
        Open ODF spreadsheet file.
        """
        super().__init__(*args, **kw)

        self.root = self.find("office:body/office:spreadsheet")

    @functools.cached_property
    def tables(self) -> typing.List[Table]:
        "Return all tables in spreadsheet:"
        return [Table(e) for e in self.findall("table:table")]


# Local Variables:
# mode: python
# compile-command: "poetry run tox"
# time-stamp-pattern: "30/__date__ = \"%:y/%02m/%02d %02H:%02M:%02S %u\""
# End:
