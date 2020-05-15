"""UJOSchema.

Usage:
  UJOSchema (-h | --help)
  UJOSchema into markdown <source> [-d FOLDER] [-e EXTENSION]
  UJOSchema into binary <source> [-d FOLDER] [-e EXTENSION] [-t TARGET]

Options:
  -h --help  Show this screen.

  into markdown <source>
      convert given SOURCE (file or folder) to markdown

  into binary <source>
      convert given SOURCE (file or folder) to binary

  -d FOLDER --destination FOLDER
      destination folder for generated files [default: .]

  -e EXTENSION --extension EXTENSION
      if SOURCE is a folder, only process files with the specified extension [default: .ujs]

  -t TARGET --target TARGET
      name of a definition target. other types in the schema will be ignored, unless nested.
"""

import sys
import logging
from enum import Enum
from pathlib import Path

from docopt import docopt
from lark.exceptions import LarkError

from UJOSchema import schema_from_str, schema_to_markdown, schema_to_binary


class ConversionTargetFormats(Enum):
    MARKDOWN = "markdown"
    BINARY = "binary"


def main():
    arguments = docopt(__doc__)

    if arguments.get("into"):
        if arguments.get("markdown"):
            target_format = ConversionTargetFormats.MARKDOWN
        elif arguments.get("binary"):
            target_format = ConversionTargetFormats.BINARY
        else:
            return  # docopt should prevent us from reaching this anyway

        convert(
            source=arguments["<source>"],
            destination=arguments["--destination"],
            extension=arguments["--extension"],
            target_format=target_format,
            target_type=arguments.get("--target"),
        )


def convert(source, destination, extension, target_format, target_type=None):
    try:
        destination = Path(destination).resolve()
        destination.mkdir(parents=True, exist_ok=True)
    except OSError as error:
        log.error(f"Failed to create output directory: {error}")
        return

    for schema_file in get_schema_files(source, extension):
        log.info(f"converting: {schema_file} ...")

        schema = schema_from_file(schema_file)
        if not schema:
            continue

        if target_format is ConversionTargetFormats.MARKDOWN:
            md_file = destination / (schema_file.stem + ".md")
            md = schema_to_markdown(schema)
            write_to_file(destination=md_file, mode="w+", content=md)
        elif target_format is ConversionTargetFormats.BINARY:
            bin_file = destination / ((target_type or schema_file.stem) + ".bin")
            bin_data = schema_to_binary(schema, target_type)
            write_to_file(destination=bin_file, mode="wb+", content=bin_data)


def get_schema_files(source, extension):
    try:
        source_path = Path(source).resolve()
    except OSError as error:
        log.error(f"Failed to process source: {error}")
        return []

    if source_path.is_dir():
        schema_files = source_path.glob("*." + extension.split(".")[-1])
    else:
        schema_files = [source_path]
    return schema_files


def schema_from_file(schema_file):
    try:
        with open(schema_file) as sf:
            schema = schema_from_str(sf.read())
    except OSError as error:
        log.error(f"Failed to read {schema_file}: {error}")
    except LarkError as error:
        log.error(f"Failed to parse {schema_file}: {error}")
    else:
        return schema


def write_to_file(destination, mode, content):

    try:
        with open(destination, mode) as md_file:
            md_file.write(content)
    except OSError:
        log.error(f"Failed to write to {destination}")
    else:
        log.info(f"... done: {destination}")


if __name__ == "__main__":

    formatter = logging.Formatter("%(levelname)s: %(message)s")

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    log = logging.getLogger(Path(__file__).parent.stem)
    log.addHandler(handler)
    # log.setLevel(logging.INFO)
    log.setLevel(logging.DEBUG)

    main()
