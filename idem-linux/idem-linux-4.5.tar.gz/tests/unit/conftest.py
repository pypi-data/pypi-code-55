import pytest


@pytest.fixture(scope="session")
def hub(base_hub):
    """
    provides a full hub that is used as a reference for mock_hub
    """
    base_hub.pop.sub.add(dyne_name="corn")
    base_hub.pop.sub.add(dyne_name="exec")
    base_hub.pop.sub.add(dyne_name="states")

    return base_hub


@pytest.fixture(scope="function")
def c_hub(hub):
    """
    A hub specific to corn unit testing
    Scope is function so that CORN values are clean with every run
    """
    mock_hub = hub.pop.testing.mock_hub()
    mock_hub.corn.init.clean_value = hub.corn.init.clean_value
    mock_hub.pop.data.imap = hub.pop.data.imap
    mock_hub.corn.CORN = hub.pop.data.omap()
    return mock_hub
