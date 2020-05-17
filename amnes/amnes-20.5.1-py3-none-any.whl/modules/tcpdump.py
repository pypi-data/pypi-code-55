"""This module contains the TcpDump Node Module for AMNES.

Classes:
    TcpDump: Node Module for running tcpdump on nodes.
"""

from ..core.node_task import NodeTaskFiles, NodeTaskParams
from ..exec.worker.node_module import NodeModuleError
from .shellcmd import ShellCommandBase
from .utils import check_forbidden_keys, check_string


class TcpDump(ShellCommandBase):
    """Node Module for running tcpdump on nodes.

    This module can be used to run tcpdump with a given configuration
    on the worker.

    Available configuration options:

    ```yaml
    params:
      interface: "any"
      expression: "icmp"
      custom: "-i eth0 -n port 8080"
    files: {}
    ```

    If `custom` is specified, all other configuration options of the Iperf module are
    ignored. You can also specify all configuration options for
    `ShellCommandBase`, but the following options are forbidden: `command`.
    """

    # pylint: disable=useless-super-delegation
    def __init__(
        self, params: NodeTaskParams, files: NodeTaskFiles, workdir: str
    ) -> None:
        """Tcpdump module constructor method.

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
            params.add_pair("command", f"tcpdump {custom}")
        else:
            interface = check_string(cfgdict.get("interface"), "interface")
            expression = check_string(cfgdict.get("expression"), "expression")
            if interface and expression:
                params.add_pair("command", f"tcpdump -i {interface} {expression}")
            else:
                raise NodeModuleError(
                    message="If custom parameters are not used, "
                    + "interface and expression must be set."
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
