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


def test_log(hub, mock_hub):
    # Verify that basic logging substitutions have been made
    assert hub.log.log.func is mock_hub.log.log.func
    assert hub.log.trace is mock_hub.log.trace
    assert hub.log.warning is mock_hub.log.warning
    assert hub.log.error is mock_hub.log.error
    assert hub.log.critical is mock_hub.log.critical


def test_pop(hub, mock_hub):
    # Verify that basic pop substitutions have been made
    assert hub.pop.loop.create.func is mock_hub.pop.loop.create.func
    assert hub.pop.data.imap.func is mock_hub.pop.data.imap.func
