import mock
import pytest


# TODO redefine the scope of the hub
@pytest.fixture(scope="function")
def hub(hub):
    # TODO Add dynes that will be used for your tests
    for dyne in ():
        hub.pop.sub.add(dyne_name=dyne)
        if dyne in ("corn", "exec", "states"):
            hub.pop.sub.load_subdirs(getattr(hub, dyne), recurse=True)

    args = [
        # TODO patch in whatever cli args are necessary to run your test
    ]
    with mock.patch("sys.argv", ["pytest-pop"] + args):
        hub.pop.config.load(["pytest_pop"], "pytest_pop")

    yield hub

    # TODO Hub cleanup
    pass
