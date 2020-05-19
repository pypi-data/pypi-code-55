import os
import typer
import platform

from . import postgres
from .db import migrate, is_database_uptodate
from .installer import get_instance
from .config import create_config, create_or_update_user
from .runtime import install_cert_path, setup_vips
from .server import run_server
from .checker import check_installation_requirements, check_runtime_requirements
from remo_app import __version__
from remo_app.config.config import Config

app = typer.Typer(add_completion=False, add_help_option=False)


def make_db_url(db):
    engine = db.get('engine')
    if engine != 'postgres':
        typer.echo(f"""
ERROR: Not supported DB engine - {engine}.

Please use 'postgres'.
""")
        typer.Exit()

    host, name, password, port, user = db.get('host'), db.get('name'), db.get('password'), db.get('port'), db.get('user')
    return f'{engine}://{user}:{password}@{host}:{port}/{name}'


def set_db_url(url):
    os.environ['DATABASE_URL'] = url


@app.command(add_help_option=False, options_metavar='')
def init():
    typer.echo('Initiailizing Remo:')

    installer = get_instance()
    dependencies = installer.dependencies()
    if dependencies:
        fmt_deps_list = '\n   * '.join(dependencies)
        msg = f"""
This will download and install the following packages as needed: \n   * {fmt_deps_list}
Do you want to continue?"""
        if not typer.confirm(msg, default=True):
            typer.echo('\nInstallation aborted.')
            raise typer.Exit()

    db_config = installer.install(postgres=postgres.get_instance())
    db_url = make_db_url(db_config)
    set_db_url(db_url)
    migrate()

    config = create_config(db_url)
    if config.viewer == 'electron':
        installer.download_electron_app()

    typer.echo("""

    (\\(\\
    (>':')  Remo successfully initiliazed.
    You can launch remo using the command 'python -m remo_app'
    """)


@app.command(add_help_option=False, options_metavar='')
def run_jobs():
    from remo_app.remo.use_cases import jobs
    print('Remo running jobs:')
    for job in jobs.all_jobs:
        job()


@app.command(add_help_option=False, options_metavar='')
def debug():
    config = Config.load()
    run_server(config, debug=True)


def version_callback(value: bool):
    if value:
        typer.echo(f"Remo: v{__version__}")
        raise typer.Exit()


def help_callback(value: bool):
    if value:
        typer.echo(f"""
Remo: v{__version__}

Commands:
  (no command)  - starts server
  init          - initializes REMO_HOME folder
  run-jobs      - runs periodic jobs

  --version     - shows remo version
  --help        - shows help info

""")
        raise typer.Exit()


@app.callback(invoke_without_command=True, options_metavar='', subcommand_metavar='')
def main(
    ctx: typer.Context,
    version: bool = typer.Option(None, "--version", callback=version_callback, is_eager=True),
    help: bool = typer.Option(None, "--help", callback=help_callback, is_eager=True),
):
    os.environ["DJANGO_SETTINGS_MODULE"] = "remo_app.config.standalone.settings"
    typer.echo(logo)

    # check_installation_requirements()
    install_cert_path()

    if ctx.invoked_subcommand != 'init':
        if not Config.is_exists():
            typer.echo("""
ERROR: Remo not fully initialized, config file was not found at REMO_HOME.

Please run: python -m remo_app init
        """)
            raise typer.Exit()

        setup_vips()

        config = Config.load()
        if not config.db_url:
            typer.echo("""
         You installed a new version of Remo that uses PostgreSQL database for faster processing.
         To use it, you need to run 'python -m remo_app init'.
WARNING: Your current data in SQLite database will be lost.

To proceed, just run: python -m remo_app init
            """)
            raise typer.Exit()

        set_db_url(config.db_url)
        check_runtime_requirements(config.parse_db_params())

        from remo_app.config.standalone.wsgi import application
        if not is_database_uptodate():
            migrate()

        name, email, password = create_or_update_user(config.user_name, config.user_email, config.user_password)
        config.update(user_name=name, user_email=email, user_password=password)
        config.save()

    if ctx.invoked_subcommand is None:
        run_server(config)


logo = (f"""
===============================================
    (\\(\\
    (>':')  Remo: v{__version__}
===============================================
Python: {platform.python_version()}, {platform.platform()}
""")
