import shutil
import os
import subprocess
import sys
import time

import requests
import platform
import json

import typer

from remo_app.config import REMO_HOME


class Download:
    def __init__(self, url, path, text, chunk_size=1024 * 1024):
        dir_path, filename = os.path.split(path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        typer.echo(text)
        if self.is_tool_exists('aria2c'):
            cmd = f'aria2c -x4 -d "{dir_path}" -o "{filename}" "{url}"'
            Shell.call(cmd, show_output=False)
            if os.path.exists(path):
                return

        text = 'Progress: '
        print(text, end='\r')

        with requests.get(url, stream=True) as resp:
            total_size = self.content_size(resp.headers)
            if total_size == -1:
                total_size = 60 * 1024 * 1024

        with open(path, 'wb') as f:
            with requests.get(url, stream=True) as resp:
                downloaded = 0
                for chunk in resp.iter_content(chunk_size):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)

                        percentage = round(downloaded / total_size * 100)
                        done = int(percentage / 2)
                        rest = 50 - done
                        bar = '[{}{}]'.format('#' * done, ' ' * rest)
                        print('{} {} {}%  '.format(text, bar, percentage), end='\r')
        print('{} [{}] {}%  '.format(text, '#' * 50, 100))

    @staticmethod
    def content_size(headers):
        try:
            return int(headers.get('content-length'))
        except (KeyError, TypeError):
            return -1

    @staticmethod
    def is_tool_exists(tool):
        return bool(shutil.which(tool))


class Shell:
    @staticmethod
    def call(cmd: str, show_command=True, show_output=True):
        if show_command:
            typer.echo(f"$ {cmd}")
        kwargs = {'shell': True}
        if not show_output:
            kwargs['stdout'] = subprocess.DEVNULL
            kwargs['stderr'] = subprocess.DEVNULL
        return subprocess.call(cmd, **kwargs)

    @staticmethod
    def call_output(cmd: str, show_command=True):
        if show_command:
            typer.echo(f"$ {cmd}")
        output = subprocess.check_output(cmd.split())
        return output.decode("utf-8").strip()


def _get_pip_executable():
    python_dir = os.path.dirname(sys.executable)
    files = os.listdir(python_dir)
    for pip in ['pip', 'pip.exe']:
        if pip in files:
            return os.path.join(python_dir, pip)

    if 'Scripts' in files:
        scripts_dir = os.path.join(python_dir, 'Scripts')
        pip = 'pip.exe'
        if pip in os.listdir(scripts_dir):
            return os.path.join(scripts_dir, pip)

    typer.echo('ERROR: pip was not found')
    raise typer.Exit()


class Pip:
    executable = _get_pip_executable()

    @staticmethod
    def run_command(command, package):
        if Shell.call(f'"{Pip.executable}" {command} {package}', show_output=False) != 0:
            typer.echo(f'ERROR: pip failed to {command} {package}')
            raise typer.Exit()

    @staticmethod
    def install(package):
        Pip.run_command('install', package)

    @staticmethod
    def uninstall(package):
        Pip.run_command('uninstall', package)


class PostgresInstaller:
    username = 'remo'
    dbname = 'remo'
    userpass = 'remo'

    @staticmethod
    def _install_psycopg2():
        Pip.install('psycopg2')

    @staticmethod
    def _is_installed_psycopg2():
        try:
            import psycopg2
        except Exception:
            return False
        return True

    def install(self):
        if not self._is_installed():
            self._install()

        if not self._is_installed_psycopg2():
            self._install_psycopg2()

        if not self._is_running():
            self._launch()

        db = self._create_db_and_user(self.dbname, self.username, self.userpass)
        db_params = json.dumps(db, indent=2, sort_keys=True)
        if not self.can_connect(self.dbname, self.username, self.userpass):
            typer.echo(
                f"""
Failed connect to database:
{db_params}
        """
            )
            raise typer.Exit()

        typer.echo(
            f"""
Postgres database connection parameters:
{db_params}
        """
        )
        return db

    def on_start_check(self, db_params):
        if self.can_connect(**db_params):
            return

        if not self._is_installed():
            typer.echo(
                """
ERROR: postgres not installed

Please run: python -m remo_app init
"""
            )
            raise typer.Exit()

        if not self._is_running():
            self._launch()

        if not self._is_installed_psycopg2():
            self._install_psycopg2()

        if not self.can_connect(**db_params):
            typer.echo(
                """
ERROR: failed connect to database. Please check `db_url` value in config file.
            """
            )
            raise typer.Exit()

    @staticmethod
    def db_params(database='', user='', password='', host='localhost', port='5432'):
        return {
            'engine': 'postgres',
            'user': user,
            'password': password,
            'host': host,
            'port': port,
            'name': database,
        }

    @staticmethod
    def can_connect(database='', user='', password='', host='localhost', port='5432', **kwargs):
        try:
            import psycopg2
            conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
        except Exception:
            return False
        conn.close()
        return True

    def _is_installed(self):
        raise NotImplementedError()

    def _is_running(self):
        raise NotImplementedError()

    def _launch(self):
        raise NotImplementedError()

    def _install(self):
        raise NotImplementedError()

    def _create_db_and_user(self, dbname, username, password):
        raise NotImplementedError()

    def _drop_db(self, database: str):
        raise NotImplementedError()

    def restart(self):
        raise NotImplementedError()

    def drop_database(self, db_params):
        self.restart()
        for _ in range(5):
            if self.can_connect(**db_params):
                break
            time.sleep(1)

        if self.can_connect(**db_params):
            self._drop_db(db_params.get('database'))
        else:
            typer.echo(
                """
ERROR: failed connect to database. Please check `db_url` value in config file.
            """
            )
            raise typer.Exit()


