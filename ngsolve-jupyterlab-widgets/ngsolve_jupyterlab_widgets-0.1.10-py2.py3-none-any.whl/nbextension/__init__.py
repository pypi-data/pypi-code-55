#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Matthias Hochsteger
# Distributed under the terms of the Modified BSD License.


def _jupyter_nbextension_paths():
    return [
        {
            "section": "notebook",
            "src": "nbextension/static",
            "dest": "ngsolve_jupyterlab_widgets",
            "require": "ngsolve_jupyterlab_widgets/extension",
        }
    ]
