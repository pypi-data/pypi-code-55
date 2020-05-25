import itertools
from pathlib import Path

import fire

from azureml.studio.core.io.image_directory import (COMPRESSED_EXT_TO_CLASS,
                                                    ImageDirectory)
from azureml.studio.core.logger import logger
from azureml.studio.internal.error import ErrorMapping, InvalidDatasetError
from azureml.studio.internal.error_handler import error_handler


def load(input_path, loader=ImageDirectory.load_compressed):
    try:
        return loader(input_path)
    except Exception as e:
        ErrorMapping.rethrow(e, InvalidDatasetError(
            dataset1=input_path.name,
            reason=f"Got exception when loading: {ErrorMapping.get_exception_message(e)}",
            troubleshoot_hint="Please make sure there is image in input dataset."))


@error_handler
def convert(input_path, output_path):
    input_path = Path(input_path)
    if input_path.is_file():
        if input_path.suffix in COMPRESSED_EXT_TO_CLASS:
            logger.info(
                f"Input is compressed file. Loading from {input_path}.")
            loader_dir = load(input_path)
        else:
            ErrorMapping.throw(
                InvalidDatasetError(
                    dataset1=input_path.name,
                    reason=f"Only file with {set(COMPRESSED_EXT_TO_CLASS.keys())} extensions is accepted"))
    else:
        # load from any valid compressed file in first layer of current directory.
        compressed_file_paths = list(itertools.islice((
            path for path in input_path.iterdir() if path.suffix in COMPRESSED_EXT_TO_CLASS), 1))
        if len(compressed_file_paths) > 0:
            logger.info(
                f"Found compressed file. Loading from {compressed_file_paths[0]}.")
            loader_dir = load(compressed_file_paths[0])
        else:
            # try to load from current directory.
            logger.info(f"Loading from directory {input_path}.")
            loader_dir = load(input_path, loader=ImageDirectory.load)

    loader_dir.dump(output_path)


if __name__ == '__main__':
    fire.Fire(convert)