def stage(msg: str, marker='[-]', separator='\n{}\n'.format('-' * 50)):
    typer.echo(f'{separator}{marker} {msg}')


class OSInstaller:
    sqlite_url = ''
    sqlite_exe = ''

    def install(self, postgres: PostgresInstaller):
        self.install_os_specific_tools()

        self.drop_electron_files()
        self.setup_remo_home()

        stage('Installing vips lib')
        self.install_vips()

        stage('Installing postgres')
        return postgres.install()

    def uninstall(self, postgres: PostgresInstaller, db_params):
        stage('Deleting database')
        postgres.drop_database(db_params)

        stage('Deleting remo folder')
        self.delete_remo_home_folder()

    def install_os_specific_tools(self):
        pass

    def install_vips(self):
        raise NotImplementedError()

    def install_sqlite(self):
        if self.is_tool_exists('sqlite3'):
            return

        path = str(os.path.join(REMO_HOME, 'sqlite'))
        if not os.path.exists(path):
            os.makedirs(path)

        archive_path = os.path.join(path, 'sqlite.zip')
        if not os.path.exists(archive_path):
            Download(self.sqlite_url, archive_path, '* Downloading sqlite:')

            bin_path = str(os.path.join(path, 'bin'))
            if not os.path.exists(bin_path):
                os.makedirs(bin_path)
            typer.echo('* Extract sqlite')
            self.unzip(archive_path, bin_path)

        if os.path.exists(self.sqlite_exe):
            os.environ["PATH"] = os.path.dirname(self.sqlite_exe) + os.pathsep + os.environ["PATH"]
        else:
            typer.echo(
                'WARNING: automatic installation for SQLite failed. Please try to install it manually. \n'
                'See instructions here https://www.sqlitetutorial.net/download-install-sqlite/'
            )
            raise typer.Exit()

    def unzip(self, archive_path, extract_path):
        raise NotImplementedError()

    @staticmethod
    def is_tool_exists(tool):
        return bool(shutil.which(tool))

    def download_electron_app(self):
        app_path = str(os.path.join(REMO_HOME, 'app'))
        if os.path.exists(app_path) and os.listdir(app_path):
            # skip if dir not empty
            return

        stage('Installing electron app')

        archive_path = os.path.join(REMO_HOME, 'app.zip')
        if not os.path.exists(archive_path):
            url = 'https://app.remo.ai/download/latest?platform={}'.format(platform.system())
            Download(url, archive_path, '* Downloading remo app:')

        typer.echo('* Extract remo app')
        self.unzip(archive_path, app_path)

    @staticmethod
    def drop_electron_files():
        app_path = str(os.path.join(REMO_HOME, 'app'))
        if os.path.exists(app_path):
            shutil.rmtree(app_path, ignore_errors=True)

        archive_path = os.path.join(REMO_HOME, 'app.zip')
        if os.path.exists(archive_path):
            os.remove(archive_path)

    @staticmethod
    def setup_remo_home():
        if not os.path.exists(REMO_HOME):
            typer.echo('Installing Remo to dir: {}'.format(REMO_HOME))
            os.makedirs(REMO_HOME)

    def dependencies(self) -> list:
        return []

    def delete_remo_home_folder(self):
        if os.path.exists(REMO_HOME):
            shutil.rmtree(REMO_HOME, ignore_errors=True)


