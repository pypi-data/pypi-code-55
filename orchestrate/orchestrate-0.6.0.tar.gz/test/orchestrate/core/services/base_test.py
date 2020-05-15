from mock import Mock

from orchestrate.core.services.base import Service


class TestService(object):
  def test_services(self):
    mock_services = Mock()
    services = Service(mock_services)
    assert services.services is not None
