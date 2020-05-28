#!/usr/bin/env python
# -*- coding: utf-8 -*-

from taz.exception import (
    DatabricksClusterIdNotFoundException,
    DatabricksClusterNameNotFoundException,
)

from taz.http import HttpRequest
import json


class Cluster:
    def __init__(self, **entries):
        if entries is not None:
            self.__dict__.update(entries)


class Job:
    def __init__(self, **entries):
        if entries is not None:
            self.__dict__.update(entries)


class Run:
    def __init__(self, **entries):
        if entries is not None:
            self.__dict__.update(entries)


class Workspace:
    def __init__(self, token, url="https://northeurope.azuredatabricks.net"):
        self.token = token
        self.url = url
        self.clusters = []
        self.jobs = []
        self.runs = []

    def _get(self, endpoint):
        return (
            HttpRequest("{}/{}".format(self.url, endpoint))
            .set_headers(
                {
                    "Authorization": "Bearer {}".format(self.token),
                    "Content-Type": "application/json",
                }
            )
            .get()
            .response
        )

    def get_clusters(self):
        response = self._get("api/2.0/clusters/list")
        for cluster in json.loads(response.text).get("clusters"):
            self.clusters.append(Cluster(**cluster))
        return self

    def get_jobs(self):
        response = self._get("api/2.0/jobs/list")
        for job in json.loads(response.text).get("jobs"):
            self.jobs.append(Job(**job))
        return self

    def get_runs(self):
        response = self._get("api/2.0/jobs/runs/list")
        for run in json.loads(response.text).get("runs"):
            self.runs.append(Run(**run))
        return self

    def get_cluster_by_id(self, cluster_id):
        for cluster in self.clusters:
            if cluster.cluster_id == cluster_id:
                return cluster
        raise DatabricksClusterIdNotFoundException

    def get_cluster_by_name(self, cluster_name):
        for cluster in self.clusters:
            if cluster.cluster_name == cluster_name:
                return cluster
