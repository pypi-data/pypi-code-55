"""This modules contains classes and functions for managing experiment results.

Classes:
    ExperimentReference: Reference of a specific concrete experiment repetition.
    FileTransfer: Class representing a registered file transfer.
    ResultManager: Manager class for recieving and storing experiment results.
    RemoteResultManager: Remote manager for result manager instance.
"""

import tempfile
from logging import Logger
from select import select
from socket import socket
from threading import Lock, Thread, current_thread
from typing import TYPE_CHECKING, Dict, List, NamedTuple, Optional, Tuple
from uuid import uuid4

import Pyro5.api as Pyro5
import Pyro5.socketutil as P5socket

from ...data.manager.storage_backend import ConcreteExperimentReference
from ..app import AmnesRemoteException
from ..logging import InstanceLogging

if TYPE_CHECKING:
    from .app import Controller  # pylint: disable=cyclic-import


class ExperimentReference(NamedTuple):
    """Reference of a specific concrete experiment repetition."""

    concrete_experiment_reference: ConcreteExperimentReference
    repetition: int


class FileTransfer:
    """Class representing a registered file transfer.

    Attributes:
        token (str): Unique filetransfer token for identification.
        experiment_reference (ExperimentReference): Concrete experiment repetition the
                                                    file belongs to.
    """

    def __init__(self, experiment_reference: ExperimentReference) -> None:
        """File transfer constructor method.

        Args:
            experiment_reference (ExperimentReference): Concrete experiment repetition
                                                        the file belongs to.
        """
        self.__token: str = str(uuid4())
        self.__experiment_reference: ExperimentReference = experiment_reference

    @property
    def token(self) -> str:
        """str: Unique filetransfer token for identification.

        Returns:
            str: Unique filetransfer token for identification.
        """
        return self.__token

    @property
    def experiment_reference(self) -> ExperimentReference:
        """ExperimentReference: Concrete experiment repetition the file belongs to.

        Returns:
            ExperimentReference: Concrete experiment repetition the file belongs to.
        """
        return self.__experiment_reference


class ResultManager(InstanceLogging):
    """Manager class for recieving and storing experiment results."""

    LOGID = "resultmanager"

    def __init__(self, logger: Logger, controller: "Controller") -> None:
        """Result Manager constructor method.

        Args:
            logger (Logger): Logger for object instance.
            controller (Controller): Controller which initialized the result manager.
        """
        InstanceLogging.__init__(self, logger)
        self.__transfers: Dict[str, FileTransfer] = {}
        self.__active_threads: List[Thread] = []
        self.__controller: "Controller" = controller
        self.__listen_socket: socket = P5socket.create_socket(
            bind=(
                self.__controller.configuration.controller.filetransfer_address,
                self.__controller.configuration.controller.filetransfer_port,
            )
        )
        self.__active: bool = False
        self.__run_lock = Lock()

    def execute(self) -> None:
        """Execute Result Manager loop logic."""
        with self.__run_lock:
            self.__active = True
            while self.__active:
                readsockets: List[socket] = []
                readsockets.append(self.__listen_socket)
                readsockets, _, _ = select(readsockets, [], [], 3)
                for sock in readsockets:
                    if sock == self.__listen_socket:
                        self.__handle_connection()
            self.logger.info("Result Manager is shutting down ...")
            for thread in self.__active_threads:
                thread.join()
            self.logger.info("Result Manager stopped gracefully.")

    def shutdown(self) -> None:
        """Set shutdown flag for loop logic."""
        self.__active = False
        self.__run_lock.acquire()

    def request_filetransfer(self) -> Tuple[str, Tuple[str, int]]:
        """Prepare and configure a filetransfer socket for client.

        Returns:
            str: File Transfer Token.
            Tuple[str, int]: Address and port of result manager listening socket.

        Raises:
            ValueError: If no experiment is currently active.
        """
        if not self.__controller.current_experiment:
            raise ValueError("No experiment currently active.")
        transfer = FileTransfer(self.__controller.current_experiment)
        self.__transfers[transfer.token] = transfer
        return (transfer.token, self.__listen_socket.getsockname()[:2])

    def __get_filetransfer_by_token(self, token: str) -> Optional[FileTransfer]:
        """Get file transfer instance by token.

        Args:
            token (str): Token of file transfer instance which should be returned.

        Returns:
            File transfer instance by token or None if token is not valid.
        """
        return self.__transfers.get(token)

    def __handle_connection(self) -> None:
        """Handle new connection on listenting socket."""
        tsocket, _ = self.__listen_socket.accept()
        thread = Thread(
            target=self.__handle_transfer,
            args=(tsocket,),
            name=f"FileTransfer-Unknown-{uuid4()}",
        )
        thread.daemon = False
        thread.start()
        self.__active_threads.append(thread)

    def __handle_transfer(self, tsocket: socket) -> None:
        """Handle file transfer connection.

        Args:
            tsocket (socket): Socket of client which opened the file transfer
                              connection.

        Raises:
            ValueError: If storage backend is not available.
        """
        token = P5socket.receive_data(tsocket, 36).decode()
        transfer = self.__get_filetransfer_by_token(token)
        if transfer is None:
            self.logger.warning(
                f"File Transfer '{token}' was requested but is unknown."
            )
            tsocket.close()
            self.__active_threads.remove(current_thread())
            return
        current_thread().name = f"FileTransfer-{transfer.token}"
        self.logger.info(f"File Transfer '{token}' started ...")
        reference = transfer.experiment_reference.concrete_experiment_reference
        repetition = transfer.experiment_reference.repetition
        try:
            with tempfile.TemporaryFile() as tmpf:
                chunk = b"buffer"
                while chunk:
                    chunk = tsocket.recv(4096)
                    tmpf.write(chunk)
                tsocket.close()
                if self.__controller.storage:
                    tmpf.seek(0, 0)
                    self.__controller.storage.import_file(
                        tmpf, reference=reference, repetition=repetition,
                    )
                else:
                    self.logger.error("No Storage Backend available!")
                    raise ValueError("No Storage Backend available!")
                self.logger.info(f"File Transfer '{token}' finished.")
        except Exception as exc:  # pylint: disable=broad-except
            self.logger.error(f"File Transfer '{token}' failed: {exc}")
        finally:
            del self.__transfers[token]
        self.__active_threads.remove(current_thread())


class RemoteResultManager:
    """Remote manager for result manager instance."""

    PYROID = "rmtresultmngr"
    PINGMSG = "pong"

    def __init__(self, resultmngr: ResultManager) -> None:
        """Remote result manager constructor method.

        Args:
            resultmngr (ResultManager): Linked result manager which should be managed.
        """
        self.__resultmngr: ResultManager = resultmngr

    @staticmethod
    @Pyro5.expose  # type: ignore
    def ping() -> str:
        """Returns remote result manager ping message.

        Returns:
            str: Remote result manager ping message.
        """
        return RemoteResultManager.PINGMSG

    @Pyro5.expose  # type: ignore
    def request_filetransfer(self) -> Tuple[str, Tuple[str, int]]:
        """Prepare and configure a filetransfer socket for client.

        Returns:
            str: File Transfer Token.
            Tuple[str, int]: Address and port of result manager listening socket.
        """
        with AmnesRemoteException.exception_handling():
            return self.__resultmngr.request_filetransfer()
