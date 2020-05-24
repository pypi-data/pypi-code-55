# -*- coding: utf-8 -*-
# (c) 2020 Martin Wendt and contributors; see https://github.com/mar10/yabs
# Licensed under the MIT license: https://www.opensource.org/licenses/mit-license.php
"""
"""
# import pytest

from test_release_tool.main import run


class TestVersionManager:
    def test_basics(self):
        assert run() == 42
