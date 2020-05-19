from collections import defaultdict
from pathlib import Path
from botocore.exceptions import ClientError
from configparser import ConfigParser
import click
import pyperclip

from cli.src.ssm_client import SSMClient

DEFAULT_CONFIG_PATH = '~/.ssm/config'
DEFAULT_AWS_CONFIG_PATH = '~/.aws/credentials'
DEFAULT_SSM_CONFIG_PARAMS = {
    'profile_name': 'default',
    'auto_decrypt_secret_value': True,
    'auto_encrypt_secret_value': True
}

pass_client = click.make_pass_decorator(SSMClient)


class CliConfiguration:
    DEFAULT_PROFILE_NAME = 'default'

    def __init__(self, path):
        self.config_path = Path(path)
        self.config = ConfigParser()

        self.config.read(self.config_path.expanduser())

    def exists(self):
        return self.config_path.expanduser().exists()

    def has_multiple_profiles(self):
        return len(self.config.sections()) > 1

    def setup(self, **config_properties):
        self.config[self.DEFAULT_PROFILE_NAME] = config_properties

        self.config_path.parent.expanduser().mkdir(parents=True, exist_ok=True)

        with self.config_path.expanduser().open(mode='w') as configfile:
            self.config.write(configfile)

        self.config.read(self.config_path.expanduser())

    def default_profile(self):
        return self.config[self.DEFAULT_PROFILE_NAME]

    def profiles(self):
        return self.config.sections()

    def get_bool_value(self, key, section=DEFAULT_PROFILE_NAME):
        return self.config.getboolean(section, key)

    def should_auto_encrypt_secret_value(self, section=DEFAULT_PROFILE_NAME):
        return self.get_bool_value('auto_encrypt_secret_value', section)

    def should_auto_decrypt_secret_value(self, section=DEFAULT_PROFILE_NAME):
        return self.get_bool_value('auto_decrypt_secret_value', section)


@click.group()
@click.option('--config_path', default=DEFAULT_CONFIG_PATH,
              help="Path to the cli configuration file. Default is '{}'".format(DEFAULT_CONFIG_PATH), hidden=True)
@click.pass_context
def cli(ctx, config_path):
    config = CliConfiguration(config_path)

    if not config.exists():
        click.secho("You are running this cli with default aws configuration. It is recommended you run 'ssm configure'"
                    " to better define your aws creds.", fg='yellow')
        ctx.obj = SSMClient(config)
    else:
        ctx.obj = SSMClient(config, profile_name=config.default_profile()['profile_name'])


@cli.command(name='configure', help='Setup an initial configuration for this cli')
@click.option('-s', '--show_configuration', is_flag=True, help="Shows the current configuration if already set.")
@click.option('-p', '--profile_name', help="Sets the specific AWS profile you wish to work with."
                                           "If you just have one AWS profile this option is irrelevant")
def configure_client(profile_name, show_configuration=False, path=DEFAULT_CONFIG_PATH):
    aws_config = CliConfiguration(DEFAULT_AWS_CONFIG_PATH)

    if not aws_config.exists():
        click.secho("Could not find an aws configure file."
                    " Please run 'aws configure' and enter your aws credentials", fg='red')
        click.secho("If you do not have aws-cli installed. You can read this article and follow accordingly: "
                    "https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html", fg='red')
        raise click.Abort

    ssm_config = CliConfiguration(path)

    if show_configuration:
        click.echo(dict(ssm_config.default_profile()))
        return

    ssm_config_parameters = defaultdict(object, DEFAULT_SSM_CONFIG_PARAMS)

    if profile_name:
        ssm_config_parameters['profile_name'] = profile_name
    elif aws_config.has_multiple_profiles():
        click.echo("It seems you are using multiple profiles in your aws credentials file.")
        selected_profile_name = click.prompt('Which AWS Profile would you like to use?',
                                             type=click.Choice(aws_config.profiles(), case_sensitive=False))
        ssm_config_parameters['profile_name'] = selected_profile_name

    ssm_config.setup(**ssm_config_parameters)

    click.echo("Will be using aws credentials from profile '{}'"
               .format(click.style(ssm_config_parameters.get('profile_name'), fg='green')))
    click.secho("New configuration saved in '{}'".format(DEFAULT_CONFIG_PATH), fg='green')


@cli.command(name='get', help='Retrieve a specific secret.')
@click.option('-c', '--copy', is_flag=True, help='''Copies the secret value to your clipboard''')
@click.argument('secret_key')
@pass_client
def get_secret(client, secret_key, copy):
    try:
        value = client.get(secret_key)

        if copy:
            pyperclip.copy(value)
            click.secho("Secret copied to clipboard!", fg='green')
        else:
            click.secho(value, fg='green')
    except ClientError:
        raise click.UsageError(click.style("Parameter Key '{}' not found!".format(secret_key), fg='red'))


@cli.command(name='describe', help='Retrieve a list of available secrets')
@click.option('-c', '--copy', is_flag=True, help='''Copies the selected secret value to your clipboard''')
@click.option('-g', '--get', is_flag=True, help='''Give you a prompt to choose which secret to get''')
@click.option('-p', '--path', default=None, help='''Describe only parameters located in a specific path \
                                                 (must start with "/")''')
@pass_client
@click.pass_context
def describe_secrets(ctx, client, path, get, copy):
    secrets = client.describe(path)

    if not secrets:
        raise click.UsageError(click.style("Could not find any secrets to describe!", fg='red'))

    if not get:
        click.secho("\n".join(secrets), fg='green')
    else:
        click.echo("Select the secret index to get it's value")

        for index, value in enumerate(secrets):
            click.echo("[{}] {}".format(index + 1, value))

        secret_index = click.prompt("\nSelect a Secret by its index")

        selected_secret = secrets[int(secret_index) - 1]

        ctx.invoke(get_secret, secret_key=selected_secret, copy=copy)


@cli.command(name='put', help='Submit a new secret to the SSM store. Please enter the key name.'
                              ' Once submitted, a prompt will be opened to enter the actual secret value')
@click.argument('secret_key')
@pass_client
def put_secret(client, secret_key):
    value = click.prompt("What should be the value of the secret key '{}'? ".format(secret_key),
                         hide_input=True)
    description = click.prompt("Would you like to add a description to the '{}' secret? ".format(secret_key))

    client.put(secret_key, value, description)

    click.secho("Successfully created secret '{}'!".format(secret_key), fg='green')


if __name__ == '__main__':
    cli()
