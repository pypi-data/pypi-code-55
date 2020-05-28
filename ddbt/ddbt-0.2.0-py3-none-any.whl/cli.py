import argparse
import copy
import os
import sys
import traceback
from typing import List

import dbt.profiler
from dbt.exceptions import RuntimeException
from dbt.logger import GLOBAL_LOGGER as logger
from dbt.logger import log_manager
from dbt.main import (
    _add_common_arguments,
    _add_selection_arguments,
    _add_table_mutability_arguments,
    _build_base_subparser,
    _build_run_subparser,
    adapter_management,
    initialize_config_values,
)
from dbt.utils import ExitCodes

import ddbt.task.bootstrap_schema as bootstrap_schema
import ddbt.task.bootstrap_source as bootstrap_source
import ddbt.task.extract as extract_task
import ddbt.task.run as run_task
from ddbt.constants import (
    DDBT_BOOTSTRAP_ARGS,
    DDBT_BOOTSTRAP_SOURCE_ARGS,
    DDBT_EXTRACT_ARGS,
    DDBT_GIT_ARGS,
    DDBT_MAT_ARGS,
    DDBT_TIME_ARGS,
)


def _get_version() -> str:
    """Get the current version from __init__.

    Returns:
        str: ddbt version
    """
    from ddbt import __version__

    return __version__


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    with log_manager.applicationbound():
        try:
            results, succeeded = handle_and_check(args)
            if succeeded:
                exit_code = ExitCodes.Success.value
            else:
                exit_code = ExitCodes.ModelError.value

        except KeyboardInterrupt:
            logger.info("ctrl-c")
            exit_code = ExitCodes.UnhandledError.value

        # This can be thrown by eg. argparse
        except SystemExit as e:
            exit_code = e.code

        except BaseException as e:
            logger.warning("Encountered an error:")
            logger.warning(str(e))

            if log_manager.initialized:
                logger.debug(traceback.format_exc())
            elif not isinstance(e, RuntimeException):
                # if it did not come from dbt proper and the logger is not
                # initialized (so there's no safe path to log to), log the
                # stack trace at error level.
                logger.error(traceback.format_exc())
            exit_code = ExitCodes.UnhandledError.value

    sys.exit(exit_code)


def handle_and_check(args: List[str]):
    with log_manager.applicationbound():
        parsed = parse_args(args)

        # we've parsed the args - we can now decide if we're debug or not
        if parsed.debug:
            log_manager.set_debug()

        profiler_enabled = False

        if parsed.record_timing_info:
            profiler_enabled = True

        with dbt.profiler.profiler(
            enable=profiler_enabled, outfile=parsed.record_timing_info
        ):
            initialize_config_values(parsed)

            with adapter_management():

                task = parsed.cls.from_args(parsed)
                logger.debug("running ddbt with arguments {parsed}", parsed=str(parsed))
                logger.info("Running with ddbt={}".format(_get_version() + "\n"))
                results, succeeded = task.run()
            return results, succeeded


def _add_ddbt_arguments(*subparsers, **kwargs):
    for sub in subparsers:
        arg_list = copy.deepcopy(kwargs.get("arg_list"))
        for argl in arg_list:
            positional = argl.pop("name_or_flag")
            sub.add_argument(*positional, **argl)


def _set_ddbt_defaults(*subparsers, **kwargs):
    for sub in subparsers:
        for k, v in kwargs.items():
            sub.set_defaults(**{k: v})


def _build_extract_subparser(subparsers, base_subparser):
    extract_sub = subparsers.add_parser(
        "extract",
        parents=[base_subparser],
        help="""
        Extract data using Embulk, a parallel bulk data loader that helps data
        transfer between various storages, databases and cloud services.

        """,
    )
    extract_sub.set_defaults(
        cls=extract_task.ExtractTask, which="extract", rpc_method="extract"
    )
    return extract_sub


def _build_bootstrap_subparser(subparsers, base_subparser):
    bootstrap_sub = subparsers.add_parser(
        "bootstrap",
        parents=[base_subparser],
        help="""
        Bootstrap sources and schemas from database catalog.
        """,
    )
    return bootstrap_sub


def _build_bootstrap_source_subparser(subparsers, base_subparser):
    sub = subparsers.add_parser(
        "source",
        parents=[base_subparser],
        help="""
        Bootstrap sources from database catalog. Task will look into your
        sql and if it refers to one of the sources, it will try to find
        a relation in the database and generate a yml file.
        """,
    )
    sub.set_defaults(
        cls=bootstrap_source.BootstrapSourceTask,
        which="bootstrap-source",
        rpc_method="bootstrap-source",
    )
    return sub


def _build_bootstrap_schema_subparser(subparsers, base_subparser):
    sub = subparsers.add_parser(
        "schema",
        parents=[base_subparser],
        help="""
        Bootstrap schemas from database catalog. Task searches the database
        and compares it to the specified dbt models. If the relation exists,
        the corresponding yml specification (schema) is generated.
        """,
    )
    sub.set_defaults(
        cls=bootstrap_schema.BootstrapSchemaTask,
        which="bootstrap-schema",
        rpc_method="bootstrap-schema",
    )
    return sub


