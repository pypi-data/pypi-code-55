import pytest


@pytest.fixture
def hub(hub):
    hub.pop.sub.add(dyne_name="foo")
    hub.foo.func = lambda x: x
    yield hub


def test_autospec(hub, mock_hub):
    val = "12345"
    # Call a function on the mock hub
    mock_hub.foo.func(val)

    # Verify that the function was called with the given parameter
    mock_hub.foo.func.assert_called_once_with(val)


def test_logging(hub, mock_hub):
    # Verify that basic logging substitutions have been made
    assert hub.log.trace is mock_hub.log.trace
    assert hub.log.warning is mock_hub.log.warning
    assert hub.log.error is mock_hub.log.error
    assert hub.log.critical is mock_hub.log.critical


def test_pop(mock_hub):
    # Verify that basic pop substitutions have been made
    assert hub.pop.loop.create is mock_hub.pop.loop.create
    assert hub.pop.data.imap is mock_hub.pop.data.imap
