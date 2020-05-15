#
# remt - reMarkable tablet command-line tools
#
# Copyright (C) 2018-2020 by Artur Wroblewski <wrobell@riseup.net>
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""
PDF annotations indexer.
"""

import cytoolz.functoolz as ftz
import textwrap

from .data import Page, Stroke
from .pdf import pdf_text
from .util import split

FMT_PAGE = 'Page {} ({})'.format

def ann_text(pdf_doc, items):
    """
    Get annotated text from PDF document using document items parsed from
    reMarkable file.
    """
    to_text = ftz.curry(pdf_text)
    is_item = ftz.flip(isinstance, (Page, Stroke))
    is_page = ftz.flip(isinstance, Page)
    get_page = pdf_doc.get_page

    # find pages and strokes
    items = (v for v in items if is_item(v))

    # split into (page, strokes)
    items = split(is_page, items)

    # get PDF pages
    items = ((get_page(p.number), s) for p, s in items)

    # for each page and stroke get text under stroke
    items = ((p, map(to_text(p), s)) for p, s in items)

    yield from items

def fmt_ann_text(items):
    """
    Format annotated text read from PDF document as reStructuredText
    document.
    """
    items = ((fmt_header(p), fmt_text(t)) for p, t in items)
    yield from items

def fmt_header(page):
    """
    Format page header in reStructuredText format.
    """
    header = FMT_PAGE(page.get_label(), page.get_index())
    return '{}\n{}'.format(header, '=' * len(header))

def fmt_text(texts):
    """
    Format collection of text items in reStructuredText format.
    """
    result = '\n\n'.join(t for t in texts if t)
    result = textwrap.indent(result, ' ' * 4)
    result = '::\n\n{}\n'.format(result)
    return result


# vim: sw=4:et:ai
