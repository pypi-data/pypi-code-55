import getpass
import json
import os
import yaml
from pathlib import Path
from typing import Any, Dict, Optional

import hvac
import requests
from dbt.exceptions import RuntimeException
from dbt.logger import GLOBAL_LOGGER as logger
from dbt.ui.printer import green, red, yellow


def from_url(url: str, params: Optional[Dict[str, Any]] = None) -> requests.Response:
    """Load data from url

    Args:
        url (str): [description]
        params (Optional[Dict[str, Any]], optional): [description]. Defaults to None.

    Returns:
        requests.Response: [description]
    """
    result = requests.get(url=url, params=params)
    logger.info(f"[JINJA2] Request [{result.url}]: {result.status_code}")
    return result


def from_env(env: str) -> Optional[str]:
    """Load data from env variable.

    Args:
        env (str): Env variable name

    Returns:
        str: env variable
    """
    result = os.getenv(env)
    return result


def from_file(filepath: str) -> str:
    """Load data from file

    Args:
        filepath (str): filepath

    Returns:
        str: file content
    """
    path_ = Path(filepath)
    logger.info(f"[JINJA2] Reading from file {str(path_)}")
    result = path_.read_text()
    return result


def from_vault_token(url: str, token: str, verify=False) -> hvac.Client:
    """Create client of Hashicorp Vault. Token authorization.

    Args:
        url (str): vault url
        token (str): authorization token
        verify (bool): wheter verify TLS

    Returns:
        hvac.Client: vault client.
    """
    client = hvac.Client(url=url, token=token, verify=verify)
    logger.info(f"[JINJA2] Vault {url} authenticated {client.is_authenticated()}")
    return client


def from_vault_ldap(
    url: str, username: str, password: str, verify=False,
) -> hvac.Client:
    """Create client of Hashicorp Vault. LDAP authorization.

    Args:
        url (str): vault url
        username (str): ldap username
        password (str): ldap password
        verify (bool): wheter verify TLS

    Returns:
        hvac.Client: vault client.
    """
    client = hvac.Client(url=url, verify=verify)
    client.auth.ldap.login(username=username, password=password)
    logger.info(f"[JINJA2] Vault {url} authenticated {client.is_authenticated()}")
    return client


def load_json(data: str) -> Dict[str, Any]:
    """Load string representing json into dictionary.

    Args:
        data (str): string

    Returns:
        Dict[str, Any]: parsed string
    """
    result = json.loads(data)
    return result


def load_yaml(data: str) -> Dict[str, Any]:
    """Load string representing yaml into dictionary.

    Args:
        data (str): string

    Returns:
        Dict[str, Any]: parsed string
    """
    result = yaml.safe_load(data)
    return result


def whoami() -> str:
    """Get current username.

    Returns:
        str: username
    """
    return getpass.getuser()


def log_yellow(text: str):
    """Log with yellow color.

    Args:
        text (str): Log text
    """
    logger.info(yellow(text))


def log_red(text: str):
    """Log with red color.

    Args:
        text (str): Log text
    """
    logger.info(red(text))


def log_green(text: str):
    """Log with green color.

    Args:
        text (str): Log text
    """
    logger.info(green(text))


def log(text: str):
    """Log.

    Args:
        text (str): Log text
    """
    logger.info(text)


def raise_exception(text: str):
    """Raise exception.

    Args:
        text (str): error text

    Raises:
        RuntimeException: error
    """
    raise RuntimeException(text)
