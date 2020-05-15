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
PDF annotation indexer unit tests.
"""

from ..indexer import fmt_header, fmt_text

from unittest import mock

def test_fmt_header():
    """
    Test formatting page header in reStructuredText format.
    """
    page = mock.MagicMock()
    page.get_label.return_value = 'IX'
    page.get_index.return_value = '10'

    result = fmt_header(page)
    print(result)
    assert 'Page IX (10)\n============' == result

def test_fmt_text():
    """
    Test formatting a collection of texts in reStructuredText format.
    """
    texts = ['abc', '', 'xyz\nzyx']
    result = fmt_text(texts)
    expected = """\
::

    abc

    xyz
    zyx
"""
    assert expected == result

# vim: sw=4:et:ai
