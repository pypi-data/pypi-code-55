import os
import platform
import time

import typer

from .installer import PostgresInstaller, Shell, Download
from remo_app.config import REMO_HOME


class WindowsPostgresInstaller(PostgresInstaller):
    def _is_running(self):
        return Shell.call("psql -U postgres -l", show_command=False, show_output=False) == 0

    def _launch(self):
        typer.echo("Launching postgres ...")

        for _ in range(3):
            return_code = Shell.call("pg_ctl start", show_output=False)
            if return_code == 0:
                break
            time.sleep(2)

        if Shell.call("pg_ctl status", show_command=False, show_output=False) != 0:
            typer.echo('ERROR: failed to launch postgres')
            raise typer.Exit()

        typer.echo(
            """
You can stop Postgres server with following command:
$ pg_ctl stop
"""
        )

    def _install(self):
        Shell.call("scoop install postgresql@12.2", show_output=False)
        self._set_env_vars()

    def _create_db_and_user(self, dbname, username, password):
        Shell.call(f"""psql -U postgres -c "create user {username} with encrypted password '{password}';" """, show_output=False)
        Shell.call(f"""psql -U postgres -c "create database {dbname};" """, show_output=False)
        Shell.call(f"""psql -U postgres -c "grant all privileges on database {dbname} to {username};" """, show_output=False)
        return self.db_params(database=dbname, user=username, password=password)

    def _is_installed(self):
        self._set_env_vars()
        return Shell.call("psql --version", show_command=False, show_output=False) == 0

    @staticmethod
    def _set_env_vars():
        postgres_dir = os.path.expandvars('%userprofile%\\scoop\\apps\\postgresql\\12.2\\bin')
        if os.path.exists(postgres_dir) and postgres_dir not in os.environ["PATH"]:
            os.environ["PATH"] = postgres_dir + os.pathsep + os.environ["PATH"]

        pg_data = os.path.expandvars("%userprofile%\\scoop\\apps\\postgresql\\current\\data")
        if os.path.exists(pg_data) and not os.getenv('PGDATA'):
            os.environ["PGDATA"] = pg_data


class LinuxPostgresInstaller(PostgresInstaller):

    def _is_installed(self):
        return Shell.call("psql --version", show_command=False, show_output=False) == 0

    def _install(self):
        Shell.call('sudo apt-get install -y -qq postgresql-10', show_output=False)

    def _is_running(self):
        return Shell.call("service postgresql status", show_command=False, show_output=False) == 0

    def _launch(self):
        typer.echo("Launching postgres ...")
        Shell.call('sudo systemctl start postgresql')

        typer.echo(
            """
You can stop it later with following command:
$ sudo systemctl stop postgresql
"""
        )

    def _create_db_and_user(self, dbname, username, password):
        Shell.call(
            f"""sudo -u postgres psql -c "create user {username} with encrypted password '{password}';" """,
            show_output=False
        )
        Shell.call(f"""sudo -u postgres psql -c "create database {dbname};" """, show_output=False)
        Shell.call(
            f"""sudo -u postgres psql -c "grant all privileges on database {dbname} to {username};" """,
            show_output=False
        )
        return self.db_params(database=dbname, user=username, password=password)


class MacPostgresInstaller(PostgresInstaller):

    def _is_installed(self):
        if Shell.call("postgres --version", show_command=False, show_output=False) == 0:
            return True
        self._add_postgres_to_path()
        return Shell.call("postgres --version", show_command=False, show_output=False) == 0

    def _add_postgres_to_path(self):
        if os.path.exists("/usr/local/opt/postgresql@10/bin"):
            os.environ['PATH'] = f"/usr/local/opt/postgresql@10/bin:{os.getenv('PATH')}"

    def _is_running(self):
        if Shell.call("psql -l", show_command=False, show_output=False) == 0:
            return True
        self._add_postgres_to_path()
        return Shell.call("psql -l", show_command=False, show_output=False) == 0

    def _install(self):
        Shell.call('brew install postgresql@10', show_output=False)
        shell_exe_path = os.getenv('SHELL')
        shell_name = os.path.basename(shell_exe_path)
        shell_rc_path = os.path.expanduser(f'~/.{shell_name}rc')
        Shell.call(f"""echo 'export PATH="/usr/local/opt/postgresql@10/bin:$PATH"' >> {shell_rc_path}""")
        self._add_postgres_to_path()

    def _launch(self):
        postgres_exe_path = Shell.call_output("which postgres", show_command=False)
        postgres_dir = os.path.dirname(os.path.dirname(postgres_exe_path))
        files = list(filter(lambda name: name.startswith('homebrew'), os.listdir(postgres_dir)))
        if not files:
            typer.echo("Failed to launch postgres server, please start it manually.")
            raise typer.Exit()

        homebrew_mxcl = os.path.join(postgres_dir, files[0])
        typer.echo("Launching postgres ...")
        Shell.call(f'launchctl load {homebrew_mxcl}')

        typer.echo(
            f"""
You can stop it later with following command:
$ launchctl unload {homebrew_mxcl}
"""
        )

        tries = 5
        while not self._is_running() and tries > 0:
            time.sleep(1)
            tries -= 1
        if not self._is_running():
            typer.echo("Failed to launch postgres")
            raise typer.Exit()

    def _create_db_and_user(self, dbname, username, password):
        Shell.call('createdb $USER', show_output=False)
        Shell.call(f"""psql -c "create user {username} with encrypted password '{password}';" """, show_output=False)
        Shell.call(f'createdb {dbname} -O {username}', show_output=False)
        return self.db_params(database=dbname, user=username, password=password)


def get_instance() -> PostgresInstaller:
    installer = {
        'Windows': WindowsPostgresInstaller,
        'Linux': LinuxPostgresInstaller,
        'Darwin': MacPostgresInstaller,
    }.get(platform.system())

    if not installer:
        typer.echo(f'WARNING: current operation system - {platform.system()}, is not supported.')
        raise typer.Exit()

    return installer()
