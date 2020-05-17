"""This module contains Feature Node Modules to extend usable Node Modules.

Classes:
    CustomFilesFeature: Feature Node Module for handling cleanup of custom files.
"""

from contextlib import suppress
from pathlib import Path
from typing import Sequence, Set

from ..core.node_task import NodeTaskFiles, NodeTaskParams
from ..exec.worker.node_module import NodeModule


class CustomFilesFeature(NodeModule):
    """Feature Node Module for handling cleanup of custom files.

    Attributes:
        custom_files (Set[str]): Set of all added custom files which will be
                                 removed on cleanup.
    """

    # pylint: disable=useless-super-delegation
    def __init__(
        self, params: NodeTaskParams, files: NodeTaskFiles, workdir: str
    ) -> None:
        """Partial constructor method for custom files feature.

        Args:
            params (NodeTaskParams): The parameters required for the execution of the
                                     NodeModule.
            files (NodeTaskFiles): The files required for the execution of the module.
            workdir (str): Working directory for the node module instance.
        """
        super().__init__(params, files, workdir)
        self.__custom_files: Set[str] = set()

    @property
    def custom_files(self) -> Set[str]:
        """Set[str]: Set of all added custom files which will be removed on cleanup.

        Returns:
            Set[str]: Set of all added custom files which will be removed on cleanup.
        """
        return self.__custom_files

    def add_custom_file(self, file: str) -> None:
        """Add file path to set of custom files.

        Args:
            file (str): File path which should be added to the list of custom files.

        Raises:
            ValueError: If file path is empty or only contains spaces.
        """
        if (not file) or (file.isspace()):
            raise ValueError("File path is empty or only contains spaces.")
        if file not in self.custom_files:
            self.__custom_files.add(file)

    def add_custom_files(self, files: Sequence[str]) -> None:
        """Add sequence of file paths to set of custom files.

        Args:
            files (Sequence[str]): Sequence of file paths which should be added to the
                                   list of custom files.

        Raises:
            ValueError: If any file path is empty or only contains spaces.
        """
        for file in files:
            self.add_custom_file(file)

    def remove_custom_file(self, file: str) -> None:
        """Remove file path from set of custom files.

        Args:
            file (str): File path which should be removed from the list of custom files.

        Raises:
            ValueError: If file path is empty or only contains spaces.
        """
        if (not file) or (file.isspace()):
            raise ValueError("File path is empty or only contains spaces.")
        if file in self.custom_files:
            self.__custom_files.remove(file)

    def remove_custom_files(self, files: Sequence[str]) -> None:
        """Remove sequence of file paths from set of custom files.

        Args:
            files (Sequence[str]): Sequence of file paths which should be removed
                                   from the list of custom files.

        Raises:
            ValueError: If any file path is empty or only contains spaces.
        """
        for file in files:
            self.remove_custom_file(file)

    def execute(self) -> None:
        """Empty execute implementation."""
        super().execute()

    def collect(self) -> None:
        """Empty collect implementation."""
        super().collect()

    def cleanup(self) -> None:
        """Partial cleanup for removing all files from disk added to custom files."""
        super().cleanup()
        for file in self.custom_files:
            with suppress(FileNotFoundError):
                Path(file).unlink()
