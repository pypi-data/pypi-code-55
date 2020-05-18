import glob
import os
import pathlib
import random
import shutil
import sys
import time
from datetime import datetime
from pathlib import PurePath

from cement import Controller, ex
from cement.utils.version import get_version_banner

import yaml

from ..core.version import get_version

VERSION_BANNER = """
portable, reusable, self-managed salt projects %s
%s
""" % (
    get_version(),
    get_version_banner(),
)

PROJECT_ARG = (["project"], {"help": "the salt packet project name", "action": "store"})
PROJECT_ARG_OPT = (
    ["-p", "--project"],
    {"help": "the salt packet project name", "action": "store", "required": False},
)


class Base(Controller):
    class Meta:
        label = "base"

        # text displayed at the top of --help output
        description = "portable, reusable, self-managed salt projects"

        # text displayed at the bottom of --help output
        epilog = "Usage: salt-packets add git@repo.url"

        # controller level arguments. ex: 'salt-packets --version'
        arguments = [
            ### add a version banner
            (["-v", "--version"], {"action": "version", "version": VERSION_BANNER})
        ]

    def _default(self):
        """Default action if no sub-command is passed."""

        self.app.args.print_help()

    @ex(
        arguments=[
            (["repo_url"], {"help": "the url of the salt packet", "action": "store"}),
            (
                ["-i", "--minion-id"],
                {
                    "help": "set the minion id incase a packet requires it",
                    "action": "store",
                    "dest": "minion_id",
                },
            ),
            (
                ["-e", "--env"],
                {
                    "help": "set an environment variable with --env=VAR=value",
                    "action": "append",
                    "dest": "argv_env",
                },
            ),
        ]
    )
    def add(self):
        """Example sub-command."""
        env_list = [e.split("=") for e in (self.app.pargs.argv_env or [])]
        ENV = {k.upper(): v for k, v in env_list}
        self.app.utils.add_packet(
            self.app.pargs.repo_url, self.app.pargs.minion_id, extra_env=ENV
        )

    @ex(arguments=[])
    def upgrade(self):
        pip = "git+ssh://git@code.netprophet.tech/netp/salt-packets"
        self.app.log.info(f"Updating pip from remote {pip}")
        # Execvp will replace this process with the sidechain
        os.execvp("pip3", ["pip3", "install", "--upgrade", pip])

    @ex(arguments=[])
    def ls(self):
        for p in self.app.utils.list_projects():
            print(p)

    @ex(arguments=[PROJECT_ARG])
    def environment(self):
        config = self.app.utils.get_config(self.app.pargs.project)
        print()
        print("Packet Profile: (%s)" % config["packet_path"])
        print("==================")
        yaml.dump(config["packet"], sys.stdout)
        print()
        print("System: (%s)" % config["system_path"])
        print("==================")
        yaml.dump(config["system"], sys.stdout)
        print()
        print("Installation Profile Environment: (%s)" % config["profile_path"])
        print("==================")
        yaml.dump(config["profile"].get("environment", {}), sys.stdout)
        print()
        print("Final Combined Environment:")
        print("==================")
        yaml.dump(config["environment"], sys.stdout)

    @ex(
        arguments=[
            PROJECT_ARG_OPT,
            (
                ("--no-compile", "-C"),
                {
                    "help": "don't recompile the .cache directory before highstate",
                    "action": "store_false",
                    "dest": "compile",
                },
            ),
        ]
    )
    def highstate(self):
        self.app.utils.highstate(
            self.app.pargs.project, compile=self.app.pargs.compile)

    @ex(arguments=[PROJECT_ARG_OPT])
    def compile(self):
        self.app.utils.compile(self.app.pargs.project)

    @ex(arguments=[PROJECT_ARG_OPT])
    def pull(self):
        if self.app.pargs.project:
            self.app.log.info(self.app.utils.git_pull(self.app.pargs.project).stdout)
        else:
            for project in self.app.utils.list_projects():
                self.app.log.info("Pulling project %s" % project)
                self.app.log.info(self.app.utils.git_pull(project).stdout)

    @ex(arguments=[PROJECT_ARG])
    def install_cronjob(self):
        self.app.utils.create_cronjob(self.app.pargs.project, "0 18 * * *")

    @ex(arguments=[PROJECT_ARG])
    def hard_pull(self):
        self.app.utils.git_hard_pull(self.app.pargs.project)

    @ex(arguments=[PROJECT_ARG])
    def update(self):
        project = self.app.pargs.project
        self.app.utils.git_hard_pull(project)
        self.app.utils.highstate(project)
