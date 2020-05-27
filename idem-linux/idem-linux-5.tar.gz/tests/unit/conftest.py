import pytest


@pytest.fixture(scope="function")
def hub(hub):
    """
    provides a full hub that is used as a reference for mock_hub
    """
    hub.pop.sub.add(dyne_name="corn")
    hub.pop.sub.add(dyne_name="exec")

    yield hub


@pytest.fixture(scope="function")
def mock_hub(hub, mock_hub):
    """
    A hub specific to corn unit testing
    Scope is function so that CORN values are clean with every run
    """
    mock_hub.corn.init.clean_value = hub.corn.init.clean_value
    mock_hub.corn.CORN = hub.pop.data.omap()

    yield mock_hub

    del mock_hub.corn.CORN
