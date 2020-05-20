# -*- coding: utf-8 -*-
import asyncio
import _pytest.python as pythtest
import mock
import os
import pop.hub
import pytest
import sys
import logging
from typing import Any, Dict, List

log = logging.getLogger("pytest_pop.plugin")


def pytest_sessionstart(session: pytest.Session):
    CODE_DIR = session.config.invocation_dir
    TPATH_DIR = os.path.join(CODE_DIR, "tpath")
    if CODE_DIR in sys.path:
        sys.path.remove(CODE_DIR)
    sys.path.insert(0, CODE_DIR)
    if TPATH_DIR in sys.path:
        sys.path.remove(TPATH_DIR)
    sys.path.insert(0, TPATH_DIR)


@pytest.fixture(autouse=True)
def hub(event_loop):
    hub = pop.hub.Hub()

    # Set up the rudimentary logger
    hub.pop.sub.add(dyne_name="log")

    # use the event loop from pytest-asyncio
    if asyncio._get_running_loop() is not event_loop:
        asyncio.set_event_loop(event_loop)
    hub.pop.loop.create()
    assert hub.pop.Loop is event_loop

    log.debug("Initialized hub fixture")
    yield hub


@pytest.fixture(autouse=True, scope="function")
def mock_hub(hub):
    # swap out some fake functions for real ones
    mock_hub = hub.pop.testing.mock_hub()
    for val in dir(hub.log):
        if not val.startswith("_"):
            setattr(mock_hub.log, val, getattr(hub.log, val))
    for s in hub.pop._subs:
        sub = getattr(hub.pop, s)
        for val in dir(sub):
            if not val.startswith("_"):
                setattr(getattr(mock_hub.pop, s), val, sub)
    yield mock_hub


@pytest.fixture
def acct_subs() -> List[str]:
    raise NotImplementedError("Override the 'acct_subs' fixture in your conftest.py")


@pytest.fixture
def acct_profile() -> str:
    raise NotImplementedError("Override the 'acct_profile' fixture in your conftest.py")


@pytest.fixture
@pytest.mark.asyncio
async def ctx(hub, acct_subs: List[str], acct_profile: str) -> Dict[str, Any]:
    """
    Set up the context for idem-cloud executions
    :param acct_subs: The output of an overridden fixture of the same name
    :param acct_profile: The output of an overridden fixture of the same name
    """
    ctx = {
        "run_name": "test",
        "test": False,
    }

    old_opts = hub.OPT

    if not (hasattr(hub, "acct") and hasattr(hub, "states")):
        log.debug("Creating a temporary hub to generate ctx")
        # Use a fresh hub
        hub = pop.hub.Hub()
        # Add the bare minimum of
        for dyne in ("acct", "states"):
            hub.pop.sub.add(dyne_name=dyne)

    if not (
        hub.OPT.get("acct")
        and hub.OPT.acct.get("acct_file")
        and hub.OPT.acct.get("acct_key")
    ):
        # Get the account information from environment variables
        log.debug("Loading temporary config from idem and acct")
        with mock.patch("sys.argv", ["pytest_pop"]):
            hub.pop.config.load(["idem", "acct"], "idem", parse_cli=False)

    # Add the profile to the account
    hub.acct.init.unlock(hub.OPT.acct.acct_file, hub.OPT.acct.acct_key)
    ctx["acct"] = await hub.acct.init.gather(acct_subs, acct_profile)

    hub.OPT = old_opts

    yield ctx


def pytest_runtest_protocol(item: pythtest.Function, nextitem: pythtest.Function):
    """
    implements the runtest_setup/call/teardown protocol for
    the given test item, including capturing exceptions and calling
    reporting hooks.
    """
    log.debug(f">>>>> START >>>>> {item.name}")


def pytest_runtest_teardown(item: pythtest.Function):
    """
    called after ``pytest_runtest_call``
    """
    log.debug(f"<<<<< END <<<<<<< {item.name}")


@pytest.fixture(scope="session", autouse=True)
def os_sleep_secs():
    if "CI_RUN" in os.environ:
        return 1.75
    return 0.5
