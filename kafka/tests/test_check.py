# (C) Datadog, Inc. 2019-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

import pytest

from .common import KAFKA_E2E_METRICS


@pytest.mark.e2e
def test(dd_agent_check):
    instance = {}
    aggregator = dd_agent_check(instance)

    for metric in KAFKA_E2E_METRICS:
        aggregator.assert_metric(metric)

    # import pdb
    # pdb.set_trace()
    # print("end!!")