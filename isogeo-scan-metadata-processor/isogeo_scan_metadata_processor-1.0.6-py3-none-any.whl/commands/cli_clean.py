#! python3  # noqa: E265

"""
    Sub-command in charge of cleaning up temporary files.

    Author: Isogeo
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging
from datetime import datetime, timedelta
from os import environ
from pathlib import Path
from timeit import default_timer

# 3rd party library
import click
from send2trash import send2trash

# #############################################################################
# ########## Globals ###############
# ##################################

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
@click.option(
    "-rm",
    "--remove-empty-folders",
    help="Remove empty folders.",
    is_flag=True,
    default=True,
    show_default=True,
)
@click.pass_context
def clean(cli_context: click.Context, remove_empty_folders: bool):
    """Delete logs and output folders older than the frequency set in the configuration.

    \f
    :param click.core.Context cli_context: Click context
    :param bool remove_empty_folders: if passed, empty folders will be deleted too
    """
    logger.info(
        "Let's clean files and folders created more than {} days ago.".format(
            environ.get("ISOGEO_MD_PROCESSOR_CLEAN_FREQUENCY")
        )
    )
    date_ref_days_ago = datetime.now() - timedelta(
        days=int(environ.get("ISOGEO_MD_PROCESSOR_CLEAN_FREQUENCY"))
    )

    # logs folder
    li_folders_logs = Path(environ.get("ISOGEO_MD_PROCESSOR_LOGS")).iterdir()
    with click.progressbar(
        list(li_folders_logs), label="Removing log folders",
    ) as log_folders:
        for subobj in log_folders:
            # compare last modification date
            if datetime.fromtimestamp(subobj.stat().st_mtime) < date_ref_days_ago:
                logger.debug(
                    "CLEANER - LOGS - Detected folder/file outdated: {}".format(subobj)
                )
                try:
                    send2trash(str(subobj.resolve()))
                except Exception as e:
                    logger.warning(
                        "Unable to delete: {}. Original error: {}".format(
                            subobj.resolve(), e
                        )
                    )
            # handle empty folders
            if (
                remove_empty_folders
                and subobj.is_dir()
                and not list(subobj.glob("**/*"))
            ):
                logger.info(
                    "Empty folder spotted: {}. Sending it to the trash...".format(
                        str(subobj.resolve())
                    )
                )
                try:
                    send2trash(str(subobj.resolve()))
                except Exception as e:
                    logger.warning(
                        "Unable to delete: {}. Original error: {}".format(
                            subobj.resolve(), e
                        )
                    )

    # output folder
    li_folders_output = Path(environ.get("ISOGEO_MD_PROCESSOR_OUTPUT_FOLDER")).iterdir()
    with click.progressbar(
        list(li_folders_output), label="Removing output folders",
    ) as output_folders:
        for subobj in output_folders:
            if datetime.fromtimestamp(subobj.stat().st_ctime) < date_ref_days_ago:
                logger.info(
                    "CLEANER - OUTPUT- Detected folder/file outdated: {}".format(subobj)
                )
                try:
                    send2trash(str(subobj.resolve()))
                except Exception as e:
                    logger.warning(
                        "Unable to delete: {}. Original error: {}".format(
                            subobj.resolve(), e
                        )
                    )
            # handle empty folders
            if (
                remove_empty_folders
                and subobj.is_dir()
                and not list(subobj.glob("**/*"))
            ):
                logger.info(
                    "Empty folder spotted: {}. Sending it to the trash...".format(
                        str(subobj.resolve())
                    )
                )
                try:
                    send2trash(str(subobj.resolve()))
                except Exception as e:
                    logger.warning(
                        "Unable to delete: {}. Original error: {}".format(
                            subobj.resolve(), e
                        )
                    )


# #############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    """Standalone execution."""
    # additionnal imports
    import multiprocessing

    # 3rd party
    from dotenv import load_dotenv

    # load settings as environment vars
    load_dotenv("./dev.env", override=True)
    # workaround for multiprocessing support for packaged version on Windows
    # see: https://github.com/pyinstaller/pyinstaller/wiki/Recipe-Multiprocessing
    # and: https://stackoverflow.com/a/48805137/2556577
    multiprocessing.freeze_support()
    # launch cli
    clean(obj={})
