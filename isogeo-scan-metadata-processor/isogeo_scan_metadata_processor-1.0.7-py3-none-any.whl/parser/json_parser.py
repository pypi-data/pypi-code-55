#! python3  # noqa: E265

"""
    Read JSON files produced by Isogeo Scan.

    See:

    - https://docs.python.org/fr/3/library/JSON file.html

"""


# #############################################################################
# ########## Libraries #############
# ##################################
# standard library
import logging
import json
from json.decoder import JSONDecodeError
from io import BufferedIOBase
from os import access, R_OK
from pathlib import Path
from typing import Union

# 3rd party
from isogeo_pysdk import Metadata

# submodule
from scan_metadata_processor.parser import Listing, Lookup, Sign

# #############################################################################
# ########## Globals ###############
# ##################################

logger = logging.getLogger(__name__)


# ##############################################################################
# ########## Classes ###############
# ##################################
class MetadataJsonReader:
    """Read a JSON file produced by FME scripts of Isogeo Scan and return a Metadata.

    :param Union[str, Path, BufferedIOBase, bytes] in_json: path to the json file to read.
    """

    # global options to pass to open method
    # see: https://docs.python.org/fr/3/library/functions.html#open
    ENCODING_DEFAULT = "UTF-8"  # used as default encoding
    ENCODING_FALLBACK = "latin1"  # used as fallback encoding
    ENCODING_ERRORS_MODE = "replace"  # used to handle encoding errors

    def __init__(self, in_json: Union[str, Path, BufferedIOBase, bytes]):
        """Instanciating Isogeo Metadata JSON Reader."""
        # check and get JSON path
        if isinstance(in_json, (str, Path)):
            self.input_json = self.check_json_file(in_json)
            # extract data from input file
            with self.input_json.open(
                mode="r",
                encoding=self.ENCODING_DEFAULT,
                errors=self.ENCODING_ERRORS_MODE,
            ) as bytes_data:
                self.json_data = json.load(bytes_data)
        elif isinstance(in_json, BufferedIOBase):
            self.input_json = self.check_json_buffer(in_json)
            # extract data from input file
            self.json_data = json.load(bytes_data)
        elif isinstance(in_json, bytes):
            # extract data from input bytes
            self.json_data = json.loads(in_json)
        else:
            raise TypeError(
                "JSON type must be one of: str, Path, BufferedIOBase, bytes"
            )

        # guess source stage
        self.source

    # CHECKS
    def check_json_file(self, json_path: Union[str, Path]) -> Path:
        """Perform some checks on passed json file and load it as Path object.

        :param json_path: path to the json file to check

        :returns: sanitized json path
        :rtype: Path
        """
        # if path as string load it in Path object
        if isinstance(json_path, str):
            try:
                json_path = Path(json_path)
            except Exception as exc:
                raise TypeError("Converting json path failed: {}".format(exc))

        # check if file exists
        if not json_path.exists():
            raise FileExistsError(
                "JSON file to check doesn't exist: {}".format(json_path.resolve())
            )

        # check if it's a file
        if not json_path.is_file():
            raise IOError("JSON file is not a file: {}".format(json_path.resolve()))

        # check if file is readable
        if not access(json_path, R_OK):
            raise IOError("json file isn't readable: {}".format(json_path))

        # check integrity
        with json_path.open(
            mode="r", encoding=self.ENCODING_DEFAULT, errors=self.ENCODING_ERRORS_MODE
        ) as in_json_file:
            try:
                json.load(in_json_file)
            except JSONDecodeError as err:
                logger.error("JSON file is invalid: {}".format(json_path.resolve()))
                raise err
            except UnicodeDecodeError as err:
                logger.error(
                    "Failed to decode JSON file with encoding '{}': {}. "
                    "Trying to use the fallback encoding...".format(
                        self.ENCODING_DEFAULT, json_path.resolve()
                    )
                )
                # switch to fallback encoding
                self.ENCODING_DEFAULT = self.ENCODING_FALLBACK

                if self.ENCODING_DEFAULT != self.ENCODING_FALLBACK:
                    return self.check_json_file(json_path=json_path)

                raise err

        # return sanitized path
        return json_path

    def check_json_buffer(self, json_buffer: BufferedIOBase):
        """Perform some checks on passed json file and load it as Path object.

        :param json_buffer: path to the json file to check

        :returns: sanitized json path
        :rtype: Path
        """
        # check integrity
        try:
            json.load(json_buffer)
        except json.JSONDecodeError as exc:
            logger.error("Invalid JSON {}. Trace: {}".format(json_buffer, exc))
            raise exc

        # return sanitized path
        return json_buffer

    # PROPERTIES
    @property
    def source(self) -> str:
        """Look at the structure of the file and determine \
            at which stage of the scan it was produced or if it's an Isogeo export.

        :returns: scan stage ('listing', 'sign', 'lookup') or 'isogeo'
        :rtype: str
        """
        # read structure to identify source
        if isinstance(self.json_data, list) and "dataset" in self.json_data[0]:
            source = "lookup"
        elif isinstance(self.json_data, list) and "feature" in self.json_data[0]:
            source = "sign"
        elif isinstance(self.json_data, list) and "result" in self.json_data[0]:
            source = "listing"
        elif isinstance(self.json_data, dict):
            # test if it's already an Isogeo metadata
            try:
                Metadata.clean_attributes(self.json_data)
                source = "isogeo"
            except Exception:
                logger.warning(
                    "Unknown source: nor Scan, nor Isogeo. JSON data type (list expected): {}".format(
                        type(self.json_data)
                    )
                )
                source = None
        else:
            logger.warning(
                "Unknown stage. JSON data type (list expected): {}".format(
                    type(self.json_data)
                )
            )
            source = None

        # return sanitized path
        return source

    @property
    def as_model(self) -> object:
        """Load JSON into a model.

        :return: model corresponding to the parsed JSON content
        :rtype: object
        """
        if self.source == "listing":
            model = Listing(self.json_data)
        elif self.source == "lookup":
            model = Lookup(**self.json_data[0].get("dataset"))
        elif self.source == "sign":
            model = Sign(**self.json_data[0].get("feature"))
        elif self.source == "isogeo":
            model = Metadata.clean_attributes(self.json_data)
        else:
            model = None

        # return model
        return model


# #############################################################################
# ##### Main #######################
# ##################################
if __name__ == "__main__":
    from os import environ
    from dotenv import load_dotenv

    logging.basicConfig(level=logging.DEBUG)
    # logger.setLevel(logging.INFO)

    # load dev environment vars
    load_dotenv("dev.env", override=True)
    fixtures_dir = Path(environ.get("FIXTURES_DIR"))

    for i in fixtures_dir.glob("**/*.json"):
        json_reader = MetadataJsonReader(i)

        # open JSON
        # print(json_reader.input_json, json_reader.source)
        # print(json_reader.input_json.name)
        model = json_reader.as_model
        if isinstance(model, Lookup):
            # print(model.isMapDocument)
            # print(model.isMapDocument)
            # print(model.isRaster)
            pass
        elif isinstance(model, Sign):
            # print(model.error, model.signatures)
            pass
        elif isinstance(model, Metadata):
            print(model.title_or_name())
        else:
            continue
