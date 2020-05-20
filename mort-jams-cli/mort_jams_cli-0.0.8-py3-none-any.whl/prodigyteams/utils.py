from typing import Optional, Tuple
import os
import sys
import time
import json
from pathlib import Path
from typing import Any, Dict, List, Sequence, Callable
from datetime import datetime, timedelta
from functools import update_wrapper

import requests
import typer
from wasabi import Printer, color

auth_wait_time_seconds = 60 * 5
# Used for identifying the app to generate the directory to store the tokens locally
# On Linux, it ends up at ~/.config/prodigy-teams/
app_name = "prodigy-teams"

scope = "openid profile email"
grant_type = "urn:ietf:params:oauth:grant-type:device_code"


class Broker:
    def __init__(self, *, address: str = None, token: str = None):
        self.address = address
        self.token = token


class CLIConfig:
    def __init__(
        self,
        *,
        api_host: str,
        device_audience: str,
        device_client_id: str,
        device_token_url: str,
        device_code_url: str,
    ):
        self.api_host = api_host if not api_host.endswith("/") else api_host[:-1]
        self.device_audience = device_audience
        self.device_client_id = device_client_id
        self.device_token_url = device_token_url
        self.device_code_url = device_code_url

    @staticmethod
    def from_dict(obj: dict) -> "CLIConfig":
        return CLIConfig(
            api_host=obj["host"],
            device_audience=obj["daudience"],
            device_client_id=obj["dclient_id"],
            device_token_url=obj["dtoken_url"],
            device_code_url=obj["dcode_url"],
        )


class State:
    def __init__(
        self,
        *,
        id_token: str = None,
        api_token: str = None,
        broker: Broker = None,
        projects: List[dict] = None,
        tasks: List[dict] = None,
    ):
        self.id_token = id_token
        self.api_token = api_token
        self.broker = broker
        self.projects = projects
        self.tasks = tasks


class ClickPrinter(Printer):
    def text(
        self,
        title="",
        text="",
        color=None,
        icon=None,
        spaced=False,
        show=True,
        no_print=False,
        exits=None,
    ):
        text = super().text(
            title=title,
            text=text,
            color=color,
            icon=icon,
            spaced=spaced,
            show=show,
            no_print=True,
            exits=exits,
        )
        if no_print:
            return text
        typer.echo(text)


class ProdigyTeamsAPIException(Exception):
    pass


class ProdigyTeamsIDException(Exception):
    pass


printer = ClickPrinter()

state = State()


def dicts_to_table(data: Sequence[Dict[str, Any]]):
    """
    Generate a tuple with headers and rows in the format wasabi expects from a list
    of dicts having column names as keys.
    """
    headers: List[str] = []
    if not data:
        return headers, data
    use_data = list(data)
    headers = list(use_data[0].keys())
    rows = []
    for item in data:
        row = []
        for key in headers:
            row.append(item[key])
        rows.append(row)
    return headers, rows


def authenticate_device_and_get_id_token():
    config: CLIConfig = get_cli_config()

    response = requests.post(
        config.device_code_url,
        data={
            "client_id": config.device_client_id,
            "scope": scope,
            "audience": config.device_audience,
        },
    )
    if response.status_code != 200:
        printer.fail("Could not communicate with the device authentication API.")
        sys.exit(1)
    data = response.json()
    device_code = data.get("device_code")
    user_code = data.get("user_code")
    verification_uri = data.get("verification_uri")
    data.get("expires_in")
    interval = data.get("interval", 5)
    verification_uri_complete = data.get("verification_uri_complete")
    if not (
        device_code
        and user_code
        and verification_uri
        and interval
        and verification_uri_complete
    ):
        printer.fail("The device authentication API sent an incomplete response.")
        sys.exit(1)
    typer.launch(verification_uri_complete)
    printer.divider("Logging in...")
    printer.good("Opening browser to authenticate...")
    printer.divider()
    printer.info(
        "If a browser doesn't open automatically after some seconds, you can copy and open this link:"
    )
    printer.info(color(f"{verification_uri_complete}", fg="green"))
    printer.info("Alternatively, you can manually open:")
    printer.info(color(f"{verification_uri}", fg="green"))
    printer.info("And type the code:")
    printer.info(color(f"{user_code}", fg="green"))
    last_check = 0
    with typer.progressbar(range(auth_wait_time_seconds)) as seconds:
        for second in seconds:
            if time.time() > (last_check + int(interval)):
                token_response = requests.post(
                    config.device_token_url,
                    data={
                        "grant_type": grant_type,
                        "device_code": device_code,
                        "client_id": config.device_client_id,
                    },
                )
                last_check = time.time()
                token_data = token_response.json()
                if token_response.status_code == 200:
                    id_token = token_data.get("id_token")
                    printer.divider()
                    printer.good("Login successful")
                    printer.divider()
                    return id_token
            time.sleep(1)


