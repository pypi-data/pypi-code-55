"""
Verify that the hub is part of everything
"""


def test_session_hub(hub, session_hub):
    hub.test_value = "12345"
    assert not hasattr(session_hub, "test_value")


def test_module_hub(hub, module_hub):
    hub.test_value = "12345"
    assert not hasattr(module_hub, "test_value")


def test_function_hub(hub, function_hub):
    hub.test_value = "12345"
    assert not hasattr(function_hub, "test_value")


def test_mock_hub(mock_hub):
    mock_hub.log.debug("Mocking a hub")


def setup_module(module):
    hub = module.hub
    hub.log.debug("Setup module")


def setup_function(function):
    hub = function.hub
    hub.log.debug("Setup function")


def test_function(hub):
    hub.log.debug("test function")


class TestHub:
    @classmethod
    def setup_class(cls):
        hub = cls.hub
        hub.log.debug("Setup class")

    def test_method(self):
        hub = self.hub
        hub.log.debug("test method")

    @classmethod
    def teardown_class(cls):
        hub = cls.hub
        hub.log.debug("Teardown class")


def teardown_function(function):
    hub = function.hub
    hub.log.debug("Teardown function")


def teardown_module(module):
    hub = module.hub
    hub.log.debug("Teardown module")
