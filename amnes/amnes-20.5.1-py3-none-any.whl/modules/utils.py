"""This module contains utility classes and functions for AMNES Modules."""

from typing import List, Optional

from ..core.node_task import NodeTaskConfig
from ..exec.worker.node_module import NodeModuleError


def check_string(instr: Optional[str], desc: str) -> str:
    """Checks if given string is a valid configuration value.

    Args:
        instr (Optional[str]): String which should be checked.
        desc (str): Description of configuration option for error messages.

    Returns:
        Given input string if it is a valid configuration value.
        Empty string, if `None` was given as input string.

    Raises:
        NodeModuleError: If given input string is invalid and not `None`.
    """
    if instr is None:
        return ""
    if (not isinstance(instr, str)) or (not instr) or (instr.isspace()):
        raise NodeModuleError(message=f"Invalid {desc} specified.") from ValueError(
            f"Given {desc} is not a non-empty, non-spaces string."
        )
    return instr


def check_forbidden_keys(config: NodeTaskConfig, keys: List[str]) -> None:
    """Check if node task config contains any of the forbidden keys.

    Args:
        config (NodeTaskConfig): Node task config instance which should be checked.
        keys (List[str]): List of forbidden keys for check.

    Raises:
        NodeModuleError: If any forbidden key was found in node task config instance.
    """
    for key in keys:
        if key in config.keys:
            raise NodeModuleError(
                message=f"Forbidden key was set for node module: '{key}'"
            )
