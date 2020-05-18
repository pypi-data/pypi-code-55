#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of mysql-db-backup-faster.
# https://github.com/heynemann/generator-python-package

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2020, gwangil <pki054@naver.com>

from preggy import expect

from mysql_db_backup_faster import __version__
from tests.base import TestCase


class VersionTestCase(TestCase):
    def test_has_proper_version(self):
        expect(__version__).to_equal('0.1.0')
