#! python3  # noqa: E265

"""
    Sub-command in charge of processing input ZIP files and loading results into database.

    Author: Isogeo
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import gettext
import logging
from os import environ, rename
from pathlib import Path
from timeit import default_timer

# 3rd party library
import click

# submodules
from scan_metadata_processor import ES_ENABLED, MetadataJsonReader, Unzipper
from scan_metadata_processor.utils.bouncer import (
    exit_cli_error,
    exit_cli_normal,
    exit_cli_success,
)

if ES_ENABLED:
    from scan_metadata_processor.database.elasticsearch import ElasticSearchManager

# #############################################################################
# ########## Globals ###############
# ##################################

# localization
_ = gettext.gettext

# chronometer
START_TIME = default_timer()

# logs
logger = logging.getLogger(__name__)

# default CLI context.
# See: https://click.palletsprojects.com/en/7.x/commands/#context-defaults
CONTEXT_SETTINGS = dict(obj={})


# #############################################################################
# ####### Command-line ############
# #################################
@click.command()
@click.pass_context
def process(cli_context: click.Context):
    """Process input metadata (zipped) and load into database."""

    logger.info("PROCESS started after {:5.2f}s.".format(default_timer() - START_TIME))

    # retrieve values from CLI context
    input_folder = cli_context.obj.get("FOLDER_INPUT")
    output_folder = cli_context.obj.get("FOLDER_OUTPUT")

    # -- ZIP EXTRACTION ----------------------------------------------------------------
    # looking for zip files
    extraction_folder = Path(output_folder / "to_process")
    li_zip_files = list(input_folder.glob("**/*.zip"))
    if not len(li_zip_files):
        exit_cli_normal("No ZIP files found in: {}".format(extraction_folder.resolve()))

    # parse zip files and extract JSON files
    with click.progressbar(
        iterable=li_zip_files, length=len(li_zip_files), label="Extracting ZIP files..."
    ) as prgbar_zip_to_extract:
        for in_zip in prgbar_zip_to_extract:
            unzipper = Unzipper(in_zip)
            extracted = unzipper.unzip(
                to_folder=extraction_folder, all_in=0, only_extensions=(".json",),
            )
            if not extracted:
                logger.warning("No JSON file found into the ZIP: {}".format(in_zip))
                continue
            else:
                logger.debug(
                    "{} JSON files extracted from '{}' to '{}'".format(
                        len(extracted), in_zip, extraction_folder
                    )
                )

    # -- DATABASE CONFIGURATION --------------------------------------------------------
    db_type = environ.get("ISOGEO_MD_PROCESSOR_DATABASE_TYPE", None)
    if db_type is None:
        exit_cli_error(
            "setting ISOGEO_MD_PROCESSOR_DATABASE_TYPE is not correctly set."
        )

    if db_type == "elastic-search" and ES_ENABLED:
        # db connection
        elasticlient = ElasticSearchManager(
            host=environ.get("DATABASE_HOST"),
            port=environ.get("DATABASE_PORT"),
            pool_size=environ.get("DATABASE_POOL_CONNECTIONS"),
            user=environ.get("DATABASE_USER"),
            password=environ.get("DATABASE_PASSWORD"),
            ssl=int(environ.get("DATABASE_SSL", "1")),
        )

        # connect
        elasticlient.connect()

        # ensure index is created
        elasticlient.create_index()

        # store db insertion method
        db_insertion = elasticlient.insert_document
    elif db_type == "elastic-search" and not ES_ENABLED:
        exit_cli_error(
            ModuleNotFoundError(
                _("Elastic Search package dependency is not available.")
            )
        )
    else:
        exit_cli_error(
            NotImplementedError(
                _("This database type '{}' is not implemented yet.".format(db_type))
            )
        )

    # -- JSON PROCESSING ---------------------------------------------------------------
    # looking for JSON files
    li_json_files = list(extraction_folder.glob("**/*.json"))
    if not len(li_json_files):
        exit_cli_normal("No JSON files to import")

    # create the output folder
    processed_folder = Path(output_folder / "processed" / "to_{}".format(db_type))
    processed_folder.mkdir(parents=True, exist_ok=True)

    with click.progressbar(
        iterable=li_json_files,
        length=len(li_json_files),
        label="Processing JSON files to {}".format(db_type),
    ) as prgbar_json_to_process:
        for in_json in prgbar_json_to_process:
            # load JSON
            try:
                json_reader = MetadataJsonReader(in_json)
                logger.debug(
                    "Metadata from '{}' found into JSON: {}".format(
                        json_reader.source, json_reader.input_json
                    )
                )
            except Exception as exc:
                logger.error(exc)
                continue

            # import into selected database
            db_insertion(
                document_to_index=json_reader.as_model.to_dict(),
                auto_refresh="wait_for",
                document_type="metadata-lookup",
            )

            # archive loaded JSON
            rename(src=in_json, dst=processed_folder / in_json.name)

        # refresh indices
        elasticlient.es_client.indices.refresh()

    # ending
    exit_cli_success(
        "PROCESS completed after {:5.2f}s.".format(default_timer() - START_TIME)
    )


# #############################################################################
# ##### Stand alone program ########
# ##################################

if __name__ == "__main__":
    """Standalone execution."""
    # additionnal imports
    import multiprocessing

    # workaround for multiprocessing support for packaged version on Windows
    # see: https://github.com/pyinstaller/pyinstaller/wiki/Recipe-Multiprocessing
    # and: https://stackoverflow.com/a/48805137/2556577
    multiprocessing.freeze_support()
    # launch cli
    process(obj={})
