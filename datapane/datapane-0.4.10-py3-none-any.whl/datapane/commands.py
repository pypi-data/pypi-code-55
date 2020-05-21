import dataclasses as dc
import os
import tarfile
import time
import typing as t
import uuid
from contextlib import contextmanager, suppress
from distutils.dir_util import copy_tree
from distutils.util import strtobool
from pathlib import Path
from typing import Dict, Iterator, List, Optional, Tuple

import click
import click_spinner
import requests
from jinja2 import Environment, FileSystemLoader
from packaging import version as v
from requests import HTTPError
from tabulate import tabulate

from dp_common import JDict, SDict, log, scripts
from dp_common.scripts import config as sc

from . import api
from . import config as c
from ._version import __rev__, __version__

DEBUG: bool = False


def check_pip_version() -> None:
    # this is a bit of a hack for now - want to do upon server API call
    cli_version = v.Version(__version__)
    if __version__ == "0.0.1":  # we're on dev version
        return None
    url = "https://pypi.org/pypi/datapane/json"
    r = requests.get(url=url)
    r.raise_for_status()
    pip_version = v.Version(r.json()["info"]["version"])
    log.debug(f"CLI version {cli_version}, latest pip version {pip_version}")
    if pip_version > cli_version:
        failure_msg(
            f'Your client is out-of-date (version {cli_version}) and may be causing errors, please upgrade to {pip_version} using pip ("pip3 install --upgrade [--user] datapane")'
        )
        exit(2)
        # click.launch("https://pypi.org/project/datapane/")


# TODO
#  - add info subcommand
#  - convert to use typer (https://github.com/tiangolo/typer) or autoclick
def init(debug: Optional[bool], config_env: str):
    """Init the cmd-line env"""
    api.init(config_env=config_env, debug=debug or False)
    with suppress(Exception):
        check_pip_version()

    # config_f = c.load_from_envfile(config_env)
    # _debug = debug if debug is not None else c.config.debug
    # setup_logging(verbose_mode=_debug)
    # log.debug(f"Loaded environment from {config_f}")


@dc.dataclass(frozen=True)
class DPContext:
    """
    Any shared context we want to pass across commands,
    easier to just use globals in general tho
    """

    env: str


def success_msg(msg: str):
    click.secho(msg, fg="green")


def failure_msg(msg: str, do_exit: bool = False):
    click.secho(msg, fg="red")
    if do_exit:
        ctx: click.Context = click.get_current_context(silent=False)
        ctx.exit(2)


@contextmanager
def api_error_handler(err_msg: str):
    try:
        yield
    except HTTPError as e:
        log.error(e)
        failure_msg(err_msg, do_exit=True)


def gen_title() -> str:
    return f"New - {uuid.uuid4().hex}"


def print_table(xs: t.Iterable[SDict], obj_name: str) -> None:
    success_msg(f"Available {obj_name}:")
    print(tabulate(xs, headers="keys", showindex=True))


###############################################################################
# Main
@click.group()
@click.option("--debug/--no-debug", default=None, help="Enable additional debug output.")
@click.option("--env", default=c.DEFAULT_ENV, help="Alternate config environment to use.")
@click.version_option(version=f"{__version__} ({__rev__})")
@click.pass_context
def cli(ctx, debug: bool, env: str):
    """Datapane CLI Tool"""
    global DEBUG
    DEBUG = debug
    init(debug, env)
    ctx.obj = DPContext(env=env)


###############################################################################
# Auth
@cli.command()
@click.option("--token", prompt="Your API Token", help="API Token to the Datapane server.")
@click.option("--server", default="https://datapane.com", help="Datapane API Server URL.")
@click.pass_obj
def login(obj: DPContext, token, server):
    """Login to a server with the given API token."""
    config = c.Config(server=server, token=token)
    r = api.Resource(endpoint="/settings/login/", config=config).get()

    # update config with valid values
    with c.update_config(obj.env) as x:
        x["server"] = server
        x["token"] = token

    # click.launch(f"{server}/settings/")
    success_msg(f"Logged in to {server} as {r.username}")


@cli.command()
@click.pass_obj
def logout(obj: DPContext):
    """Logout from the server and reset the API token in the config file."""
    with c.update_config(obj.env) as x:
        x["server"] = c.DEFAULT_SERVER
        x["token"] = c.DEFAULT_TOKEN

    success_msg(f"Logged out from {c.config.server}")


@cli.command()
def ping():
    """Check can connect to the server."""
    try:
        r = api.Resource(endpoint="/settings/login").get()
        success_msg(f"Connected to {c.config.server} as {r.username}")
    except HTTPError as e:
        failure_msg(f"Couldn't successfully connect to {c.config.server}, check your login details")
        log.error(e)


###############################################################################
# Blobs
@cli.group()
def blob():
    """Commands to work with Blobs"""
    ...


