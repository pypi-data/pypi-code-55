"""This module contains all necessary definitions for an abstract NodeModule class.

Classes:
    NodeModuleError: Error which is raised when a node module function call fails.
    NodeModuleMethodNotBoundError: Error which is raised if a method is called but
                                   no method is bound to it.
    NodeModule: Base NodeModule class from which all further node modules must inherit.
"""

from typing import BinaryIO, Optional

from ...core.node_task import NodeTaskFiles, NodeTaskParams


class NodeModuleError(Exception):
    """Error which is raised when a node module function call fails.

    This error can be customized by setting specific parameters on creation.
    If `plain` is set to True on creation, the printed error string will be empty.
    Otherwise, the error string will be constructed with `message` if set.

    >>> NodeModuleError()
    "NodeModuleError: Error occured in node module function call."

    >>> NodeModuleError(plain=True)
    "NodeModuleError"

    >>> NodeModuleError(message="Custom message.")
    "NodeModuleError: Node module function call failed: Custom message."

    >>> NodeModuleError(message="Custom message.", plain=True)
    "NodeModuleError"

    Attributes:
        message (str): More precise error message which describes the
                       node module error.
        plain (bool): If plain error (empty error string) should be created.
    """

    def __init__(self, *, message: str = "", plain: bool = False) -> None:
        """Node module class constructor method.

        Args:
            message (str): More precise error message which describes the
                           node module error.
            plain (bool): If plain error (empty error string) should be created.
        """
        super().__init__()
        self.__plain = False
        self.__message = message if not plain else ""

    @property
    def message(self) -> str:
        """str: More precise error message which describes the node module error.

        Returns:
            message (str): More precise error message which describes the
                           node module error.
        """
        return self.__message

    @property
    def plain(self) -> bool:
        """bool: True if plain error (empty error string) should be created.

        Returns:
            bool: True if plain error (empty error string) should be created.
        """
        return self.__plain

    def __str__(self) -> str:
        """Overwrite magic string method of the super class.

        Overrides the string method of `Exception` by additionally
        returning the key that could not be parsed as a message.

        Returns:
            str: Custom error message constructed with set attributes.
        """
        if self.plain:
            return ""
        if self.message and (not self.message.isspace()):
            return "Node module function call failed: {}".format(self.message)
        return "Error occured in node module function call."


class NodeModuleMethodNotBoundError(NotImplementedError):
    """Error which is raised if a method is called but no method is bound to it."""


class NodeModule:
    """Base NodeModule class from which all further node modules must inherit.

    Within this class, three basic methods are defined which must be overwritten
    by every other module. The worker assumes that each of these module methods
    has been implemented correctly.

    The methods must be implemented as follows:

    execute: Within the execute method, all logical steps for executing the specific
             task of this module are defined. The external execution of this method
             must be fully sufficient to accomplish the intended task.

    collect: If the worker calls this method, all data required for evaluation must
             be stored persistently via the DataManager.

    cleanup: Calling the cleanup method must ensure that everything in the local
             environment is restored to the initial state and that no persistent data
             remains in the local storage directory.

    Attributes:
        params (NodeTaskParams): The parameters required for the execution of the
                                 NodeModule.
        files (NodeTaskFiles): The files required for the execution of the module.
        workdir (str): Working directory for the node module instance.
        error (Optional[NodeModuleError]): NodeModuleError occured in previous function
                                           call, may be `None`.
        corrupt (bool): True, if an uncatched error occured in any previous function
                        call, else False.
    """

    def __init__(
        self, params: NodeTaskParams, files: NodeTaskFiles, workdir: str
    ) -> None:
        """Base node module constructor method.

        Args:
            params (NodeTaskParams): The parameters required for the execution of the
                                     NodeModule.
            files (NodeTaskFiles): The files required for the execution of the module.
            workdir (str): Working directory for the node module instance.
        """
        self.__params = params
        self.__files = files
        self.__workdir = workdir
        self.error = None
        self.corrupt = False

    @property
    def params(self) -> NodeTaskParams:
        """NodeTaskParams: The parameters of this NodeModule instance.

        Returns:
            params (NodeTaskParams): The parameters of this NodeModule instance.
        """
        return self.__params

    @property
    def files(self) -> NodeTaskFiles:
        """NodeTaskParams: The parameters of this NodeModule instance.

        Returns:
            params (NodeTaskParams): The parameters of this NodeModule instance.
        """
        return self.__files

    @property
    def workdir(self) -> str:
        """str: Working directory for the node module instance.

        Returns:
            str: Working directory for the node module instance.
        """
        return self.__workdir

    @property
    def error(self) -> Optional[NodeModuleError]:
        """Optional[NodeModuleError]: Error which occured in a previous function call.

        Returns:
            Optional[NodeModuleError]: Error which occured in a previous function call.
        """
        return self.__error

    @error.setter
    def error(self, error: NodeModuleError) -> None:
        """Sets error which occured in a previous function call.

        Args:
            error (NodeModuleError): Error which occured in a previous function call.
        """
        self.__error = error

    @property
    def corrupt(self) -> bool:
        """bool: True, if an uncatched error occured in any previous function call.

        Returns:
            bool: True, if an uncatched error occured in any previous function
                  call, else False.
        """
        return self.__corrupt

    @corrupt.setter
    def corrupt(self, corrupt: bool) -> None:
        """Mark if an uncatched error occured in any previous function call.

        Args:
            corrupt (bool): If an uncatched error occured in any previous function call.
        """
        self.__corrupt = corrupt

    def execute(self) -> None:
        """Method for executing the specific task of this module.

        The external execution of this method must be fully sufficient to accomplish
        the intended task.
        """

    def collect(self) -> None:
        """Method for collecting and storing all data required for evaluation.

        If the worker calls this method, all data required for evaluation must be
        stored persistently via the DataManager.
        """

    def cleanup(self) -> None:
        """Method for restoring the environment to the initial state.

        Calling the cleanup method must ensure that everything in the local environment
        is restored to the initial state and that no persistent data remains in the
        local storage directory.
        """

    def store_io(  # pylint: disable=no-self-use,missing-raises-doc
        self, stream: BinaryIO
    ) -> None:
        """Method for storing content of an IO stream into a persistent object.

        Args:
            stream (BinaryIO): IO stream which should be stored persistently.
        """
        raise NodeModuleMethodNotBoundError(
            "'Store IO' capability not available as no method is bound."
        )
