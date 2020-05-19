import mock
import pytest


@pytest.fixture(scope="session")
def hub(hub):
    # TODO Add dynes that will be used for your tests
    for dyne in ():
        hub.pop.sub.add(dyne_name=dyne)

    args = [
        # TODO patch in whatever cli args are necessary to run your test
    ]
    with mock.patch("sys.argv", ["pytest-pop"] + args):
        hub.pop.config.load(["pytest_pop"], "pytest_pop")
    return hub