def get_config_dir_path() -> Path:
    config_path = Path(typer.get_app_dir(app_name))
    config_path.mkdir(parents=True, exist_ok=True)
    return config_path


def get_id_token_path() -> Path:
    config_path = get_config_dir_path()
    return config_path / "id_token"


def get_api_token_path() -> Path:
    config_path = get_config_dir_path()
    return config_path / "api_token"


def fetch_cli_json(host: str) -> dict:
    api_response = requests.get(f"{host}/v1/cli.json")
    if api_response.status_code != 200:
        raise ProdigyTeamsIDException()
    return api_response.json()


def get_cli_host_path() -> Path:
    config_path = get_config_dir_path()
    host_path = config_path / "api_host"
    if not host_path.is_file():
        host_path.write_text("https://api.prodigy.rest")
    return host_path


def get_cli_json_path() -> Path:
    config_path = get_config_dir_path()
    return config_path / "cli.json"


def set_cli_host(host_name: str) -> None:
    """Set the CLI host environment to a specific target."""

    try:
        config_dict = fetch_cli_json(host_name)
    except BaseException as e:
        printer.fail(f"Unable to set CLI host to: {host_name}\nFailed with error: {e}")
        raise typer.Abort()
    host_path = get_cli_host_path()
    host_path.write_text(host_name)
    json_path = get_cli_json_path()
    json_path.write_text(json.dumps(config_dict, indent=2))
    printer.info(f"Set CLI host to: {host_name}")


def get_cli_config() -> CLIConfig:
    host: str = get_cli_host_path().read_text()
    json_path = get_cli_json_path()
    if not json_path.is_file():
        config_dict = fetch_cli_json(host)
        json_path.write_text(json.dumps(config_dict, indent=2))
    else:
        config_dict = json.loads(json_path.read_text())
    try:
        return CLIConfig.from_dict(config_dict)
    except KeyError:
        # fetch the file fresh if it's missing keys
        config_dict = fetch_cli_json(host)
        json_path.write_text(json.dumps(config_dict, indent=2))
    return CLIConfig.from_dict(config_dict)


def get_cache_path() -> Path:
    config_path = get_config_dir_path()
    return config_path / "cache.json"


def get_fresh_id_token():
    id_token = authenticate_device_and_get_id_token()
    id_token_path = get_id_token_path()
    id_token_path.write_text(id_token)
    state.id_token = id_token
    return id_token


def get_id_token():
    if state.id_token:
        return state.id_token
    id_token_file = get_id_token_path()
    if id_token_file.is_file():
        id_token = id_token_file.read_text()
        state.id_token = id_token
        return id_token
    return get_fresh_id_token()


