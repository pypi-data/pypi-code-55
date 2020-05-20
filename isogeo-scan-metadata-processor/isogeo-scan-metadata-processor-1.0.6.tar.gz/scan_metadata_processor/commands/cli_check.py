#! python3  # noqa: E265


"""
    Sub-command in charge of checking settings and environment.

    Author: Isogeo
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging
from gettext import gettext
from os import access, environ, getlogin, R_OK, W_OK
from pathlib import Path
from timeit import default_timer

# 3rd party library
import click
from isogeo_pysdk.checker import IsogeoChecker
from requests import HTTPError, Session

# submodules
from scan_metadata_processor import ES_ENABLED
from scan_metadata_processor.utils.proxies import proxy_settings
from scan_metadata_processor.utils.bouncer import exit_cli_error, exit_cli_success

# #############################################################################
# ########## Globals ###############
# ##################################

# translation
_ = gettext

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
def check(cli_context: click.Context):
    """Perform checks about requirements: folders, network..."""
    logger.info("CHECK started after {:5.2f}s.".format(default_timer() - START_TIME))

    # extract values from CLI context
    logs_folder = cli_context.obj.get("FOLDER_LOGS")
    output_folder = cli_context.obj.get("FOLDER_OUTPUT")

    # -- CHECK FOLDERS PERMISSIONS -----------------------------------------------------
    if not access(logs_folder, W_OK):
        err_msg = "The LOGS folder is not writable by '{}': {}".format(
            getlogin(), logs_folder.resolve()
        )
        exit_cli_error(err_msg)

    if not access(output_folder, W_OK):
        err_msg = "The OUTPUT folder is not writable by '{}': {}".format(
            getlogin(), output_folder.resolve()
        )
        exit_cli_error(err_msg)

    input_folder = Path(environ.get("ISOGEO_MD_PROCESSOR_INPUT_FOLDER"))
    if not access(input_folder, R_OK):
        err_msg = "The INPUT folder is not readable by '{}': {}".format(
            getlogin(), input_folder.resolve()
        )
        exit_cli_error(err_msg)

    # -- DATABASE ----------------------------------------------------------------------
    db_type = environ.get("ISOGEO_MD_PROCESSOR_DATABASE_TYPE", None)
    if db_type == "elastic-search" and not ES_ENABLED:
        err_msg = _(
            "Database type is set to Elastic Search but the required package is not installed."
        )
        exit_cli_error(err_msg)

    if not Path(environ.get("ISOGEO_MD_PROCESSOR_DATABASE_FOLDER")).is_dir():
        logger.error(
            "Folder path for the database is not correct: {}".format(
                environ.get("ISOGEO_MD_PROCESSOR_DATABASE_FOLDER")
            )
        )
    database_folder = Path(environ.get("ISOGEO_MD_PROCESSOR_DATABASE_FOLDER"))

    try:
        database_folder.mkdir(parents=True, exist_ok=True)
        logger.info("Database folder: {}".format(database_folder))
    except PermissionError as e:
        msg_err = (
            "Impossible to create the output folder. Does the user '{}' ({}) have write permissions "
            "on the OUTPUT folder?. Original error: {}".format(
                environ.get("userdomain"), getlogin(), e
            )
        )
        exit_cli_error(msg_err)

    if not IsogeoChecker().check_is_uuid(environ.get("ISOGEO_GROUP_ID")):
        exit_cli_error("Isogeo group UUID is not correct")

    # -- NETWORK -----------------------------------------------------------------------
    if int(environ.get("FULL_OFFLINE_MODE")) == 0 and db_type == "azure-isogeo":
        # load urls to check from text file defined in settings
        file_urls_to_check = Path(
            environ.get("URLS_TO_CHECK", "./urls_network_check.txt")
        )
        if file_urls_to_check.is_file():
            # urls_to_check = []
            with file_urls_to_check.open(mode="r", encoding="UTF8") as in_file:
                urls_to_check = in_file.read().splitlines()
            urls_to_check = [url for url in urls_to_check if len(url)]
        else:
            urls_to_check = None
        check_network(urls_to_check)
        logger.info("Network connections are good.")
    else:
        logger.info("Full offline mode enabled: network has not been tested.")

    # ending
    exit_cli_success(
        message=_("CHECK completed after {:5.2f}s.").format(
            default_timer() - START_TIME
        ),
        abort=False,
    )


def check_network(urls_to_check: list = None, check_azure_storage: bool = True) -> bool:
    """Check to contact URLs passed in as arg and a connection to Azure blob storage.

    :param list urls_to_check: list of URls to check. If None, fallback to Isogeo URLs. Defaults to: None - optional
    :param bool check_azure_storage: option to check also connection to Azure blob. Defaults to: True - optional

    :return: True
    :rtype: bool
    """
    fallback_urls = [
        "https://api.isogeo.com/about",
        "http://help.isogeo.com/",
        "https://id.api.isogeo.com/about",
    ]
    if urls_to_check is None:
        urls_to_check = fallback_urls

    # open http session
    with Session() as chuck:
        # set session options
        chuck.proxies = proxy_settings()
        chuck.verify = bool(int(environ.get("SSL_VERIFICATION", 1)))

        # try classic urls
        for url in urls_to_check:
            resp = chuck.get(url=url)
            try:
                resp.raise_for_status()
                logging.debug("URL check passed for: {}".format(url))
            except HTTPError as err:
                exit_cli_error(
                    _("Check URL failed. '{}' is not reachable. Trace: {}").format(
                        url, err
                    )
                )

    return True


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
    check(obj={})
