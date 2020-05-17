"""This module contains the NetEm Node Module for AMNES.

Classes:
    NetEm: Node Module for configuring and using NetEm on nodes.
"""

from ..core.node_task import NodeTaskFiles, NodeTaskParams
from ..exec.worker.node_module import NodeModuleError
from .shellcmd import ShellCommandBase
from .utils import check_forbidden_keys, check_string


class NetEm(ShellCommandBase):
    """Node Module for configuring and using NetEm on nodes.

    This module can be used to configure and use NetEm with on the worker.

    Available configuration options:

    ```yaml
    params:
      custom: "limit 5"
    files: {}
    ```

    If `custom` is specified, all other configuration options of the NetEm module are
    ignored. You can also specify all configuration options for
    `ShellCommandBase`, but the following options are forbidden: `command`.
    """

    # pylint: disable=useless-super-delegation
    def __init__(
        self, params: NodeTaskParams, files: NodeTaskFiles, workdir: str
    ) -> None:
        """Netem module constructor method.

        Args:
            params (NodeTaskParams): The parameters required for the execution of the
                                     NodeModule.
            files (NodeTaskFiles): The files required for the execution of the module.
            workdir (str): Working directory for the node module instance.

        Raises:
            NodeModuleError: If configuration for module is invalid.
        """
        check_forbidden_keys(params, ["command"])
        cfgdict = dict(params.pairs)
        custom = check_string(cfgdict.get("custom"), "custom parameters")
        if custom:
            params.add_pair("command", f"tc {custom}")
        else:
            raise NodeModuleError(
                message="NetEm module requires configuration via custom parameter."
            )
        ShellCommandBase.__init__(self, params, files, workdir)

    def execute(self) -> None:
        """Empty execute implementation."""
        super().execute()

    def collect(self) -> None:
        """Empty collect implementation."""
        super().collect()

    def cleanup(self) -> None:
        """Empty cleanup implementation."""
        super().cleanup()
