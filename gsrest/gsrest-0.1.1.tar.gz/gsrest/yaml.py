# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 Instituto Tecnológico de Canarias, S.A.
#
# This file is part of GsRest
# (see https://github.com/esuarezsantana/gsrest).
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
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
"""Geoserver rest YAML importer.
"""

import yaml

from . import collection
from .core.registry import ElementRegistry


class GsYamlError(Exception):
    "Yaml Error."


def read(yaml_path):
    "Reads a yaml file with descriptions of elements."

    def _get_yaml_contents(yaml_path):
        "Open file and get contents as a dict."
        with open(yaml_path) as fid:
            userdata = yaml.safe_load(fid)
        return userdata

    def _parse(data_blocks):
        "Get a list of elements from a Yaml file."
        for block in data_blocks:
            for elem_type, elems in block.items():
                # strip plural into singular
                klass = ElementRegistry.get(elem_type.rstrip("s"))
                for elem_attrs in elems:
                    yield klass(**elem_attrs)

    main_dikt = _get_yaml_contents(yaml_path)
    try:
        gs_data = main_dikt["elements"]
    except KeyError:
        raise GsYamlError
    return collection.ElementCollection(*_parse(gs_data))
