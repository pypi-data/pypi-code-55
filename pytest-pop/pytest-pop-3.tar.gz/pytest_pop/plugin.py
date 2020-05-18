# -*- coding: utf-8 -*-
import _pytest.config as conf
import _pytest.python as pytesthon
import copy
import mock
import pop.hub
import pytest


@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session: pytest.Session):
    """
    Initialize the hub and attach it to the pytest config
    """
    config: conf.Config = session.config
    config.hub = pop.hub.Hub()
    with mock.patch("sys.argv", ["pytest_pop"]):
        # At the very least set up logging
        config.hub.pop.config.load(["pytest_pop"], "pytest_pop", parse_cli=False)


@pytest.mark.order(0)
@pytest.fixture(scope="session", autouse=True)
def hub(pytestconfig):
    """
    provides a full hub that is used as a reference for mock_hub
    This can be extended by creating a hub() fixture in your
    own conftest.py and putting `hub` as it's first parameter
    """
    yield pytestconfig.hub


@pytest.fixture(scope="session")
def session_hub(hub):
    new_hub = copy.copy(hub)
    yield new_hub
    del new_hub


@pytest.fixture(scope="module")
def module_hub(hub):
    new_hub = copy.copy(hub)
    yield new_hub
    del new_hub


@pytest.fixture(scope="function")
def function_hub(hub):
    new_hub = copy.copy(hub)
    yield new_hub
    del new_hub


@pytest.fixture(scope="function")
def mock_hub(hub):
    mock_hub = hub.pop.testing.mock_hub()
    mock_hub.log.trace = hub.log.trace
    mock_hub.log.debug = hub.log.debug
    mock_hub.log.info = hub.log.info
    mock_hub.log.warning = hub.log.warning
    mock_hub.log.critcal = hub.log.critical
    mock_hub.log.error = hub.log.error
    yield mock_hub


def pytest_generate_tests(metafunc: pytesthon.Metafunc):
    """
    Inject the hub onto module, function, method, and class setup/teardown functions.
    Every fixture, module, function, and class will now have access to the hub.
    """
    # TODO make sure these are the hubs scoped at the right level
    # TODO for example, the hub on the module hub should be the same one returned
    # TODO by the module_hub fixture
    if metafunc.cls is not None:
        metafunc.cls.hub = metafunc.config.hub
    if metafunc.function is not None:
        metafunc.function.hub = metafunc.config.hub
    if metafunc.module is not None:
        metafunc.module.hub = metafunc.config.hub