class WindowsInstaller(OSInstaller):
    sqlite_url = 'https://www.sqlite.org/2020/sqlite-tools-win32-x86-3310100.zip'
    sqlite_exe = str(
        os.path.join(REMO_HOME, 'sqlite', 'bin', 'sqlite-tools-win32-x86-3310100', 'sqlite3.exe')
    )

    def dependencies(self) -> list:
        return ['vips', 'postgres', 'scoop', 'git', 'unzip', 'aria2']

    def install_os_specific_tools(self):
        self._add_scoop_to_path()
        if not self.is_tool_exists('scoop'):
            stage('Installing scoop')

            Shell.call("""powershell.exe -Command "iwr -useb get.scoop.sh | iex" """, show_output=False)
            self._add_scoop_to_path()

        if not self.is_tool_exists('git'):
            Shell.call("scoop install git", show_output=False)

        if not self.is_tool_exists('aria2c'):
            Shell.call("scoop install aria2", show_output=False)

        if not self.is_tool_exists('unzip'):
            Shell.call("scoop install unzip", show_output=False)

    @staticmethod
    def _add_scoop_to_path():
        scoop_dir = os.path.expandvars('%userprofile%\\scoop\\shims')
        if os.path.exists(scoop_dir) and scoop_dir not in os.environ["PATH"]:
            os.environ["PATH"] = scoop_dir + os.pathsep + os.environ["PATH"]

    def install_vips(self):
        vips_bin_path = str(os.path.join(REMO_HOME, 'libs', 'vips', 'vips-dev-8.8', 'bin'))
        if not os.path.exists(vips_bin_path):
            self.download_vips()
        os.environ["PATH"] = vips_bin_path + os.pathsep + os.environ["PATH"]

    def download_vips(self):
        libs_path = str(os.path.join(REMO_HOME, 'libs'))
        archive_path = os.path.join(libs_path, 'vips.zip')
        if not os.path.exists(archive_path):
            url = 'https://github.com/libvips/libvips/releases/download/v8.8.4/vips-dev-w64-web-8.8.4.zip'
            Download(url, archive_path, '* Downloading vips lib:')

            vips_lib_path = str(os.path.join(libs_path, 'vips'))
            typer.echo('* Extract vips lib')
            self.unzip(archive_path, vips_lib_path)

    def unzip(self, archive_path, extract_path):
        if not os.path.exists(extract_path):
            os.makedirs(extract_path)

        if self.is_tool_exists('7z'):
            Shell.call(f'7z x "{archive_path}" -o"{extract_path}"', show_output=False)
            return

        if self.is_tool_exists('unzip'):
            Shell.call(f'unzip -q "{archive_path}" -d "{extract_path}"', show_output=False)
            return

        Shell.call(
            """powershell.exe -Command "Expand-Archive '{}' '{}'" """.format(archive_path, extract_path),
            show_output=False
        )


class MacInstaller(OSInstaller):
    sqlite_url = 'https://www.sqlite.org/2020/sqlite-tools-osx-x86-3310100.zip'
    sqlite_exe = str(os.path.join(REMO_HOME, 'sqlite', 'bin', 'sqlite-tools-osx-x86-3310100', 'sqlite3'))

    def dependencies(self) -> list:
        return ['vips', 'postgres', 'brew', 'git', 'unzip']

    def install_os_specific_tools(self):
        if Shell.call("brew --version", show_command=False, show_output=False) != 0:
            typer.echo(
                """
Please install homebrew - package manager for macOS. See: https://brew.sh

Paste that in a macOS Terminal:
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"

After installation complete, re-run: python -m remo_app init
"""
            )
            raise typer.Exit()

    def install_vips(self):
        if Shell.call("vips -v", show_command=False, show_output=False) != 0:
            Shell.call('brew install vips', show_output=False)

    def unzip(self, archive_path, extract_path):
        if not os.path.exists(extract_path):
            os.makedirs(extract_path)
        Shell.call('unzip -q "{}" -d "{}"'.format(archive_path, extract_path), show_output=False)


class LinuxInstaller(OSInstaller):
    sqlite_url = 'https://www.sqlite.org/2020/sqlite-tools-linux-x86-3310100.zip'
    sqlite_exe = str(os.path.join(REMO_HOME, 'sqlite', 'bin', 'sqlite-tools-linux-x86-3310100', 'sqlite3'))

    def dependencies(self) -> list:
        return ['vips', 'postgres', 'openssl', 'apt-transport-https', 'ca-certificates', 'unzip', 'libpq-dev', 'python3-dev', 'unzip']

    def install_os_specific_tools(self):
        Shell.call("sudo apt-get update -qq", show_output=False)
        Shell.call("sudo apt-get install -y -qq openssl", show_output=False)
        Shell.call(
            "sudo apt-get install -y -qq apt-transport-https ca-certificates unzip libpq-dev python3-dev",
            show_output=False
        )

    def install_vips(self):
        if Shell.call("vips -v", show_command=False, show_output=False) != 0:
            Shell.call('sudo apt-get install -y -qq libvips-dev', show_output=False)

    def unzip(self, archive_path, extract_path):
        if not os.path.exists(extract_path):
            os.makedirs(extract_path)
        Shell.call('unzip -q "{}" -d "{}"'.format(archive_path, extract_path), show_output=False)


def get_instance() -> OSInstaller:
    installer = {'Windows': WindowsInstaller, 'Linux': LinuxInstaller, 'Darwin': MacInstaller}.get(
        platform.system()
    )

    if not installer:
        typer.echo(f'WARNING: current operation system - {platform.system()}, is not supported.')
        raise typer.Exit()

    arch, _ = platform.architecture()
    if arch != '64bit':
        typer.echo(f'WARNING: current system architecture {arch}, is not supported.')
        raise typer.Exit()

    return installer()
