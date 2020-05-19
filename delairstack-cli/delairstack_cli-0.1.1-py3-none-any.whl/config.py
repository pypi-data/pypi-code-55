from appdirs import user_data_dir
from collections import namedtuple
import configparser
from pathlib import Path
from typing import Optional

from delairstack import DelairStackSDK
import typer

from delairstack_cli import utils


Credentials = namedtuple('Credentials', ['username', 'password', 'url', 'proxy_url'])

DEFAULT_CONF_DIR = Path(user_data_dir('delairstack'))
DEFAULT_CREDENTIAL_PATH = DEFAULT_CONF_DIR / 'credentials'
DEFAULT_PROFILE = 'default'
DEFAULT_URL = 'https://www.delair.ai'


def get_credentials(*, credential_path: Path, profile: str) -> Optional[Credentials]:
    if credential_path.exists():
        try:
            config = configparser.RawConfigParser()
            config.read(credential_path)
            credentials = Credentials(
                username=config[profile]['username'],
                password=config[profile]['password'],
                url=config[profile]['url'],
                proxy_url=config[profile].get('proxy_url')
            )
            return credentials

        except (configparser.MissingSectionHeaderError, KeyError):
            return None
    else:
        return None


def check_credentials(credentials: Credentials) -> bool:
    try:
        DelairStackSDK(
            user=credentials.username,
            password=credentials.password,
            url=credentials.url,
            proxy_url=credentials.proxy_url,
            connection={'max_retries': 1}
        )
    except Exception:
        return False

    return True  # Connection OK = valid credentials


def save_config(credentials: Credentials, *, credential_path: Path,
                profile: str) -> None:
    config = configparser.RawConfigParser()
    credential_dict = credentials._asdict()

    if credentials.proxy_url is None:
        credential_dict.pop('proxy_url')

    config[profile] = credential_dict

    if not credential_path.parent.exists():
        Path(credential_path.parent).mkdir(parents=True, exist_ok=True)

    with open(credential_path, 'w') as configfile:
        config.write(configfile)


def setup(credential_path: Path = DEFAULT_CREDENTIAL_PATH,
          *, profile: str = DEFAULT_PROFILE) -> Credentials:

    welcome_msg = typer.style(
        'Alright. Let\'s configure your credentials to connect to the platform.',
        fg=typer.colors.GREEN,
        bold=True
    )
    print(welcome_msg)
    print()

    existing_credentials = get_credentials(
        credential_path=credential_path,
        profile=profile
    )

    if existing_credentials:
        confirmation_msg = typer.style(
            'A configuration file already exists. Do you want to replace it ?',
            fg=typer.colors.RED
        )
        typer.confirm(confirmation_msg, abort=True)
        username = typer.prompt(
            typer.style('Email', bold=True),
            type=str,
            default=existing_credentials.username
        )
        password = typer.prompt(
            typer.style('Password ', bold=True) +
            '[Press ENTER to keep password unchanged]',
            type=str,
            default=existing_credentials.password,
            show_default=False,
            hide_input=True
        )
        url = typer.prompt(
            typer.style('Platform URL', bold=True),
            type=str,
            default=existing_credentials.url
        )
        proxy_url = typer.prompt(
            typer.style('Proxy URL', bold=True),
            type=str,
            default=existing_credentials.proxy_url or '',
        )

    else:
        username = typer.prompt(typer.style('Email', bold=True), type=str)
        password = typer.prompt(
            typer.style('Password', bold=True) + ' (will not be displayed)',
            type=str,
            hide_input=True
        )
        url = typer.prompt(
            typer.style('Platform URL', bold=True) +
            ' (or press ENTER to set {})'.format(DEFAULT_URL),
            type=str,
            default=DEFAULT_URL,
            show_default=False
        )
        proxy_url = typer.prompt(
            typer.style('Proxy URL', bold=True) +
            ' (or press ENTER if not applicable)',
            type=str,
            default='',
            show_default=False
        )

    if proxy_url == '':
        proxy_url = None

    credentials = Credentials(
        username=username,
        password=password,
        url=url,
        proxy_url=proxy_url
    )
    print()

    print('Checking credentials...')
    with utils.spinner():
        valid = check_credentials(credentials)

    if not valid:
        invalid_cred_msg = typer.style(
            '✖ Cannot connect with the supplied credentials. '
            'Do you want to save this configuration anyway ?',
            fg=typer.colors.RED
        )
        typer.confirm(invalid_cred_msg, abort=True)
    else:
        valid_cred_msg = typer.style(
            '✓ Connection OK with these credentials',
            fg=typer.colors.GREEN
        )
        print(valid_cred_msg)

    save_config(credentials, credential_path=credential_path, profile=profile)

    saved_cred_msg = typer.style(
        '✓ Credentials saved in {!r}'.format(credential_path),
        fg=typer.colors.GREEN
    )
    print(saved_cred_msg)
    print()

    return credentials