def parse_args(args: List[str]):
    p = argparse.ArgumentParser(
        prog="ddbt",
        description="""
        Extension to dbt cli, an ELT tool for managing
        your SQL transformations and data models.
        For more documentation on these commands, visit: docs.getdbt.com
        """,
        epilog="""
        Specify one of these sub-commands and you can find more help from
        there.
        """,
    )
    # Copied from dbt main.py
    p.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s version: {_get_version()}",
        help="""
        Show version information
        """,
    )

    p.add_argument(
        "-r",
        "--record-timing-info",
        default=None,
        type=str,
        help="""
        When this option is passed, dbt will output low-level timing stats to
        the specified file. Example: `--record-timing-info output.profile`
        """,
    )

    p.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="""
        Display debug logging during dbt execution. Useful for debugging and
        making bug reports.
        """,
    )

    p.add_argument(
        "--log-format",
        choices=["text", "json", "default"],
        default="default",
        help="""Specify the log format, overriding the command's default.""",
    )

    p.add_argument(
        "--no-write-json",
        action="store_false",
        dest="write_json",
        help="""
        If set, skip writing the manifest and run_results.json files to disk
        """,
    )

    p.add_argument(
        "-S",
        "--strict",
        action="store_true",
        help="""
        Run schema validations at runtime. This will surface bugs in dbt, but
        may incur a performance penalty.
        """,
    )

    p.add_argument(
        "--warn-error",
        action="store_true",
        help="""
        If dbt would normally warn, instead raise an exception. Examples
        include --models that selects nothing, deprecations, configurations
        with no associated models, invalid test configurations, and missing
        sources/refs in tests.
        """,
    )

    partial_flag = p.add_mutually_exclusive_group()
    partial_flag.add_argument(
        "--partial-parse",
        action="store_const",
        const=True,
        dest="partial_parse",
        default=None,
        help="""
        Allow for partial parsing by looking for and writing to a pickle file
        in the target directory. This overrides the user configuration file.
        WARNING: This can result in unexpected behavior if you use env_var()!
        """,
    )

    partial_flag.add_argument(
        "--no-partial-parse",
        action="store_const",
        const=False,
        default=None,
        dest="partial_parse",
        help="""
        Disallow partial parsing. This overrides the user configuration file.
        """,
    )

    # if set, run dbt in single-threaded mode: thread count is ignored, and
    # calls go through `map` instead of the thread pool. This is useful for
    # getting performance information about aspects of dbt that normally run in
    # a thread, as the profiler ignores child threads. Users should really
    # never use this.
    p.add_argument(
        "--single-threaded", action="store_true", help=argparse.SUPPRESS,
    )

    # if set, extract all models and blocks with the jinja block extractor, and
    # verify that we don't fail anywhere the actual jinja parser passes. The
    # reverse (passing files that ends up failing jinja) is fine.
    p.add_argument("--test-new-parser", action="store_true", help=argparse.SUPPRESS)

    subs = p.add_subparsers(title="Available sub-commands")

    base_subparser = _build_base_subparser()

    run_sub = _build_run_subparser(subs, base_subparser)
    extract_sub = _build_extract_subparser(subs, base_subparser)
    bootstrap_sub = _build_bootstrap_subparser(subs, base_subparser)
    bootstrap_subs = bootstrap_sub.add_subparsers(title="Available sub-commands")
    bootstrap_source = _build_bootstrap_source_subparser(bootstrap_subs, base_subparser)
    bootstrap_schema = _build_bootstrap_schema_subparser(bootstrap_subs, base_subparser)
    # Extract
    _add_ddbt_arguments(extract_sub, arg_list=DDBT_EXTRACT_ARGS)
    # Bootstrap
    _add_ddbt_arguments(
        bootstrap_source, bootstrap_schema, arg_list=DDBT_BOOTSTRAP_ARGS
    )
    _add_ddbt_arguments(bootstrap_source, arg_list=DDBT_BOOTSTRAP_SOURCE_ARGS)
    # --threads, --no-version-check
    _add_common_arguments(run_sub)
    # --models, --exclude
    _add_selection_arguments(run_sub, bootstrap_source, bootstrap_schema, extract_sub)
    # --full-refresh
    _add_table_mutability_arguments(run_sub)
    # add ddbt run args
    _add_ddbt_arguments(
        run_sub, bootstrap_source, bootstrap_schema, arg_list=DDBT_GIT_ARGS
    )
    _add_ddbt_arguments(
        run_sub, bootstrap_source, bootstrap_schema, arg_list=DDBT_MAT_ARGS
    )
    _add_ddbt_arguments(run_sub, extract_sub, arg_list=DDBT_TIME_ARGS)

    # change run cls
    _set_ddbt_defaults(run_sub, cls=run_task.RunTask, which="run")

    if len(args) == 0:
        p.print_help()
        sys.exit(1)

    parsed = p.parse_args(args)

    if hasattr(parsed, "profiles_dir"):
        parsed.profiles_dir = os.path.expanduser(parsed.profiles_dir)

    if not hasattr(parsed, "which"):
        # the user did not provide a valid subcommand. trigger the help message
        # and exit with a error
        p.print_help()
        p.exit(1)

    return parsed
