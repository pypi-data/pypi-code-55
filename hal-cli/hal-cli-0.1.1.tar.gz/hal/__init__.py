"""HAL manages your machine learning research environment in AWS"""

import json
from pathlib import Path

from .config import default_config, get_config, get_config_path  # noqa: F401
from .hal9000 import Hal9000  # noqa: F401

__version__ = "0.1.1"

hal_dir = Path.home() / ".hal"
if not hal_dir.exists():
    hal_dir.mkdir()
    with open(get_config_path("config"), "w") as f:
        json.dump(default_config, f)
