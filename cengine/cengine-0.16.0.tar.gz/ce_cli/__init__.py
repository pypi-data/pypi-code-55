#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This is the Command Line Utilities for maiot Core Engine.

.. currentmodule:: ce_cli
.. moduleauthor:: maiot GmbH <support@maiot.io>
"""
import ce_api
from .auth import login, logout, whoami, reset

from .datasource import list_datasources, create_datasource, set_datasource
from .workspace import list_workspaces, create_workspace, set_workspace

from .evaluation import evaluate, compare

from .pipeline import list_pipelines, configure_pipeline, pull_pipeline, \
    push_pipeline, run_pipeline, get_pipeline_status
from .version_cli import version


from .pipeline_utils import *
