#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import json

from collections import namedtuple

from .decorator import waitingdots
from .config import databricks

from taz.databricks import Workspace, Cluster

workspace = Workspace(token=databricks["token"])


def dictfilter(d, keys):
    return dict(zip(keys, [d[k] for k in keys]))


@waitingdots
def test_010_list_clusters():
    for cluster in workspace.get_clusters().clusters:
        print(dictfilter(cluster.__dict__, ["cluster_name", "cluster_id", "state"]))


@waitingdots
def test_020_list_jobs():
    for job in workspace.get_jobs().jobs:
        print(
            {
                "job_id": job.job_id,
                "job_name": job.settings["name"],
                "existing_cluster_id": job.settings.get("existing_cluster_id", None),
                "new_cluster": job.settings.get("new_cluster", None),
            }
        )


@waitingdots
def test_030_list_runs():
    for run in workspace.get_runs().runs:
        print(
            json.dumps(
                dictfilter(run.__dict__, ["job_id", "run_id", "state"]), indent=2
            )
        )


@waitingdots
def test_040_find_cluster_by_id():
    cluster_id = workspace.get_clusters().clusters[0].cluster_id
    print(workspace.get_cluster_by_id(cluster_id).cluster_name)


@waitingdots
def test_050_find_cluster_by_name():
    cluster_name = workspace.get_clusters().clusters[1].cluster_name
    print(workspace.get_cluster_by_name(cluster_name).cluster_name)
