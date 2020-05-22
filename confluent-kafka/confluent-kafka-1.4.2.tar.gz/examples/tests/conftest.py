#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2020 Confluent Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from uuid import uuid4

import pytest

from tests.integration.cluster_fixture import TrivupFixture


class Args(object):
    __slots__ = ['bootstrap_servers', 'schema_registry']

    def __init__(self, kafka_cluster):
        self.schema_registry = kafka_cluster.schema_registry_conf()['url']
        self.bootstrap_servers = kafka_cluster.client_conf()['bootstrap.servers']

    @property
    def topic(self):
        return "test_example-" + str(uuid4())

    @property
    def group_id(self):
        return "test_example-" + str(uuid4())


@pytest.fixture(scope="package")
def args():
    cluster = TrivupFixture({'with_sr': True})

    args = Args(cluster)
    try:
        yield args
    finally:
        cluster.stop()
