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
Read and parse reMarkable tablet metadata.
"""

import glob
import json
import operator
import os
from cytoolz.dicttoolz import assoc
from cytoolz.functoolz import compose
from datetime import datetime

from remt.error import *

BASE_DIR = '/home/root/.local/share/remarkable/xochitl'

def fn_path(data, base=BASE_DIR, ext='.*'):
    """
    Having metadata object create UUID based path of a file created by
    reMarkable tablet.

    :param data: Metadata object.
    """
    return '{}/{}{}'.format(base, data['uuid'], ext)

def create_metadata(is_dir, parent_uuid, name):
    now = datetime.utcnow()
    tstamp = int(now.timestamp() * 1000)
    type = 'CollectionType' if is_dir else 'DocumentType'
    data = {
        'deleted': False,
        'lastModified': str(tstamp),
        'metadatamodified': True,
        'modified': True,
        'parent': parent_uuid,
        'pinned': False,
        'synced': False,
        'type': type,
        'version': 0,
        'visibleName': name,
    }
    return data

def to_path(data, meta):
    parent = data.get('parent')
    name = data['visibleName']
    if parent:
        return to_path(meta[parent], meta) + '/' + name
    else:
        return name

def resolve_uuid(meta):
    meta = {k: assoc(v, 'uuid', k) for k, v in meta.items()}
    return {to_path(data, meta): data for data in meta.values()}

def fn_metadata(meta, path):
    """
    Get reMarkable tablet file metadata or raise file not found error if no
    metadata for path is found.

    :param meta: reMarkable tablet metadata.
    :param path: Path of reMarkable tablet file.
    """
    data = meta.get(path)
    if not data:
        raise FileError('File or directory not found: {}'.format(path))
    return data

async def read_meta(sftp, dir_meta):
    """
    Read metadata from a reMarkable tablet.
    """
    await sftp.mget(BASE_DIR + '/*.metadata', dir_meta)
    await sftp.mget(BASE_DIR + '/*.content', dir_meta)

    to_uuid = compose(
        operator.itemgetter(0),
        os.path.splitext,
        os.path.basename,
    )
    load_json = compose(json.load, open)

    files_content = glob.glob(dir_meta + '/*.content')
    files_content = {to_uuid(fn): fn for fn in files_content}

    files = glob.glob(dir_meta + '/*.metadata')
    files = ((fn, to_uuid(fn)) for fn in files)
    files = ((fn, u) for fn, u in files if u in files_content)

    # load metadata file and content file
    data = (
        (u, load_json(fn), load_json(files_content[u]))
        for fn, u in files
    )
    meta = {u: assoc(m, 'content', c) for u, m, c in data}
    return resolve_uuid(meta)

# vim: sw=4:et:ai
