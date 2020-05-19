import os

import boto3
from botocore.exceptions import ClientError

import pytest

from moto import mock_ssm

from cli.src import ssm_client
from cli.src.ssm_cli import CliConfiguration, DEFAULT_SSM_CONFIG_PARAMS


@pytest.fixture(scope='function')
def aws_credentials(tmpdir):
    fake_aws_creds = tmpdir.join("fake_aws_credentials_file")
    fake_aws_creds.write("[default]\nAWS_ACCESS_KEY_ID=testing\nAWS_SECRET_ACCESS_KEY=testing\nregion=eu-west-1")

    """Mocked AWS Credentials for moto."""
    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    os.environ['AWS_SECURITY_TOKEN'] = 'testing'
    os.environ['AWS_SESSION_TOKEN'] = 'testing'
    os.environ['AWS_SHARED_CREDENTIALS_FILE'] = str(fake_aws_creds)
    os.environ['AWS_CONFIG_FILE'] = str(fake_aws_creds)
    os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'


@pytest.fixture
def fake_ssm_cli_config(tmpdir):
    config_tmpdir = tmpdir.join("fake_ssm_credentials_file")
    config = CliConfiguration(config_tmpdir)
    config.setup(**DEFAULT_SSM_CONFIG_PARAMS)
    yield config


@pytest.fixture
def fake_ssm_boto_client(aws_credentials):
    with mock_ssm():
        yield boto3.client('ssm')


# noinspection PyUnusedLocal
def test_should_get_value_when_found(fake_ssm_boto_client, fake_ssm_cli_config):
    fake_ssm_boto_client.put_parameter(Name='some-param', Value='some-value', Type='SecureString')

    client = ssm_client.SSMClient(fake_ssm_cli_config)

    client_result = client.get('some-param')
    assert client_result == 'some-value'


def test_should_get_value_not_decrypted_when_configured(fake_ssm_boto_client, fake_ssm_cli_config):
    fake_ssm_cli_config.default_profile()['auto_decrypt_secret_value'] = 'False'

    fake_ssm_boto_client.put_parameter(Name='some-param', Value='some-value', Type='SecureString')

    client = ssm_client.SSMClient(fake_ssm_cli_config)

    client_result = client.get('some-param')
    assert client_result == 'kms:alias/aws/ssm:some-value'


def test_should_throw_boto_client_error_when_parameter_not_found(fake_ssm_boto_client, fake_ssm_cli_config):
    with pytest.raises(ClientError):
        client = ssm_client.SSMClient(fake_ssm_cli_config)
        client.get('some-param')


def test_should_return_empty_list_when_no_parameters_to_describe(fake_ssm_boto_client, fake_ssm_cli_config):
    client = ssm_client.SSMClient(fake_ssm_cli_config)

    client_result = client.describe("/nothing/here/to/describe")
    assert len(client_result) == 0
    assert client_result == []


def test_should_describe_all_when_no_path_given(fake_ssm_boto_client, fake_ssm_cli_config):
    fake_ssm_boto_client.put_parameter(Name='some-param1', Value='some-value1', Type='SecureString')
    fake_ssm_boto_client.put_parameter(Name='some-param2', Value='some-value2', Type='SecureString')

    client = ssm_client.SSMClient(fake_ssm_cli_config)

    client_result = client.describe()
    assert len(client_result) == 2
    assert client_result == ['some-param1', 'some-param2']


def test_should_describe_for_a_specific_given_path(fake_ssm_boto_client, fake_ssm_cli_config):
    fake_ssm_boto_client.put_parameter(Name='expected_path/some-param1', Value='some-value1', Type='SecureString')
    fake_ssm_boto_client.put_parameter(Name='expected_path/some-param2', Value='some-value2', Type='SecureString')
    fake_ssm_boto_client.put_parameter(Name='other_path/some-param3', Value='some-value3', Type='SecureString')

    client = ssm_client.SSMClient(fake_ssm_cli_config)

    client_result = client.describe('/expected_path')
    assert len(client_result) == 2
    assert client_result == ['expected_path/some-param1', 'expected_path/some-param2']


def test_should_throw_boto_client_error_when_describe_incorrectly(fake_ssm_boto_client, fake_ssm_cli_config):
    with pytest.raises(ClientError):
        client = ssm_client.SSMClient(fake_ssm_cli_config)
        client.describe('this-path-is-wrong-you-will-get-an-error')


def test_should_put_encrypted_value_by_default(fake_ssm_boto_client, fake_ssm_cli_config):
    client = ssm_client.SSMClient(fake_ssm_cli_config)

    client.put('some-param', 'some-value', 'some-description')

    expected_result = fake_ssm_boto_client.get_parameter(Name='some-param', WithDecryption=True)

    assert expected_result['Parameter']['Value'] == 'some-value'


def test_should_put_non_encrypted_value_when_configured(fake_ssm_boto_client, fake_ssm_cli_config):
    fake_ssm_cli_config.default_profile()['auto_encrypt_secret_value'] = 'False'

    client = ssm_client.SSMClient(fake_ssm_cli_config)

    client.put('some-param', 'some-value', 'some-description')

    expected_result = fake_ssm_boto_client.get_parameter(Name='some-param', WithDecryption=False)

    assert expected_result['Parameter']['Value'] == 'some-value'
