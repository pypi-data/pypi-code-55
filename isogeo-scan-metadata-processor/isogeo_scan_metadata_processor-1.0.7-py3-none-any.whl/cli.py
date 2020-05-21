#! python3  # noqa: E265

"""
    Command-line to read metadata produced by FME scripts of Isogeo Scan,
    convert it into Isogeo model, apply rules and export it to a database or Isogeo.

    Author: Isogeo
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler
from os import environ, getlogin
from pathlib import Path
from platform import architecture
from platform import platform as opersys
from socket import gethostname
from timeit import default_timer
from urllib.request import getproxies

# 3rd party library
import click
from dotenv import load_dotenv

# submodules
from scan_metadata_processor.__about__ import __version__
from scan_metadata_processor.commands import cli_check, cli_clean, cli_process
from scan_metadata_processor.utils.bouncer import exit_cli_error

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
# ########## Functions #############
# ##################################


def log_start(log_filename="ISOGEO_MD_PROCESSOR_metadata_processor"):
    # required subfolder
    dir_logs = Path(environ.get("ISOGEO_MD_PROCESSOR_LOGS"))
    try:
        dir_logs.mkdir(exist_ok=True)
    except PermissionError as e:
        msg_err = (
            "Impossible to write the logs. Does the user '{}' ({}) have write permissions "
            "on the LOGS folder?. Original error: {}".format(
                environ.get("userdomain"), getlogin(), e
            )
        )
        exit_cli_error(msg_err)

    # create the logger
    logger = logging.getLogger()
    logging.captureWarnings(True)
    # logger.setLevel(logging.INFO)

    # set the format
    log_format = logging.Formatter(
        "%(asctime)s || %(levelname)s "
        "|| %(module)s - %(lineno)d ||"
        " %(funcName)s || %(message)s"
    )

    # log to the file
    log_file_handler = RotatingFileHandler(
        filename=dir_logs / "{}.log".format(log_filename),
        mode="a",
        maxBytes=3000000,
        backupCount=10,
        encoding="UTF-8",
    )

    log_file_handler.setLevel(logging.INFO)
    log_file_handler.setFormatter(log_format)

    # log to the console
    log_console_handler = logging.StreamHandler()
    log_console_handler.setLevel(logging.WARNING)
    log_console_handler.setFormatter(log_format)

    # add file and console handlers to the logger
    logger.addHandler(log_file_handler)
    # logger.addHandler(log_console_handler)

    # initialize the log
    logger.info(
        "===================== ISOGEO Scan Metadata Processor - Version {} =====================".format(
            __version__
        )
    )
    logger.info("Operating System: {}".format(opersys()))
    logger.info("Architecture: {}".format(architecture()[0]))
    logger.info("Computer: {}".format(gethostname()))
    logger.info("Launched by: {}".format(getlogin()))
    logger.info("OS Domain: {}".format(environ.get("userdomain")))
    logger.info("Network proxies detected: {}".format(len(getproxies())))

    return logger


# #############################################################################
# ####### Command-line ############
# #################################


@click.group(invoke_without_command=True, context_settings=CONTEXT_SETTINGS)
@click.option(
    "-l",
    "--label",
    help="Custom the name of the task (used to name the log file)",
    default="isogeo_metadata_processor",
)
@click.option(
    "-s",
    "--settings",
    default=".env",
    help="Environment file containing settings",
    type=click.Path(exists=True, readable=True),
)
@click.version_option(version=__version__, message="%(version)s")
@click.pass_context
def scan_metadata_processor(
    cli_context: click.Context, label: str, settings: Path,
):
    """Command-line checking settings and executing required operations.

    \f
    :param click.core.Context cli_context: Click context
    :param str label: name of run, used to custom some outputs (logs...)
    :param str settings: path to a settings file containing credentials to read database

    :Example:
        .. code-block:: powershell

        .\Isogeo_ScanMetadataProcessor.exe --label "Check" --settings .\settings.env check

    """
    # Load settings
    if Path(settings).exists():
        load_dotenv(settings, override=True)
        logging.info(
            "Settings loaded. Platfom used: {}".format(environ.get("ISOGEO_PLATFORM"))
        )
    else:
        click.Abort(
            FileNotFoundError("Settings file is missing. Please create an '.env' file.")
        )

    # create the log manager before all
    logger = log_start(label)

    # apply debug mode
    if int(environ.get("DEBUG")):
        logger.setLevel(logging.DEBUG)
        for handler in logger.handlers:
            handler.setLevel(logging.DEBUG)

    # create output folder
    output_folder = Path(
        environ.get("ISOGEO_MD_PROCESSOR_OUTPUT_FOLDER"),
        datetime.now().strftime("%Y%m%d_%H%M%S"),
    )
    try:
        output_folder.mkdir(parents=True, exist_ok=True)
    except PermissionError as e:
        msg_err = (
            "Impossible to create the output folder. Does the user '{}' ({}) have write permissions "
            "on the OUTPUT folder? Original error: {}".format(
                environ.get("userdomain"), getlogin(), e
            )
        )
        exit_cli_error(msg_err)

    # create logs subfolder
    logs_folder = Path(
        environ.get("ISOGEO_MD_PROCESSOR_LOGS"),
        datetime.now().strftime("%Y%m%d_%H%M%S"),
    )
    logs_folder.mkdir(parents=True, exist_ok=True)

    # save settings into the CLI context dict
    cli_context.obj["FOLDER_INPUT"] = Path(
        environ.get("ISOGEO_MD_PROCESSOR_INPUT_FOLDER")
    )
    cli_context.obj["FOLDER_OUTPUT"] = output_folder
    cli_context.obj["FOLDER_LOGS"] = logs_folder
    cli_context.obj["LABEL"] = label

    # db_manager.close_database()
    logger.info(
        "Main CLI completed after {:5.2f}s.".format(default_timer() - START_TIME)
    )


# -- SUB-COMMANDS ----------------------------------------------------------------------
# Add subcommands to the main command group
scan_metadata_processor.add_command(cli_check.check)
scan_metadata_processor.add_command(cli_clean.clean)
scan_metadata_processor.add_command(cli_process.process)


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
    scan_metadata_processor(obj={})
