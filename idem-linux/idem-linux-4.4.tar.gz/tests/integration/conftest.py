import pytest


@pytest.fixture(scope="session")
def hub(base_hub):
    base_hub.pop.sub.add(dyne_name="corn")
    base_hub.pop.sub.add(dyne_name="exec")
    base_hub.pop.sub.add(dyne_name="states")

    base_hub.corn.init.standalone()

    return base_hub
