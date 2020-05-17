"""This module contains the Ping Node Module for AMNES.

Classes:
    Ping: Node Module for pinging hosts.
"""

from ..core.node_task import NodeTaskFiles, NodeTaskParams
from ..exec.worker.node_module import NodeModuleError
from .shellcmd import ShellCommandBase
from .utils import check_forbidden_keys, check_string


class Ping(ShellCommandBase):
    """Node Module for pinging hosts.

    This module can be used to execute the ping command with a given configuration
    on the worker.

    Available configuration options:

    ```yaml
    params:
      destination: "[[1]]"
      count: "10"
      verbose: "True"
      custom: "-c 10 -a -v [[1]]"
    files: {}
    ```

    If `custom` is specified, all other configuration options of the Ping module are
    ignored. You can also specify all configuration options for
    `ShellCommandBase`, but the following options are forbidden: `command`.
    """

    # pylint: disable=useless-super-delegation
    def __init__(
        self, params: NodeTaskParams, files: NodeTaskFiles, workdir: str
    ) -> None:
        """Ping module constructor method.

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
            params.add_pair("command", f"ping {custom}")
        else:
            destination = check_string(cfgdict.get("destination"), "destination")
            count = check_string(cfgdict.get("count"), "count")
            verbose = check_string(cfgdict.get("verbose"), "verbose flag")
            if destination and count:
                if verbose:
                    params.add_pair("command", f"ping -v -c {count} {destination}")
                else:
                    params.add_pair("command", f"ping -c {count} {destination}")
            else:
                raise NodeModuleError(
                    message="If custom parameters are not used, "
                    + "destination and count must be set."
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
