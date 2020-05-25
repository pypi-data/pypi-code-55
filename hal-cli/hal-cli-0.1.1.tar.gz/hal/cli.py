import json
from datetime import datetime
from pathlib import Path

from typer import Option, Typer, prompt
from wasabi import Printer

from hal import Hal9000
from hal import __doc__ as docstring
from hal import get_config, get_config_path

state = {"config": get_config(), "config_name": "config"}
cli = Typer(help=docstring, no_args_is_help=True)
msg = Printer()


@cli.command()
def configure():
    """
    Configure profiles used to run HAL.
    See help at `docs/install/configuration.md`
    """
    config = {
        "username": prompt(
            text="Username", default=state["config"]["username"], type=str,
        ),
        "region": prompt(
            text="Region", default=state["config"]["region"], type=str,
        ),
        "volume_id": prompt(
            text="Volume ID", default=state["config"]["volume_id"], type=str,
        ),
        "image_id": prompt(
            text="Image ID", default=state["config"]["image_id"], type=str,
        ),
        "subnet_id": prompt(
            text="Subnet ID", default=state["config"]["subnet_id"], type=str,
        ),
        "security_group": prompt(
            text="Security group",
            default=state["config"]["security_group"],
            type=str,
        ),
        "role_arn": prompt(
            text="Role ARN", default=state["config"]["role_arn"], type=str,
        ),
        "instance_profile_arn": prompt(
            text="Instance profile ARN",
            default=state["config"]["instance_profile_arn"],
            type=str,
        ),
        "ssh_key_path": str(
            Path(
                prompt(
                    text="SSH key path",
                    default=state["config"]["ssh_key_path"],
                    type=Path,
                )
            )
            .expanduser()
            .resolve()
        ),
        "ssh_password": prompt(
            text="SSH password",
            default=state["config"]["ssh_password"],
            type=str,
        ),
    }
    config_path = get_config_path(state["config_name"])
    with open(config_path, "w") as f:
        json.dump(config, f)


@cli.command()
def connect():
    """
    Open an ssh connection to your instance. Replaces the current process with
    a new shell running on the remote machine.
    """
    h = Hal9000(state["config"])
    h.open_connection_to_instance()


@cli.command()
def describe():
    """Describe any currently running instances."""
    h = Hal9000(state["config"])
    h.describe_instances()


@cli.command()
def get(
    local_path: Path = Option(
        ..., help="The path where the fetched file should be saved"
    ),
    remote_path: Path = Option(
        ..., help="The path of the file to fetch from the remote machine"
    ),
):
    """Fetch a file from the remote instance via sftp."""
    h = Hal9000(state["config"], set_up_sftp=True)
    h.get(local_path, remote_path)


@cli.command()
def put(
    local_path: Path = Option(
        ..., help="The path of the file to send on the local machine"
    ),
    remote_path: Path = Option(
        ...,
        help="The path where the file should be saved on the remote machine",
    ),
):
    """Send a file to the remote instance via sftp."""
    h = Hal9000(state["config"], set_up_sftp=True)
    h.put(local_path, remote_path)


@cli.command()
def start(
    instance_type: str,
    spot_price: float = Option(
        default=None, help="The price you're willing to pay per hour"
    ),
    connect: bool = Option(
        default=False,
        help="If True, opens an new shell on the instance on startup",
    ),
):
    """
    Create a new instance of a specified type.
    Valid options are listed [here](https://aws.amazon.com/ec2/spot/pricing/).
    If --spot-price is not specified, a bid will be automatically calculated at
    1.1x the best available price.
    """
    h = Hal9000(state["config"])
    instance_name = f"{instance_type}-{datetime.now().date().isoformat()}"
    h.start_instance(instance_type, instance_name, spot_price)
    if connect:
        h.open_connection_to_instance()


@cli.command()
def stop():
    """Shut down a running instance."""
    h = Hal9000(state["config"])
    h.shut_down_instance()


@cli.command("open")
def _open():
    """Open the pod bay doors."""
    username = state["config"]["username"].title()
    msg.fail(f"I'm sorry, {username}. I'm afraid I can't do that.")


@cli.callback()
def config_callback(
    config: str = Option(
        default="config",
        help="The name of the config file to use",
        show_default=True,
    ),
):
    state["config_name"] = config
    state["config"] = get_config(config)


def main():
    cli()