@blob.command()
@click.argument("file", type=click.Path(exists=True))
@click.option("--title", default=gen_title)
@click.option(
    "--visibility", type=click.Choice(["PUBLIC", "DOMAIN", "OWNER_ONLY"]), default="OWNER_ONLY"
)
def upload(file: str, title: str, visibility: str):
    """Upload a csv or Excel file as a Datapane Blob"""
    log.info(f"Uploading {file}")
    r = api.Blob.upload_file(file, title=title, visibility=visibility)
    success_msg(f"Uploaded {click.format_filename(file)} to {r.url}")


@blob.command()
@click.argument("id")
@click.argument("file", type=click.Path())
def download(id: str, file: str):
    """Download blob referenced by ID to FILE"""
    r = api.Blob(id)
    r.download_file(file)
    success_msg(f"Downloaded {r.url} to {click.format_filename(file)}")


@blob.command()
@click.argument("id")
def delete(id: str):
    """Delete a blob"""
    api.Blob(id).delete()
    success_msg(f"Deleted Blob {id}")


@blob.command()
def list():
    """List blobs"""
    print_table(api.Blob.list(), "Blobs")


###############################################################################
# Scripts
@cli.group()
def script():
    """Commands to work with Scripts"""
    ...


@script.command(name="init")
@click.option("--title", default=sc.default_title)
@click.option("--name", default=lambda: os.path.basename(os.getcwd()))
def script_init(title: str, name: str):
    """Initialise a new script project"""
    # NOTE - only supports single hierarchy project dirs
    env = Environment(loader=FileSystemLoader("."))

    def render_file(fname: Path, context: Dict):
        rendered_script = env.get_template(fname.name).render(context)
        fname.write_text(rendered_script)

    # copy the scaffolds into the service
    def copy_scaffold(name: str) -> List[Path]:
        dir_path = sc.get_res_path(os.path.join("scaffold", name))
        copy_tree(dir_path, ".")
        return [Path(x.name) for x in dir_path.iterdir()]

    if sc.DATAPANE_YAML.exists():
        raise ValueError("Found existing project, cancelling")

    name = name.replace("-", "_")
    sc.validate_name(name)
    common_files = copy_scaffold("common")
    stack_files = copy_scaffold("python")

    # run the scripts
    scaffold = dict(name=name, title=title)
    for f in common_files + stack_files:
        if f.exists() and f.is_file():
            render_file(f, dict(scaffold=scaffold))
    success_msg(f"Created dp_script.py for project '{name}', edit as needed and upload")


@script.command()
@click.option("--config", type=click.Path(exists=True))
@click.option("--script", type=click.Path(exists=True))
@click.option("--title")
@click.option(
    "--visibility", type=click.Choice(["PUBLIC", "DOMAIN", "OWNER_ONLY"]), default="OWNER_ONLY"
)
def deploy(title: Optional[str], script: Optional[str], config: Optional[str], visibility: str):
    """Package and deploy a Python script or Jupyter notebook as a Datapane Script bundle"""
    script = script and Path(script)
    config = config and Path(config)
    init_kwargs = dict(visibility=visibility, title=title, script=script, config_file=config)
    kwargs = {k: v for k, v in init_kwargs.items() if v is not None}

    # if not (script or config or sc.DatapaneCfg.exists()):
    #     raise AssertationError(f"Not valid project dir")

    dp_cfg = scripts.DatapaneCfg.create_initial(**kwargs)
    log.debug(f"Packaging and uploading Datapane project {dp_cfg.name}")

    # start the build process
    with click_spinner.spinner(), scripts.build_bundle(dp_cfg) as sdist:

        if DEBUG:
            tf: tarfile.TarFile
            log.debug("Bundle from following files:")
            with tarfile.open(sdist) as tf:
                for n in tf.getnames():
                    log.debug(f"  {n}")

        r: api.Script = api.Script.upload_pkg(sdist, dp_cfg)
        success_msg(f"Uploaded {click.format_filename(str(dp_cfg.script))} to {r.web_url}")


@script.command()
@click.argument("id")
def download(id: str):
    """Download script referenced by ID to FILE"""
    s = api.Script(id)
    fn = s.download_pkg()
    success_msg(f"Downloaded {s.url} to {click.format_filename(str(fn))}")


@script.command()
@click.argument("id")
def delete(id: str):
    """Delete a script"""
    api.Script(id).delete()
    success_msg(f"Deleted Script {id}")


@script.command()
def list():
    """List Scripts"""
    print_table(api.Script.list(), "Scripts")


