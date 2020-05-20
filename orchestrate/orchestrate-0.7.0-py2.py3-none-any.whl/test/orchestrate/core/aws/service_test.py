import pytest
from mock import Mock

from orchestrate.core.aws.service import AwsService


class TestAwsService(object):
  @pytest.fixture()
  def aws_service(self):
    services = Mock()
    aws_services = Mock()
    return AwsService(services, aws_services)

  @pytest.mark.parametrize('cluster_name', [
    '',
    'inval_id1-123',
    'also-invalid_cluster-name',
    '123',
  ])
  def test_invalid_cluster_name(self, aws_service, cluster_name):
    with pytest.raises(AssertionError):
      aws_service.validate_cluster_options(cluster_name, 1, 2, None)

  @pytest.mark.parametrize('cluster_name', [
    'valid-123',
    'also-valid-cluster-name',
  ])
  def test_valid_cluster_names(self, aws_service, cluster_name):
    aws_service.validate_cluster_options(cluster_name, 1, 2, None)

  @pytest.mark.parametrize('kubernetes_version', [
    '1.9',
    '1.13',
    'not-a-version',
  ])
  def test_invalid_kubernetes_version(self, aws_service, kubernetes_version):
    with pytest.raises(AssertionError):
      aws_service.validate_cluster_options('cluster-name', 1, 2, kubernetes_version)

  @pytest.mark.parametrize('kubernetes_version', [
    None,
    '1.14',
    '1.15',
    '1.16',
    'latest',
  ])
  def test_valid_kubernetes_versions(self, aws_service, kubernetes_version):
    aws_service.validate_cluster_options('valid-name', 1, 2, kubernetes_version)

  def test_create_kubernetes_cluster_fail(self, aws_service):
    with pytest.raises(AssertionError):
      aws_service.create_kubernetes_cluster(dict(cluster_name="44_44", cpu=1, gpu=1))
