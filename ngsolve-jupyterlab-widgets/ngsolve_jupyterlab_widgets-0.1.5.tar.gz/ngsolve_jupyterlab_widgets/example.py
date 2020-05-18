#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Matthias Hochsteger.
# Distributed under the terms of the Modified BSD License.

"""
TODO: Add module docstring
"""

from ipywidgets import DOMWidget, register
from traitlets import Unicode
from ._frontend import module_name, module_version

@register
class NGSWebGuiWidget(DOMWidget):
    from traitlets import Dict, Unicode
    _view_name = Unicode('NGSolveView').tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)
    render_data = Dict({"ngsolve_version":'0.0.0'}).tag(sync=True)


@register
class ExampleWidget(DOMWidget):
    """TODO: Add docstring here
    """

    _model_name = Unicode("ExampleModel").tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode("ExampleView").tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    value = Unicode("Hello World").tag(sync=True)
