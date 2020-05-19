import os
import json
import abc
import shutil
from zipfile import ZipFile
from click import Path as ClickPath, UsageError
from clint.textui import progress

from typing import Dict, List
from pathlib import Path
import pprint
import requests
from loguru import logger

from .utils import option, command, Cli, setup_logger as default_setup_logger
from .models import FileRef, Output


class BaseModule(abc.ABC, Cli):
    OUTPUT_FILENAME: str = os.getenv("OUTPUT_FILENAME", "outputs.json")
    CHUNK_SIZE: int = 2391975

    @abc.abstractmethod
    def run_job_logic(self, parameters: dict, files: Dict[str, FileRef]) -> Output:
        """
        This is the custom implementation of what will become an interface. Does the necessary setup
        to execute the existing module code. This method should represent 90% or more of the custom code
        required to create a module using pre existing logic.

        Arguments:
            parameters {dict} -- [description]
            files {dict} -- [description]
            output_path {str} -- [description]
        """
        pass

    @classmethod
    def setup_logger(cls):
        default_setup_logger()

    def create_artifacts(
        self, output: Output, artifact_path: str = "./", zip: bool = False
    ):
        logger.info("Creating job artifacts")
        if artifact_path != "./":
            Path(artifact_path).mkdir(parents=True, exist_ok=True)

        outfile_path = os.path.join(artifact_path, self.OUTPUT_FILENAME)
        with open(outfile_path, "w") as outfile:
            outfile.write(output.output_json + "\n")
            logger.info(f"Output JSON saved to {outfile_path}")

        if output.files is not None:
            to_zip = []
            logger.info(f"Ensuring output files are in correct folder: {artifact_path}")
            for _file in output.files:
                target = Path(os.path.join(artifact_path, f"{_file.name}"))
                if not target.exists() and _file.path is not None:
                    logger.info(f"Moving {_file.path} to {target}")
                    shutil.move(_file.path, target)
                to_zip.append({"path": str(target), "name": f"{_file.name}"})

            if zip:
                zip_path = os.path.join(artifact_path, "files.zip")
                logger.info(f"Creating output files zip: {zip_path}")
                with ZipFile(zip_path, "w") as zipObj:
                    for zf in to_zip:
                        zipObj.write(zf["path"], zf["name"])
                        logger.info(f"Added {zf['name']} to {zip_path}")

    def download_files(
        self, file_refs: List[dict], files_path: str = "./"
    ) -> Dict[str, FileRef]:
        output_file_refs = {}
        for _fr in file_refs:
            file_ref = FileRef(**_fr)

            if file_ref is None:
                raise ValueError(
                    f"File Ref {file_ref.name} has no url to download the file"
                )

            r = requests.get(file_ref.url, stream=True)  # type: ignore

            target_path = Path(os.path.join(files_path, f"{file_ref.name}"))
            target_path.parent.mkdir(parents=True, exist_ok=True)

            with open(target_path, "wb") as _file:
                length = r.headers.get("content-length")
                total_length = None
                if length is not None:
                    total_length = int(length)
                logger.info(
                    f"Downloading {file_ref.name} Size: {length} to {target_path}"
                )
                if total_length is not None:
                    for ch in progress.bar(
                        r.iter_content(chunk_size=self.CHUNK_SIZE),
                        expected_size=(total_length / 1024) + 1,
                    ):
                        if ch:
                            _file.write(ch)
                else:
                    for ch in r.iter_content(chunk_size=self.CHUNK_SIZE):
                        _file.write(ch)
            file_ref.path = str(target_path)
            output_file_refs[file_ref.id] = file_ref
        return output_file_refs

    @command("run-job")
    @option(
        "params_path",
        "--params-path",
        default=None,
        envvar="PARAMS_PATH",
        type=ClickPath(exists=True),
    )
    @option(
        "params_json", "--params-json", default=None, envvar="PARAMS_JSON", type=str
    )
    @option(
        "file_refs_json",
        "--files-json",
        default=None,
        envvar="FILE_REFS_JSON",
        type=str,
    )
    @option(
        "file_refs_path",
        "--files-path",
        default=None,
        envvar="FILE_REFS_PATH",
        type=ClickPath(exists=True),
    )
    @option(
        "input_path",
        "--input",
        default="input",
        envvar="FILES_IN_PATH",
        type=ClickPath(),
    )
    @option(
        "output_path",
        "--output",
        default="output",
        envvar="OUTPUT_PATH",
        type=ClickPath(),
    )
    @option("--zip", is_flag=True)
    def run_job(
        self,
        params_path,
        params_json,
        file_refs_json,
        file_refs_path,
        input_path,
        output_path,
        zip,
    ):
        self.setup_logger()
        if params_json:
            parameters = json.loads(params_json)
        elif params_path:
            with open(params_path) as json_file:
                parameters = json.load(json_file)
        else:
            err_str = "One of either --params-json or --params-path is required"
            logger.error(err_str)
            raise UsageError(err_str)

        logger.info(f"--- Using Parameters --- \n {pprint.pformat(parameters)}")

        file_refs = None
        if file_refs_json:
            file_refs = json.loads(file_refs_json)
        elif file_refs_path:
            with open(file_refs_path) as json_file:
                file_refs = json.load(json_file)
        # Download inputs
        if file_refs is not None:
            file_refs = self.download_files(file_refs, input_path)

        if file_refs is not None:
            logger.info(f"--- Using Files ---")
            for fr in file_refs.keys():
                logger.info(f"{fr} - Path: {file_refs[fr].path}")
        else:
            logger.info(f"--- No Input Files ---")

        output = self.run_job_logic(parameters, file_refs)

        # Package up outputs
        self.create_artifacts(output, output_path, zip)
