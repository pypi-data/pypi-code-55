# -*- coding: utf-8 -*-
"""
test_download
~~~~~~~~~~~~~

Test downloading.

"""

import os
import csv
import shutil
import tempfile

import pytest

from chemistry_tools.pubchem.images import get_structure_image
from chemistry_tools.pubchem.properties import rest_get_properties


@pytest.fixture(scope='module')
def tmp_dir():
	tmpdir = tempfile.mkdtemp()
	yield tmpdir
	shutil.rmtree(tmpdir)


def test_image_download(tmp_dir):
	img = get_structure_image("Asprin")
	img.save(os.path.join(tmp_dir, 'aspirin.png'))


def test_csv_download(tmp_dir):
	csv_content = rest_get_properties([1, 2, 3], namespace="cid", properties="CanonicalSMILES,IsomericSMILES", format_="csv")
	with open(os.path.join(tmp_dir, 's.csv'), "w") as fp:
		fp.write(csv_content)

	with open(os.path.join(tmp_dir, 's.csv')) as f:
		rows = list(csv.reader(f))
		assert rows[0] == ['CID', 'CanonicalSMILES', 'IsomericSMILES']
		assert rows[1][0] == '1'
		assert rows[2][0] == '2'
		assert rows[3][0] == '3'
