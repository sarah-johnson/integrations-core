# (C) Datadog, Inc. 2020-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

from __future__ import absolute_import

import os
from typing import Iterator

import pytest

from datadog_checks.dev import WaitFor, docker_run
from datadog_checks.rethinkdb._types import Instance

from .cluster import setup_cluster
from .common import CONNECT_SERVER_PORT, HERE, HOST, IMAGE, PROXY_PORT

E2E_METADATA = {'start_commands': ['pip install rethinkdb==2.4.4']}


@pytest.fixture(scope='session')
def instance():
    # type: () -> Instance
    return {
        'host': HOST,
        'port': CONNECT_SERVER_PORT,
    }


@pytest.fixture(scope='session')
def dd_environment(instance):
    # type: (Instance) -> Iterator
    compose_file = os.path.join(HERE, 'compose', 'docker-compose.yaml')

    env_vars = {
        'RETHINKDB_IMAGE': IMAGE,
        'RETHINKDB_CONNECT_SERVER_PORT': str(CONNECT_SERVER_PORT),
        'RETHINKDB_PROXY_PORT': str(PROXY_PORT),
    }

    conditions = [WaitFor(setup_cluster)]

    log_patterns = [
        r'Server ready, "server0".*',
        r'Connected to server "server1".*',
        r'Connected to server "server2".*',
        r'Connected to proxy.*',
    ]

    with docker_run(compose_file, conditions=conditions, env_vars=env_vars, log_patterns=log_patterns):
        config = {'instances': [instance]}
        yield config, E2E_METADATA
