import json
from datetime import datetime
from pathlib import Path

from typer import Option, Typer

from . import Hal9000
from . import __doc__ as docstring
from . import default_config

cli = Typer(help=docstring)


hal_dir = Path.home() / ".hal"
config_path = hal_dir / "config.json"
if not hal_dir.exists():
    hal_dir.mkdir()
    with open(config_path, "w") as f:
        json.dump(default_config, f)
    print(f"Created blank hal config at {config_path}")

with open(config_path, "r") as f:
    existing_config = json.load(f)


@cli.command()
def configure(
    username: str = Option(default=existing_config["username"], prompt="Username"),
    password: str = Option(default=existing_config["password"], prompt="Password"),
    region: str = Option(
        default=existing_config["region"],
        prompt="Region",
        help="The region in which instances will be created",
    ),
    volume_id: str = Option(
        default=existing_config["volume_id"],
        prompt="Volume ID",
        help="The EBS volume where data and code will be stored",
    ),
    image_id: str = Option(
        default=existing_config["image_id"],
        prompt="Image ID",
        help="The default AMI used when instances start up",
    ),
    subnet_id: str = Option(
        default=existing_config["subnet_id"],
        prompt="Subnet ID",
        help="The subnet in which instances should be created",
    ),
    security_group: str = Option(
        default=existing_config["security_group"],
        prompt="Security group",
        help="The security group in which instances should be created",
    ),
    role_arn: str = Option(
        default=existing_config["role_arn"],
        prompt="Role ARN",
        help="The ARN of the role used to manage instances",
    ),
    instance_profile_arn: str = Option(
        default=existing_config["instance_profile_arn"],
        prompt="Instance profile ARN",
        help="The ARN of the instance profile",
    ),
    key_path: Path = Option(
        default=existing_config["key_path"],
        prompt="Key path",
        help="The ssh key used to communicate with instances",
    ),
):
    """Create the config.json file used to run HAL"""

    config = {
        "username": username,
        "password": password,
        "region": region,
        "volume_id": volume_id,
        "image_id": image_id,
        "subnet_id": subnet_id,
        "security_group": security_group,
        "role_arn": role_arn,
        "instance_profile_arn": instance_profile_arn,
        "key_path": str(key_path.expanduser().resolve()),
    }

    config_path = hal_dir / "config.json"
    with open(config_path, "w") as f:
        json.dump(config, f)


@cli.command()
def connect():
    """
    Open an ssh connection to your instance. Replaces the current process with
    a new shell running on the remote machine.
    """
    Hal9000().open_connection_to_instance()


@cli.command()
def describe():
    """Describes any currently running instances"""
    print(Hal9000().describe_instances())


@cli.command()
def get(
    local_path: Path = Option(
        ..., help="The path where the fetched file should be saved"
    ),
    remote_path: Path = Option(
        ..., help="The path of the file to fetch from the remote machine"
    ),
):
    """Fetch a file from the remote instance via sftp"""
    Hal9000(set_up_ssh=True).get_file(local_path, remote_path)


@cli.command()
def put(
    local_path: Path = Option(
        ..., help="The path of the file to send on the local machine"
    ),
    remote_path: Path = Option(
        ..., help="The path where the file should be saved on the remote machine"
    ),
):
    """Send a file to the remote instance via sftp"""
    Hal9000(set_up_ssh=True).send_file(local_path, remote_path)


@cli.command()
def start(
    instance_type: str,
    spot_price: float = Option(
        default=None, help="The price you're willing to pay per hour"
    ),
):
    """
    Create a new instance of a specified type.
    Valid options are listed at https://aws.amazon.com/ec2/spot/pricing/.
    If --spot-price is not specified, it will be automatically calculated at
    1.1x the best available price
    """
    hal = Hal9000()
    if hal.instance:
        raise ValueError(
            "Looks like you already have an instance running!\n"
            "instance_id: " + hal.instance.id
        )

    instance_name = f"{instance_type}-{datetime.now().date().isoformat()}"
    instance_id, spot_price = hal.create_instance(
        instance_type, instance_name=instance_name, spot_price=spot_price
    )
    print(f"instance_id:\t{instance_id}\nspot_price:\t£{spot_price}")
    hal.set_up_ssh()
    hal.attach_volume()
    hal.mount_volume()
    hal.fix_dns()
    # hal.send_file(
    #     local_path=Path("./enable_ipywidgets").resolve(),
    #     remote_path="/home/ec2-user/enable_ipywidgets",
    # )
    hal.start_jupyterlab()
    hal.open_connection_to_instance()


@cli.command()
def stop():
    """Shut down a running instance"""
    hal = Hal9000()
    instance_id = hal.instance.id
    hal.terminate_instance()

    print("Successfully shut down instance: " + instance_id)


@cli.command("open")
def _open():
    """Open the pod bay doors"""
    config_path = Path("~/.hal/config.json").expanduser()
    with open(config_path, "r") as f:
        config = json.load(f)

    user_name = config["username"].title()
    print(f"I'm sorry, {user_name}. I'm afraid I can't do that.")


def main():
    cli()


if __name__ == "__main__":
    cli()
