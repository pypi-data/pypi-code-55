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
Tests for reading and parsing reMarkable tablet metadata.
"""

from remt import meta as r_meta
from remt.error import *

import pytest
from unittest import mock

def test_fn_path():
    """
    Test creating UUID based path from metadata.
    """
    meta = {'uuid': 'xyz'}
    result = r_meta.fn_path(meta, base='/x/y', ext='.met')
    assert '/x/y/xyz.met' == result

@pytest.mark.asyncio
async def test_read_meta():
    """
    Test reading metadata.
    """
    sftp = mock.MagicMock()
    sftp.mget = mock.AsyncMock()
    dir_meta = 'dir'

    with mock.patch('glob.glob') as mock_glob, \
            mock.patch('json.load') as mock_json_load, \
            mock.patch('builtins.open') as mock_open:  # noqa: F841

        mock_glob.side_effect = [
            # let's make read_meta resistant to some filesystem
            # inconsistencies by introducing non-matching files
            ['f1.content', 'f2.content', 'f3.content', 'f5.content'],
            ['f1.metadata', 'f2.metadata', 'f3.metadata', 'f4.metadata'],
        ]
        mock_json_load.side_effect = [
            {'visibleName': 'f1', 'deleted': False},
            {'pages': 3},

            # deleted filename shall not be visible in the results
            {'visibleName': 'f2', 'deleted': True},
            {'pages': 4},

            {'visibleName': 'f3'},
            {'pages': 5},
            {'visibleName': 'f4'},
            {'pages': 6},
        ]
        result = await r_meta.read_meta(sftp, dir_meta)
        assert ['f1', 'f2', 'f3'] == list(result)
        assert {'pages': 3} == result['f1']['content']
        assert {'pages': 4} == result['f2']['content']
        assert {'pages': 5} == result['f3']['content']

def test_fn_metadata_error():
    """
    Test if error is raised if there is no metadata for a path.
    """
    meta = {'a/b/': 1}

    with pytest.raises(FileError):
        r_meta.fn_metadata(meta, 'x/y')

# vim: sw=4:et:ai
