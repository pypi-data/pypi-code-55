import pytest
from mock import Mock

from orchestrate.core.services.aws_provider_bag import AwsProviderServiceBag


class TestOrchestrateServiceBag(object):
  @pytest.fixture
  def orchestrate_services(self):
    return Mock()

  def test_orchestrate_service_bag(self, orchestrate_services):
    services = AwsProviderServiceBag(orchestrate_services, aws_access_key_id='foo', aws_secret_access_key='bar')
    assert services.autoscaling_service is not None
    assert services.autoscaling_service.client is not None
    assert services.cloudformation_service is not None
    assert services.cloudformation_service.client is not None
    assert services.cloudformation_service.cloudformation is not None
    assert services.ec2_service is not None
    assert services.ec2_service.ec2 is not None
    assert services.ecr_service is not None
    assert services.ecr_service.client is not None
    assert services.eks_service is not None
    assert services.eks_service.client is not None
    assert services.iam_service is not None
    assert services.iam_service.client is not None
    assert services.iam_service.iam is not None
    assert services.sts_service is not None
    assert services.sts_service.client is not None
