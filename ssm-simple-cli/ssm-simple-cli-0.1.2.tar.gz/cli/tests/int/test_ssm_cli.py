import os

import boto3
import pytest
from click.testing import CliRunner
from moto import mock_ssm

from cli.src import ssm_cli
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

    yield fake_aws_creds


@pytest.fixture
def fake_ssm_cli_config(tmpdir):
    config_tmpdir = tmpdir.join("fake_ssm_credentials_file")
    config = CliConfiguration(config_tmpdir)
    config.setup(**DEFAULT_SSM_CONFIG_PARAMS)
    yield config_tmpdir


@pytest.fixture
def fake_ssm_boto_client(aws_credentials):
    with mock_ssm():
        yield boto3.client('ssm')


# noinspection PyUnusedLocal
def test_should_get_value_when_found(fake_ssm_boto_client, fake_ssm_cli_config):
    fake_ssm_boto_client.put_parameter(Name='some-param', Value='some-value', Type='SecureString')

    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(ssm_cli.cli, ['--config_path', fake_ssm_cli_config, 'get', 'some-param'])
        assert result.output == 'some-value\n'
        assert result.exit_code == 0


# noinspection PyUnusedLocal
def test_should_return_not_found_message_when_parameter_not_found(fake_ssm_boto_client, fake_ssm_cli_config):
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(ssm_cli.cli, ['--config_path', fake_ssm_cli_config, 'get', 'some-unknown-value'])
        assert 'some-unknown-value' in result.output
        assert 'not found!' in result.output
        assert result.exit_code == 2


# noinspection PyUnusedLocal
def test_should_put_value_successfully(fake_ssm_boto_client, fake_ssm_cli_config):
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(ssm_cli.cli, ['--config_path', fake_ssm_cli_config, 'put', 'some-param'],
                               input='some-value\nsome-desc\n')
        returned_parameter = fake_ssm_boto_client.get_parameter(Name='some-param', WithDecryption=True)

        assert returned_parameter['Parameter']['Value'] == 'some-value'
        assert result.exit_code == 0


# noinspection PyUnusedLocal
def test_should_describe_all_parameters_by_name_and_path(fake_ssm_boto_client, fake_ssm_cli_config):
    fake_ssm_boto_client.put_parameter(Name='/some-path/some-param1', Value='not-relevant', Type='SecureString')
    fake_ssm_boto_client.put_parameter(Name='some-param2', Value='not-relevant', Type='SecureString')

    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(ssm_cli.cli, ['--config_path', fake_ssm_cli_config, 'describe'])

        assert result.output == '/some-path/some-param1\nsome-param2\n'
        assert result.exit_code == 0