def process_cmd_param_vals(params: Tuple[str, ...]) -> JDict:
    """Convert a list of k=v to a typed JSON dict"""

    def convert_param_val(x: str) -> t.Union[int, float, str, bool]:
        # TODO - this can be optimised / cleaned-up
        try:
            return int(x)
        except ValueError:
            try:
                return float(x)
            except ValueError:
                try:
                    return bool(strtobool(x))
                except ValueError:
                    return x

    def split_param(xs: Tuple[str]) -> Iterator[t.Tuple[str, str]]:
        err_msg = "'{}', should be name=value"
        for x in xs:
            try:
                k, v = x.split("=", maxsplit=1)
            except ValueError:
                raise click.BadParameter(err_msg.format(x))
            if not k or not v:
                raise click.BadParameter(err_msg.format(x))
            yield (k, v)

    return {k: convert_param_val(v) for (k, v) in split_param(params)}


@script.command()
# @click.option("--clone", help="Clone the report before running.")
@click.option("--parameter", "-p", multiple=True)
@click.option("--cache/--disable-cache", default=True)
@click.option("--wait/--no-wait", default=True)
@click.argument("id")
def run(id: str, parameter: Tuple[str], cache: bool, wait: bool):
    """Run a report"""
    params = process_cmd_param_vals(parameter)
    log.info(f"Running script with parameters {params}")
    script = api.Script(id)
    with api_error_handler("Error running script"):
        r = script.run(parameters=params, cache=cache)
    if wait:
        with click_spinner.spinner():
            while not r.is_complete():
                time.sleep(2)
                r.refresh()
            log.debug(f"Run completed with status {r.status}")
            if r.status == "SUCCESS":
                if r.result:
                    success_msg(f"Script result - '{r.result}'")
                if r.report:
                    report = api.Report(r.report)
                    success_msg(f"Report generated at {report.web_url}")
            else:
                failure_msg(
                    f"Script run failed/cancelled\n{r.error_msg}: {r.error_detail}", do_exit=True
                )

    else:
        success_msg(f"Script run started, view at {script.web_url}")


###############################################################################
# Reports
@cli.group()
def report():
    """Commands to work with Reports"""
    ...


@report.command()
@click.argument("files", type=click.Path(), nargs=-1, required=True)
@click.option(
    "--visibility", type=click.Choice(["PUBLIC", "DOMAIN", "OWNER_ONLY"]), default="OWNER_ONLY"
)
@click.option("--title", default=gen_title)
def create(files: Tuple[str], title: str, visibility: str):
    """Create a Report from the provided FILES"""
    blocks = [api.Asset.upload_file(file=Path(f)) for f in files]
    r = api.Report.create(*blocks, title=title, visibility=visibility)
    success_msg(f"Created Report {r.web_url}")


@report.command()
@click.argument("id")
def delete(id: str):
    """Delete a report"""
    api.Report(id).delete()
    success_msg(f"Deleted Report {id}")


@report.command()
def list():
    """List Reports"""
    print_table(api.Report.list(), "Reports")


@report.command()
@click.argument("id")
@click.option("--filename", default="output.html", type=click.Path())
def render(id: str, filename: str):
    """Render a report to a static file"""
    api.Report(id).render()


#############################################################################
# Variables
@cli.group()
def variable():
    """Commands to work with Variables"""
    ...


@variable.command()
@click.argument("value", required=True, type=click.STRING)
@click.option(
    "--visibility", type=click.Choice(["PUBLIC", "DOMAIN", "OWNER_ONLY"]), default="OWNER_ONLY"
)
def add(value: str, visibility: str):
    """
    Add a variable

    VALUE: value of variable

    --visibility(default=OWNER_ONLY):
    PUBLIC: visibile to everyone,
    Domain: visibile to all authenticated users on your domain,
    OWNER_ONLY: only visibile to you
    """
    res = api.Variable.add(value, visibility)
    success_msg(f"Created variable ID: {res.id}")


@variable.command()
def list():
    """List all variables"""
    print_table(api.Variable.list(), "Variables")


@variable.command()
@click.argument("id", required=True)
@click.option("--show", is_flag=True, help="Print the variable value.")
def get(id, show):
    """Get variable value using variable id"""
    res = api.Variable(id)
    if show:
        print(str(res.value).strip())
    else:
        print_table([{"id": id, "value": res.value, "visibility": res.visibility}], "Variable")


@variable.command()
@click.argument("id", required=True)
def delete(id):
    """Delete a variable using variable id"""
    api.Variable(id).delete()
    success_msg(f"Deleted variable {id}")


@variable.command()
@click.argument("id", required=True)
@click.argument("value", required=True)
@click.option("--visibility", type=click.Choice(["PUBLIC", "DOMAIN", "OWNER_ONLY"]))
def update(id, value, visibility):
    """Update a variable value using variable id

    ID: ID of variable

    VALUE: value of variable

    --visibility:
    PUBLIC: visibile to everyone,
    Domain: visibile to all authenticated users on the domain,
    OWNER_ONLY: only visibile to you
    """
    api.Variable(id).update(value=value, visibility=visibility)
    success_msg(f"Updated Variable {id}")
