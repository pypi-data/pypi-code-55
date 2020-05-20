"""HAL manages your machine learning research environment in AWS"""

from .hal9000 import Hal9000

__version__ = "0.1.0"

default_config = {
    "username": "dave",
    "volume_id": "",
    "image_id": "ami-0b8526ee89f3ed824",
    "subnet_id": "",
    "security_group": "",
    "key_path": "",
    "password": "",
    "instance_profile_arn": "",
    "role_arn": "",
    "region": "eu-west-1",
}
