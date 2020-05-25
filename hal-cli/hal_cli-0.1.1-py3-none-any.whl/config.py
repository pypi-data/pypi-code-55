import json
from pathlib import Path

from typer import Exit
from wasabi import Printer

msg = Printer()

default_config = {
    "username": "",
    "volume_id": "",
    "image_id": "ami-0b8526ee89f3ed824",
    "subnet_id": "",
    "security_group": "",
    "ssh_key_path": "",
    "ssh_password": "",
    "instance_profile_arn": "",
    "role_arn": "",
    "region": "eu-west-1",
}


def get_config_path(config_name):
    config_path = (Path.home() / ".hal" / config_name).with_suffix(".json")
    return config_path


def check_and_replace_missing_config(config, config_name):
    missing_value_keys = [
        key for key in default_config.keys() if key not in config
    ]

    if missing_value_keys:
        msg.warn("The supplied config is missing some values")
        msg.warn(
            "Reconfigure it by running "
            f'`hal --config-name "{config_name}" configure`'
        )
        msg.warn(f"Using values from default_config for {missing_value_keys}")
        for key in missing_value_keys:
            config[key] = default_config[key]

    return config


def get_config(config_name="config"):
    config_path = get_config_path(config_name)
    if config_name == "default":
        config = default_config
    else:
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
        except FileNotFoundError:
            msg.fail(f'Couldn\'t find a config file called "{config_name}".')
            msg.fail(
                f'Run `hal --config "{config_name}" configure` '
                "to configure this new profile.",
            )
            msg.fail("Aborted!")
            raise Exit()
        except json.decoder.JSONDecodeError:
            msg.fail(f'JSON in "{config_path}" is malformed')
            msg.fail("Aborted!")
            raise Exit()

    config = check_and_replace_missing_config(config, config_name)
    return config