def retry_id(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ProdigyTeamsIDException:
            get_fresh_id_token()
            try:
                return func(*args, **kwargs)
            except Exception as e:
                printer.fail("Error authenticating device and user with Prodigy Teams.")
                raise e

    return wrapper


def retry_api(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ProdigyTeamsAPIException:
            get_fresh_api_token()
            try:
                return func(*args, **kwargs)
            except Exception as e:
                printer.fail("Error communicating with Prodigy Teams API.")
                raise e

    return wrapper


def retry(func):
    @retry_api
    @retry_id
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


@retry_id
def get_fresh_api_token():
    config: CLIConfig = get_cli_config()
    id_token = get_id_token()
    api_response = requests.post(
        f"{config.api_host}/v1/api-token",
        headers={"authorization": f"Bearer {id_token}"},
    )
    if api_response.status_code != 200:
        raise ProdigyTeamsIDException()
    data = api_response.json()
    token = data.get("access_token")
    token_file = get_api_token_path()
    token_file.write_text(token)
    state.api_token = token
    return token


def get_api_token():
    if state.api_token:
        return state.api_token
    token_file: Path = get_api_token_path()
    if token_file.is_file():
        api_token = token_file.read_text()
        state.api_token = api_token
        return api_token
    else:
        return get_fresh_api_token()


@retry
def get_fresh_identity_data():
    config: CLIConfig = get_cli_config()

    id_token = get_id_token()
    api_response = requests.post(
        f"{config.api_host}/v1/identity",
        headers={"Authorization": f"Bearer {id_token}"},
    )
    if api_response.status_code != 200:
        raise ProdigyTeamsIDException()
    api_data = api_response.json()
    brokers = api_data.get("brokers")
    if not brokers:
        printer.fail("You need to first create a broker")
        raise typer.Abort()
    broker = brokers[0]
    state.broker = Broker()
    state.broker.token = broker.get("token")
    state.broker.address = broker.get("address")
    state.projects = api_data.get("projects", [])
    state.tasks = api_data.get("tasks", [])
    return state


@retry
def get_broker():
    if state.broker:
        return state.broker
    get_fresh_identity_data()
    return state.broker


@retry
def get_broker_meta():
    broker = get_broker()
    response = requests.get(
        f"{broker.address}/api/v1/broker/meta",
        headers={"authorization": f"Bearer {broker.token}"},
    )
    if response.status_code != 200:
        raise ProdigyTeamsIDException()
    data = response.json()
    return data


def local_cache(expire_seconds=300) -> Callable:
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> Any:
            cache_path = get_cache_path()
            if cache_path.is_file():
                cache_text = cache_path.read_text()
                try:
                    cache_data: dict = json.loads(cache_text)
                except json.JSONDecodeError:
                    cache_data = {}
            else:
                cache_data = {}
            func_key = f"{func.__module__}:{func.__name__}"
            args_key = ""
            if args:
                args_key += "-".join([str(arg) for arg in args])
            if kwargs:
                args_key += "_".join([f"{k}:{v}" for k, v in kwargs.items()])
            if func_key in cache_data:
                func_data = cache_data[func_key]
                call_data = func_data.get(args_key)
                if call_data:
                    expire = call_data.get("expire")
                    if expire:
                        try:
                            expire_datetime = datetime.strptime(
                                expire, "%Y-%m-%dT%H:%M:%S.%f"
                            )
                            now = datetime.now()
                            if expire_datetime > now:
                                if "data" in call_data:
                                    return call_data["data"]
                        except ValueError:
                            pass
            # Data was not returned, re-compute
            data = func(*args, **kwargs)
            new_func_data = cache_data.setdefault(func_key, {})
            new_expire_datetime = datetime.now() + timedelta(seconds=expire_seconds)
            new_func_data[args_key] = {
                "expire": new_expire_datetime.isoformat(),
                "data": data,
            }
            new_cache_text = json.dumps(cache_data)
            cache_path.write_text(new_cache_text)
            return data

        update_wrapper(wrapper, func)
        return wrapper

    return decorator


@local_cache(expire_seconds=300)
def get_cached_broker_meta():
    return get_broker_meta()


def get_packages():
    broker = get_broker()
    headers = {"Authorization": f"Bearer {broker.token}"}
    response = requests.get(f"{broker.address}/api/v1/packages", headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data
    typer.echo(f"Error fetching data: {response.text}", err=True)
    raise typer.Abort()


@local_cache(expire_seconds=300)
def get_cached_packages():
    return get_packages()


def get_binaries_for_package(package: str):
    broker = get_broker()
    headers = {"Authorization": f"Bearer {broker.token}"}
    response = requests.get(
        f"{broker.address}/api/v1/packages/{package}/", headers=headers
    )
    if response.status_code == 200:
        data = response.json()
        return data
    typer.echo(f"Error fetching data: {response.text}", err=True)
    raise typer.Abort()


@local_cache(expire_seconds=300)
def get_cached_binaries_for_package(package: str):
    return get_binaries_for_package(package)
