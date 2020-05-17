"""This module contains the Serializer for the FileModel.

Classes:
    FileSerializer: Concrete Serializer for the FileModel.
"""
import hashlib
from pathlib import Path
from typing import IO, List, Optional, Tuple

from peewee import IntegrityError

from ...core.amnes_object import AmnesObject
from ..models import ConcreteExperimentModel, FileModel
from .amnes_object import AmnesObjectSerializer

FileObject = Tuple[IO, Optional[str], Optional[str], Optional[str], Optional[List[str]]]


class FileSerializer:
    """Maps data into the filesystem and stores a reference in the database.

    The FileSerializer stores data to a file in the filesystem, stores its
    path and checksum. It maps data between `file_objects` and the filesystem.
    """

    @staticmethod
    def exists(file_id: int) -> bool:
        """Check if a given file with the given `file_id` exists in the database.

        Same method as FileSerializer.exists_by_id.

        Args:
            file_id (int): Unique `file_id` defining every file in the database.

        Returns:
            bool: Returns `True` if a file exists in the database, `False` if not.
        """
        return FileSerializer.exists_by_id(file_id)

    @staticmethod
    def exists_by_id(file_id: int) -> bool:
        """Check if a given file with the given `file_id` exists in the database.

        Args:
            file_id (int): Unique `file_id` defining every file in the database.

        Returns:
            bool: Returns `True` if a file exists in the database, `False` if not.
        """
        FileSerializer._check_file_id(file_id)

        query = FileModel.select().where(FileModel.id == file_id)
        if query.exists():
            return True
        return False

    @staticmethod
    def _check_file_id(file_id: int) -> None:
        """Raises errors if a `file_id` is not set properly.

        Args:
             file_id (int): Unique `file_id` defining every file in the database.

        Raises:
             TypeError: If `file_id` is not of type int.
             ValueError: If `object_id` is smaller than 1.
        """
        if not isinstance(file_id, int):
            raise TypeError("The parameter `object_id` must be of type int.")
        if file_id < 1:
            raise ValueError("The parameter `object_id` must be 1 or higher.")

    @staticmethod
    def insert(
        file_object: IO,
        root_path: Path,
        amnes_object: Optional[AmnesObject] = None,
        parent: Optional[ConcreteExperimentModel] = None,
        repetition: Optional[int] = None,
    ) -> int:
        """Inserts data of a file object into the filesystem.

        The FileSerializer stores data to a filesystem , whose path depends on
        the `root_path` argument. A File can be associated with a ConcreteExperiment
        and a repetition. Once a File is inserted, the parent reference and
        repetition cannot be changed.

        Args:
            file_object (IO): Accepts BinaryIO or TextIO file objects. The
                              recommended method is to pass a file object via
                              method call `open()`. Read permissions are necessary,
                              thus mode "r"/"rt" or "rb" of the `open()`-method
                              are required.
            root_path (Path): Absolute path to a directory, where all files
                              will be stored.
            amnes_object (Optional[AmnesObject]): Optional AmnesObject, to describe
                                                  inserted file.
            parent (Optional[ConcreteExperimentModel]): Optional parent reference.
                                                        A file can be associated with a
                                                        ConcreteExperiment. If a parent
                                                        is given, the `repetition`
                                                        argument has to be passed
                                                        as well.
            repetition (Optional[int]): Positive number, which refers to the exact
                                        repetition in the parent ConcreteExperiment.


        Returns:
            file_id (int): Returns a unique `file_id`.

        Examples:
            >>> from pathlib import Path
            >>> from amnes.data.serializer import FileSerializer
            >>> # StorageBackend needs to be initialized
            >>>file_object = open("file.txt", mode="r")
            >>>root_path = Path("/tmp")
            >>>file_id = FileSerializer.insert(file_object, root_path)
        """
        checksum_sha256, file_path, file_type = FileSerializer._save_file_to_filesystem(
            file_object, root_path
        )
        amnes_object_reference: Optional[int] = None
        if amnes_object:
            amnes_object_reference = AmnesObjectSerializer.insert(amnes_object)
        filemodel_instance, _ = FileModel.get_or_create(
            file_type=file_type,
            path=str(file_path),
            checksum_sha256=checksum_sha256,
            amnes_object=amnes_object_reference,
            concrete_experiment=parent,
            repetition=repetition,
        )

        return filemodel_instance.get_id()

    @staticmethod
    def delete_by_id(file_id: int, root_path: Path) -> None:
        """Deletes a file by a given `file_id`.

        The database entry and the persisted file in the filesystem will be deleted.

        Args:
            file_id: Unique `file_id` defining every file in the database.
            root_path (Path): Absolute path to a directory, where all files
                              will be stored.
        """
        FileSerializer._check_file_id(file_id)
        filemodel_instance: FileModel = FileModel.get_by_id(file_id)
        Path(root_path / filemodel_instance.path).unlink()
        filemodel_instance.delete_instance(recursive=True, delete_nullable=True)

    @staticmethod
    def update_by_id(
        file_object: IO,
        file_id: int,
        root_path: Path,
        amnes_object: Optional[AmnesObject] = None,
    ) -> None:
        """Updates the file, referenced by an existing `file_id`.

        Args:
            file_object (IO): Accepts BinaryIO or TextIO file objects. The
                               recommended method is to pass a file object via
                               method call `open()`. Read permissions are necessary,
                               thus mode "r"/"rt" or "rb" of the `open()`-method
                               are required.
            file_id (int): Unique `file_id` defining every file in the database.
            root_path (Path): Absolute path to a directory, where all files
                              will be stored.
            amnes_object (Optional[AmnesObject]): Optional, updated AmnesObject, to
                                                  describe inserted file.

        Raises:
            ValueError: If the `file_id` has no related entry in the database.
        """
        FileSerializer._check_file_id(file_id)
        if not FileSerializer.exists(file_id):
            raise ValueError("File reference does not exist.")
        checksum_sha256, file_path, file_type = FileSerializer._save_file_to_filesystem(
            file_object, root_path
        )

        filemodel_instance: FileModel = FileModel.get_by_id(file_id)
        Path(root_path / filemodel_instance.path).unlink()
        if amnes_object:
            AmnesObjectSerializer.update_by_id(
                amnes_object, filemodel_instance.amnes_object.id
            )
        query_update = FileModel.update(
            {
                "path": str(file_path),
                "checksum_sha256": checksum_sha256,
                "file_type": file_type,
            }
        ).where(FileModel.id == file_id)

        query_update.execute()

    @staticmethod
    def get_by_id(file_id: int, root_path: Path) -> FileObject:
        """Returns a `file_object` and can be used like the `open()`-method.

        It is recommended to used this method as a contextmanager, shown in the
        example.

        Args:
            file_id (int): Unique `file_id` defining every file in the database.
            root_path (Path): Absolute path to a directory, where all files
                              will be stored.

        Returns:
            file_object (IO): Returns an `open()` method, which mode depends on the
                               previous inserted `file_type`. The mode will be `rt`
                               for `text` and `rb` for all other.

        Raises:
            ValueError: If the `file_id` has no related entry in the database.
        """
        FileSerializer._check_file_id(file_id)
        if not FileSerializer.exists(file_id):
            raise ValueError("File reference does not exist.")
        filemodel_instance: FileModel = FileModel.get_by_id(file_id)
        amnes_object: Optional[AmnesObject] = None
        if filemodel_instance.amnes_object:
            amnes_object = AmnesObjectSerializer.get_by_id(
                filemodel_instance.amnes_object.id
            )
        slug = amnes_object.slug if amnes_object else None
        name = amnes_object.name if amnes_object else None
        description = amnes_object.description if amnes_object else None
        labels = amnes_object.labels if amnes_object else None

        file_path = root_path / Path(filemodel_instance.path)
        file_type = filemodel_instance.file_type
        mode = "rt" if file_type == "text" else "rb"
        FileSerializer._check_file(filemodel_instance, root_path)
        return (
            open(file_path, mode=mode),
            slug,
            name,
            description,
            labels,
        )

    @staticmethod
    def _save_file_to_filesystem(
        file_object: IO, root_path: Path
    ) -> Tuple[str, Path, str]:
        """Saves data from a `file_object` to a file.

        Args:
            file_object (IO): Accepts BinaryIO or TextIO file objects. The
                              recommended method is to pass a file object via
                              method call `open()`. Read permissions are necessary,
                              thus mode "r"/"rt" or "rb" of the `open()`-method
                              are required.
            root_path (Path): Absolute path to a directory, where all files
                              will be stored.

        Returns:
            checksum_sha256 (str), relative_file_path (str), file_type (str): Returns a
                3-tuple which consists of the SHA256 hash of the inserted data, the
                relative filepath it was written to and the file type (text/ binary).

        Raises:
            PermissionError: If mode of the `open()` method is set incorrectly.
        """
        if not str(file_object.mode).startswith("r"):
            raise PermissionError(
                "Wrong permissions of file_object. Currently "
                "are modes 'r'/ 'rt' and 'rb' supported."
            )
        data, file_type, checksum_sha256 = FileSerializer._retrieve_data(file_object)
        file_path: Path = root_path / checksum_sha256
        with file_path.open(mode="w"):
            file_path.write_bytes(data)
        relative_file_path: Path = Path(checksum_sha256)
        return checksum_sha256, relative_file_path, file_type

    @staticmethod
    def _retrieve_data(file_object: IO) -> Tuple[bytes, str, str]:
        """Receives data from a `file_object` and loads it into memory and hashes it.

        Args:
            file_object (IO): A file object, generated by the `open()`-method.

        Returns:
            data (bytes), file_type (str), checksum_sha256 (str): A 3-tuple where the
            data is represented in bytes, the file_type is either `text` or `binary`
            and the checksum_sha256 is the SHA256 Hash of the output data.
        """
        with file_object:
            if file_object.mode in ("rt", "r"):
                data: bytes = file_object.read().encode()
                file_type = "text"
                checksum_sha256: str = hashlib.sha256(data).hexdigest()
            else:
                data = file_object.read()
                file_type = "binary"
                checksum_sha256 = hashlib.sha256(data).hexdigest()
        return data, file_type, checksum_sha256

    @staticmethod
    def _check_file(filemodel_instance: FileModel, root_path: Path,) -> None:
        """Raises errors if `filemodel_instance` is not set properly.

        Args:
            filemodel_instance (FileModel): A database instance of the FileModel.
            root_path (Path): Absolute path to a directory, where all files
                              will be stored.

        Raises:
            FileNotFoundError: If the path in `filemodel_instance` does not exist
                               in the filesystem.
            IntegrityError: If the related file, has a different checksum_sha256
                            compared to its database entry.
        """
        if not Path(root_path / filemodel_instance.path).exists():
            raise FileNotFoundError("File does not exist in filesystem.")
        checksum_sha256 = FileSerializer._generate_checksum_sha256(
            str(root_path / filemodel_instance.path)
        )
        if checksum_sha256 != filemodel_instance.checksum_sha256:
            raise IntegrityError(
                "Checksums do not match. File was modified in the filesystem or "
                "checksum was changed in the database."
            )

    @staticmethod
    def _generate_checksum_sha256(file_path: str) -> str:
        """Generates a SHA256 checksum of a file.

        Args:
            file_path (str): The path to the file.

        Returns:
            checksum_sha256 (str): The SHA256 checksum of the file at the given path.
        """
        with open(file_path, "rb") as file_object:
            data: bytes = file_object.read()
            checksum_sha256 = hashlib.sha256(data).hexdigest()
        return checksum_sha256
