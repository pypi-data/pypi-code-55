# -*- coding: utf-8 -*-
# Copyright (c) 2020 kaliko <kaliko@azylum.org>
#
#  This file is part of sima
#
#  sima is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  sima is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with sima.  If not, see <http://www.gnu.org/licenses/>.
#
#
"""
Blacklisting plugin
"""

# standard library import
import random

# third parties components

# local import
from ...lib.plugin import Plugin
from ...lib.meta import Artist


class Blacklist(Plugin):
    """TO Be Writen
    """

    def __init__(self, daemon):
        super().__init__(daemon)
        self.daemon = daemon
        if not self.plugin_conf:
            return
        self.mode = self.plugin_conf.get('flavour', None)

    def callback_filter_track(self):
        pass
        #return trks


# VIM MODLINE
# vim: ai ts=4 sw=4 sts=4 expandtab
