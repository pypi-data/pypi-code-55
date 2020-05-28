import pytest
import os
import sys
import yaml
from time import sleep
import multiprocessing as mp
import requests
from importlib import reload

import pipemaker.master
from pipemaker import pipeline as p
from pipemaker.examples import example1
from pipemaker.examples.example1 import *
from pipemaker.utils.defaultlog import log


def test_sync():
    # setup
    p.reset()
    p.add(example1)
    p.mode = "s"
    p.delay = 0

    # execute
    for low in [10, 15, 25]:
        p.low = low
        p.path = f"low{p.low}"
        make_oddeven()

    # check results
    p.low = 15
    p.path = f"low{p.low}"
    assert p.load("oddeven") == [15, 16, 17, 18, 19, 20]


def run_pipeline():
    """ target for process so each run starts from scratch """
    try:
        # setup
        p.reset()
        p.add(example1)
        p.mode = "a"
        # ensures progress reporting tested
        p.delay = 2

        # check view runs
        assert len(make_oddeven.view().body) == 21

        # execute
        for low in [10, 15, 25]:
            p.low = low
            p.path = f"low{p.low}"
            make_oddeven()

        # check web view
        r = requests.get("http://localhost:5000")
        assert r.status_code == 200

        # wait for finish
        for low in [10, 15, 25]:
            p.low = low
            p.path = f"low{p.low}"
            make_oddeven.wait()

        # can be delay between files available and tasks finished
        for x in range(5):
            df = p.view()
            if all(df.status == "completed"):
                break
            log.warning("waiting for tasks in taskdb to complete")
            sleep(1)

        # check results
        p.low = 15
        p.path = f"low{p.low}"
        assert p.load("oddeven") == [15, 16, 17, 18, 19, 20]

        # check all on task list, completed, used min 3 processes.
        df = p.view()
        assert len(df) == 9
        assert all(df.status == "completed")
        assert len(df.process.unique()) >= 3

        # shutdown
        p.stop()
    except:
        log.exception("exception in run_pipeline")


@pytest.mark.parametrize("broker", ["qrabbit", "qpython"])
def test_async(broker):
    # read from default. write to test.
    confpath = ".pipemaker/config.yaml"
    with open(f"../../{confpath}") as f:
        testconfig = yaml.safe_load(f)
    testconfig["qtype"] = broker
    os.makedirs(".pipemaker", exist_ok=True)
    with open(confpath, "w") as f:
        f.write(yaml.dump(testconfig))

    run_pipeline()


if __name__ == "__main__":
    test_async("qrabbit")
