"""This module contains the iPerf Node Module for AMNES.

Classes:
    Iperf: Node Module for using iPerf on nodes.
"""

from ..core.node_task import NodeTaskFiles, NodeTaskParams
from ..exec.worker.node_module import NodeModuleError
from .shellcmd import ShellCommandBase
from .utils import check_forbidden_keys, check_string


class Iperf(ShellCommandBase):
    """Node Module for using iPerf on nodes.

    This module can be used to execute the iperf command with a given configuration
    on the worker.

    Available configuration options:

    ```yaml
    params:
      version: "3"
      custom: "-i 10 -c [[1]]"
    files: {}
    ```

    If `custom` is specified, all other configuration options of the Iperf module are
    ignored (excluding `version`). The `version` parameter must always be set to "2" or
    "3" specifiying the iperf version which should be used.
    You can also specify all configuration options for `ShellCommandBase`,
    but the following options are forbidden: `command`.
    """

    # pylint: disable=useless-super-delegation
    def __init__(
        self, params: NodeTaskParams, files: NodeTaskFiles, workdir: str
    ) -> None:
        """Iperf module constructor method.

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
        version = check_string(cfgdict.get("version"), "iperf version")
        if version not in ["2", "3"]:
            raise NodeModuleError(
                message="Iperf module requires the version parameter "
                + "to be set to '2' or '3'."
            )
        custom = check_string(cfgdict.get("custom"), "custom parameters")
        if custom:
            iperfcmd = "iperf3" if version == "3" else "iperf"
            params.add_pair("command", f"{iperfcmd} {custom}")
        else:
            raise NodeModuleError(
                message="Iperf module requires configuration via custom parameter."
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
