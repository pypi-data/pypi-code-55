import pytest


@pytest.fixture
def hub(hub):
    hub.pop.sub.add(dyne_name="corn")
    hub.pop.sub.add(dyne_name="exec")
    hub.pop.sub.add(dyne_name="states")

    hub.corn.init.standalone()

    return hub
