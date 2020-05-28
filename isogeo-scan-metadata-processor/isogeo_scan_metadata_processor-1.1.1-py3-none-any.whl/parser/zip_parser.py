#! python3  # noqa: E265

"""
    Manipulate zipped files.

    See:

    - https://docs.python.org/fr/3/library/zipfile.html

"""

# #############################################################################
# ########## Libraries #############
# ##################################

# standard library
import logging
from io import BufferedIOBase, BytesIO
from os import R_OK, access
from pathlib import Path
from typing import List, Union
from zipfile import BadZipFile, ZipFile, is_zipfile

# #############################################################################
# ########## Globals ###############
# ##################################

logger = logging.getLogger(__name__)


# ##############################################################################
# ########## Classes ###############
# ##################################
class Unzipper:
    """Check and extract files from a zip archive.

    :param input_zip: path to the zip file to unzip.
    """

    def __init__(self, input_zip: Union[str, Path]):
        """Instanciating Unzipper."""
        if isinstance(input_zip, (str, Path)):
            self.source_type = "file"
            self.zippo = self.check_zip(input_zip)
        elif isinstance(input_zip, BufferedIOBase):
            self.source_type = "buffer"
            self.zippo = self.check_zip(input_zip)
        else:
            raise TypeError(
                "Instance of input_zip must be one of: str, Path, BufferIOBase. Not: {}".format(
                    type(input_zip)
                )
            )

    @classmethod
    def check_zip(cls, input_zip: Union[str, Path]) -> Path:
        """Perform some checks on passed zip file and load it as Path object.

        :param input_zip: path to the zip file to unzip.

        :returns: sanitized zip path
        :rtype: Path
        """
        # if path as string load it in Path object
        if isinstance(input_zip, str):
            try:
                input_zip = Path(input_zip)
            except Exception as exc:
                raise TypeError("Converting zip path failed: {}".format(exc))

        if isinstance(input_zip, Path):
            # check if file exists
            if not input_zip.exists():
                raise FileExistsError(
                    "Zipfile to check doesn't exist: {}".format(input_zip.resolve())
                )

            # check if it's a file
            if not input_zip.is_file():
                raise IOError("Zipfile is not a file: {}".format(input_zip.resolve()))

            # check if file is readable
            if not access(input_zip, R_OK):
                raise IOError("Zip file isn't readable: {}".format(input_zip))

        elif isinstance(input_zip, BufferedIOBase):
            input_zip = BytesIO(input_zip.read())
        else:
            raise TypeError("Input zip type of instance is not correct.")

        # check if file is a zip
        if not is_zipfile(input_zip):
            raise BadZipFile("File isn't a ZIP: {}".format(input_zip))

        # check integrity
        try:
            with ZipFile(file=input_zip) as in_zip:
                in_zip.testzip()
        except BadZipFile as exc:
            raise exc

        # return sanitized path
        return input_zip

    def get_files_list(self) -> list:
        """Return the list of zipped files (just a wrapper around namelist() standard method).

        :return: list of zipped files
        :rtype: list
        """
        return ZipFile(self.zippo).namelist()

    def unzip(
        self,
        to_folder: Union[str, Path] = None,
        all_in: bool = True,
        only_extensions: tuple = None,
    ) -> list:
        """Extract files from zip. Can extract every files or filter on some extensions.

        :param Union[str, Path] to_folder: path to the output folder. \
        If it doesn't exist, it'll be created. Defaults to: None - optional
        :param bool all_in: option to extract all files. Defaults to: True - optional
        :param tuple only_extensions:  option to filter on certain extensions. \
        Defaults to: None - optional

        :return: list of extracted files
        :rtype: list

        :example:

        .. code-block:: python

            for i in fixtures_dir.glob("**/*.zip"):
                unzipper = Unzipper(i)
                print(unzipper.zipfile_path)

                # extract all files
                unzipper.unzip(fixtures_dir / "unzipper/all_in", all_in=1)

                # extract only JSON
                unzipper.unzip(
                    to_folder=Path(fixtures_dir / "unzipper/filtered"),
                    all_in=0,
                    only_extensions=(".json",),
                )

        """
        if self.source_type == "file":
            all_in = self._check_all_in(all_in, only_extensions)
            return self._unzip_to_disq(all_in, only_extensions, to_folder)
        elif self.source_type == "buffer":
            return self._unzip_to_memory(only_extensions=only_extensions)

    def _check_all_in(self, all_in: bool, only_extensions: tuple) -> bool:
        """Minimal checker of unzip parameters.

        :return: all_in value
        :rtype: bool
        """
        # check args conflicts
        if all_in and only_extensions is not None:
            logger.warning(
                "'all_in' and 'only_extension' are exclusive: "
                "if the first is True, then the second must be None. "
                "The option only_extension will be kept."
            )
            all_in = False
        elif not all_in and only_extensions is None:
            logger.warning(
                "'all_in' and 'only_extension' are exclusive: "
                "if the first is False, then the second must be a tuple. "
                "The option 'all_in' will be set to True."
            )
            all_in = True

        return all_in

    def _unzip_to_disq(
        self, all_in: bool, only_extensions: tuple, to_folder: Path
    ) -> list:
        """Sub-method of 'unzip', specilized for unzipping to disq.
        Same parameters of 'unzip'.
        """
        # ensure the the output folder is created
        try:
            to_folder.mkdir(exist_ok=True, parents=True)
        except PermissionError:
            raise PermissionError(
                "Output folder is not writable: {}".format(to_folder.resolve())
            )

        if not to_folder.is_dir():
            logger.warning(
                "Passed output path is not a folder: {}. Parent folder will be used instead.".format(
                    to_folder.resolve()
                )
            )
            to_folder = to_folder.parent

        # option to extract everything
        if all_in and only_extensions is None:
            with ZipFile(file=self.zippo) as in_zip:
                in_zip.extractall(to_folder)
            logger.info(
                "{} files extracted to {} from {}".format(
                    len(in_zip.namelist()), to_folder.resolve(), self.zippo.resolve(),
                )
            )
            # return with extracted files list
            return in_zip.namelist()

        # option to extract only certain files
        if not all_in and isinstance(only_extensions, tuple):
            li_extracted_files = []
            with ZipFile(file=self.zippo) as in_zip:
                for file_to_extract in in_zip.namelist():
                    if file_to_extract.endswith(only_extensions):
                        in_zip.extract(file_to_extract, to_folder)
                        li_extracted_files.append(file_to_extract)

            # return with extracted files list
            return li_extracted_files

    def _unzip_to_memory(self, only_extensions: tuple) -> List[bytes]:
        """Sub-method of unzip which unzip all files matching the extensions into a list of bytes.

        :return: list of JSONs as bytes
        :rtype: List[bytes]
        """
        li_out_files = []
        self.zippo.seek(0)
        with ZipFile(file=self.zippo) as in_zip:
            for file_in_zip in self.get_files_list():
                if file_in_zip.endswith(only_extensions):
                    li_out_files.append(in_zip.read(file_in_zip))

        return li_out_files


# #############################################################################
# ##### Main #######################
# ##################################
if __name__ == "__main__":
    pass
