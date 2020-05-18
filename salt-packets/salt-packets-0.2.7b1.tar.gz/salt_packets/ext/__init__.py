import logging
import os
import pathlib
import random
import shutil
import subprocess
import sys
import time
import urllib.parse
from collections import Counter
from copy import deepcopy
from pathlib import PurePath

import requests
from pyfiglet import Figlet

import yaml
import re

from colored import attr, fg
from salt_packets.core.exc import SaltPacketsError



def fig(text, font="slant"):
    return Figlet(font=font).renderText(text)



def expandvars(text, default=None, skip_escaped=False, data=None):
    """Expand environment variables of form $var and ${var}.
       If parameter 'skip_escaped' is True, all escaped variable references
       (i.e. preceded by backslashes) are skipped.
       Unknown variables are set to 'default'. If 'default' is None,
       they are left unchanged.
       If data is not specified, os.environ is used
    """
    def replace_var(m):
        return str((data or os.environ).get(m.group(2) or m.group(1), m.group(0) if default is None else default))
    reVar = (r'(?<!\\)' if skip_escaped else '') + r'\$(\w+|\{([^}]*)\})'
    return re.sub(reVar, replace_var, text)

CHECK_SUCCESS = f"{fg('green')}✓{attr('reset')}"
CROSS_FAIL = f"{fg('red')}✗{attr('reset')}"
PACKETS = fg("blue") + fig("PACKETS", "block") + attr("reset")
SEP = "*" * 27 # 27 looks the best for us

def inject_jinja_globals(outputs):
    return {
        "RESET": attr("reset"),
        "ORANGE": fg("orange_1"),
        "NETPROPHET": fg("orange_1") + fig("net-prophet") + attr("reset"),
        "BLUE": fg("blue"),
        "PACKETS": PACKETS,
        "CHECK_SUCCESS": CHECK_SUCCESS,
        "CROSS_FAIL": CROSS_FAIL,
        "OUTPUTS": outputs,
    }


class SaltPacketsSetupHelper:
    def __init__(self, app):
        self.app = app

    @classmethod
    def attach(cls, name, app):
        setattr(app, name, cls(app))

    @property
    def config(self):
        return self.app.config


class UtilsHelper(SaltPacketsSetupHelper):
    def env_or_arg(self, arg_name, env_name, or_path=None, required=False):
        # pargs has default value of None if argument not provided
        value = getattr(self.app.pargs, arg_name)

        if value is None:
            if env_name in os.environ:
                value = os.environ[env_name]
                self.app.log.info(
                    f"--{arg_name} not specified, using environ[{env_name}]: {value}"
                )

            elif or_path and os.path.exists(self.app.utils.path(or_path)):
                with open(self.app.utils.path(or_path), "r") as variable_file:
                    value = variable_file.read().strip()
                    self.app.log.info(
                        f"--{arg_name} not specified, using file {or_path}: {value}"
                    )

        if required and value is None:
            self.app.log.error(
                f"You must specify either --{arg_name} or set {env_name} in your environment"
            )
            raise SaltPacketsError(
                f"You must specify either --{arg_name} or set {env_name} in your environment"
            )

        return value

    def workdir(self, *extra_path):
        return os.path.realpath(
            os.path.expanduser(
                os.path.join(self.config["salt-packets"]["workdir"], *extra_path)
            )
        )

    def path(self, *extra_paths):
        return self.workdir(
            *[extra_path % self.config["salt-packets"] for extra_path in extra_paths]
        )

    def list_projects(self):
        return self.yaml_silent(self.installed_path()) or []

    def raw_exec(self, *cmd, quiet=True):  # pylint: disable=no-self-use
        """This provides subprocess functionality via the attached UtilsHelper instance.

        Pylint `no-self-use` should be disabled on this method to prevent that warning.
        This could be a staticmethod, but would make invoking it more cumbersome than it already is
        """
        log = quiet and self.app.log.debug or self.app.log.info
        log(SEP)
        log("executing")
        log("> " + " ".join(cmd))
        log(SEP)

        env = os.environ.copy()
        if os.path.exists(".env"):
            with open(".env", "r") as fh:
                for line in fh.readlines():
                    key, *rest = line.strip().split("=")
                    env[key] = "=".join(rest)

        if quiet:
            return subprocess.run(
                cmd,
                encoding="utf-8",
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE,
                env=env,
            )
        else:
            return subprocess.run(
                cmd, encoding="utf-8", stderr=sys.stderr, stdout=sys.stdout, env=env
            )

    def replace_with_call(self, *args, quiet=False):
        log = quiet and self.app.log.debug or self.app.log.info
        log()
        log(SEP)
        log("replacing process")
        log("> " + " ".join(args))
        log(SEP)
        env = os.environ.copy()
        with open(".env", "r") as fh:
            for line in fh.readlines():
                key, *rest = line.strip().split("=")
                env[key] = "=".join(rest)
        os.environ.update(env)

        # this return is a funny joke, get it?
        # nope, and you never will
        return os.execvp(args[0], args)

    def download_file(self, destination, url):
        self.app.log.debug(f"Downloading: {destination} from {url}")
        open(destination, "wb+").write(requests.get(url).content)
    
    def installed_path(self):
        return self.workdir('installed.yml')

    def get_config(self, project=None):
        workdir = self.app.config.get("salt-packets", "workdir")
        user = self.app.config.get("salt-packets", "user")
        uid = self.app.config.get("salt-packets", "uid")
        project_path = project and os.path.join(workdir, project)
        profiles_path = os.path.join(workdir, ".profiles")

        packet_path = project and os.path.join(project_path, "salt-packet.yml")
        packet = project and self.yaml_silent(packet_path)

        top_path = project and os.path.join(
            project_path, packet.get("topfile", "top.sls")
        )
        topfile = project and self.yaml_silent(top_path)

        profile_path = project and os.path.join(profiles_path, project)
        profile = project and self.yaml_silent(profile_path)

        system_path = self.app.config.get("salt-packets", "system_path")
        system = self.yaml_silent(system_path)

        if packet:
            environment = {env: os.environ.get(env.upper(),
                                               profile.get('environment', {}).get(env.upper()))
                           for env in packet.get("shell_environment", [])}
            environment.update(packet.get("environment", {}).copy())
        else:
            environment = {}
            
        environment.update(system.get("environment", {}))
        environment.update(profile and profile.get("environment", {}) or {})
        environment["PROJECT"] = project
        environment["SALT_PACKETS_DIR"] = workdir
        environment["PROJECT_PATH"] = project_path
        environment["PACKET_PATH"] = packet_path

        return {
            "workdir": workdir,
            "project": project,
            "project_path": project_path,
            "packet_path": packet_path,
            "packet": packet,
            "top_path": top_path,
            "topfile": topfile,
            "profile": profile,
            "profile_path": profile_path,
            "profiles_path": profiles_path,
            "cache_path": self.workdir(".cache"),
            "cronjob_path": "/etc/cron.d/salt-packet-%s" % project,
            "system_path": system_path,
            "system": system,
            "environment": environment,
            "user": user,
            "uid": uid,
        }

    def yaml_silent(self, fn):
        try:
            return yaml.safe_load(open(fn, "r"))
        except FileNotFoundError:
            return {}

    def salt_call(self, config, *args, replace=False, quiet=False):
        if quiet:
            args = list(args) + [
                "--out",
                "json",
                "--out-file",
                "/var/log/salt-packet",
            ]
        if config['profile'] and config['profile']['minion_id']:
            args = list(args) + ['--id=%s'%config['profile']['minion_id'],]


        command = [
            "salt-call",
            "--local",
            "--file-root=%s" % config["cache_path"],
            *args,
        ]

        if config['uid'] != 0: command = ['sudo', ] + command
        if replace:
            return self.replace_with_call(*command)
        else:
            return self.raw_exec(*command, quiet=quiet)

    def influx_client(self, config):
        from influxdb import InfluxDBClient

        if not "INFLUX_HOST" in config["environment"]:
            return None
        return InfluxDBClient(
            config["environment"]["INFLUX_HOST"],
            config["environment"].get("INFLUX_PORT", 8086),
            config["environment"].get("INFLUX_USER", ""),
            config["environment"].get("INFLUX_PASS", ""),
            config["environment"].get("INFLUX_DB", "influxdb"),
        )

    def influx_packet(self, config, measure, value):
        tags = {"host": config["environment"]["HOSTNAME"], "project": config["project"]}

        return {
            "measurement": measure,
            "tags": tags,
            "fields": isinstance(value, dict) and value or {"value": value},
        }

    def influx_count_one(self, config, measure, value):
        self.influx_count_many(config, {measure: value})

    def influx_count_many(self, config, data):
        client = self.influx_client(config)
        if client:
            client.write_points(
                [
                    self.influx_packet(config, measure, value)
                    for measure, value in data.items()
                ]
            )

    def compile(self, project=None):
        if not project:
            self.app.log.info("Compiling projects...")
        else:
            self.app.log.info("Compiling %s..."%project)

        config = self.get_config()

        if os.path.exists(config["cache_path"]):
            shutil.rmtree(config["cache_path"])

        os.makedirs(config["cache_path"], exist_ok=True)

        all_states = []

        for project in (project and [project,] or self.app.utils.list_projects()):
            config = self.get_config(project)
            self.app.log.info("  + %s" % project)
            self.app.log.debug(
                "    copying %s to %s" % (config["project_path"], config["cache_path"])
            )
            shutil.copytree(
                config["project_path"],
                os.path.join(config["cache_path"], config["project"]),
                ignore=lambda src, names: [name for name in names if name.endswith('.git')],
            )
            sls = [
                os.path.join(parent, fn)
                for parent, dirs, fns in os.walk(config["cache_path"])
                for fn in fns
                if fn.endswith(".sls")
            ]
            for fn in sls:
                with open(fn, 'r') as fh:
                    contents = fh.read()
                contents = expandvars(contents, data=config['environment'])
                with open(fn, 'w') as fh:
                    fh.write(contents)

            topfile = self.app.utils.yaml_silent(config['top_path'])
            
            for key, states in topfile["base"].items():
                for state in states:
                    if PurePath(config['profile']['minion_id']).match(key):
                        all_states.append("%s.%s" % (config["project"], state))

        self.app.log.debug("Building top.sls...")
        with open(os.path.join(config["cache_path"], "top.sls"), "w+") as fh:
            yaml.dump({"base": {"*": all_states}}, fh)

    def highstate(self, project=None, compile=True):
        if compile:
            self.compile(project)
        config = self.get_config(project)

        sudo = config['uid'] != 0
        
        self.app.log.info("")
        self.app.log.info(SEP)
        self.app.log.info("Running highstate (%s sudo)"%(sudo and 'w/' or 'w/o'))
        self.app.log.info(SEP)
        start = time.time()
        self.salt_call(config, "state.highstate", quiet=True)
        try:
            output = self.yaml_silent("/var/log/salt-packet")["local"]
            success = [key for key, o in output.items() if o["result"] == True]
            failures = [key for key, o in output.items() if o["result"] != True]
        except:
            print("Unable to read salt-packet output:")
            with open("/var/log/salt-packet", 'r') as fh:
                print(fh.read())
            sys.exit(1)

        
        self.app.log.info("%s states applied" % len(output))
        self.app.log.info("%s succeeded" % len(success))
        self.app.log.info("%ss elapsed" % (int((time.time() - start) * 100) / 100))
        timing = Counter()
        for p in (project and [project,] or self.list_projects()):
            for name, item in output.items():
                if item['__sls__'].startswith(p):
                    timing[p] += item['duration']

            self.app.log.info("  -> %ss %s"%(int(timing[p])/1000, p))
            for name, item in output.items():
                if item['__sls__'].startswith(p):
                    self.app.log.debug("    + %ss %s"%(int(item['duration'])/1000, name))
            

        if not failures:
            self.app.log.info("No failures")
        else:
            self.app.log.warning("%s failures" % len(failures))
        for failure in failures:
            _type, name, command, action = failure.split('_|-')
            info = output[failure]
            self.app.log.error('in %s: state: %s\n> %s\n%s'%(info['__sls__'],name,command,info['comment']))
        self.influx_count_many(
            config,
            {
                "highstate": {
                    "executions": 1,
                    "states": len(output),
                    "succeeded": len(success),
                    "failed": len(output) - len(success),
                }
            },
        )


    def add_packet(self, repo_url, minion_id=None, extra_env=None):
        project = repo_url.split("/")[-1]

        workdir = self.app.config.get("salt-packets", "workdir")
        user = self.app.config.get("salt-packets", "user")
        uid = self.app.config.get("salt-packets", "uid")

        profiles_path = os.path.join(workdir, ".profiles")
        profile_path = os.path.join(profiles_path, project)
        project_path = os.path.join(workdir, project)
        pathlib.Path(profiles_path).mkdir(parents=True, exist_ok=True)
        pathlib.Path(project_path).mkdir(parents=True, exist_ok=True)

        if os.path.exists(project_path):
            self.app.log.debug("Cleaning up old %s" % project_path)
            shutil.rmtree(project_path)

        self.app.log.info("Cloning into %s" % project_path)

        self.app.utils.raw_exec("git", "clone", repo_url, project_path)

        packet_path = os.path.join(project_path, "salt-packet.yml")
        packet = self.app.utils.yaml_silent(packet_path)

        top_path = os.path.join(project_path, packet.get("topfile", "top.sls"))
        topfile = self.app.utils.yaml_silent(top_path)

        self.app.log.info("Setting up your project: %s" % project)
        self.app.log.info("Using directory: %s" % project_path)
        self.app.log.info("Repository URL: %s" % repo_url)

        self.app.log.debug("salt-packet:")
        self.app.log.debug(SEP)
        self.app.log.debug(yaml.dump(packet))
        self.app.log.debug(SEP)

        environment = extra_env or {}

        environment['USER'] = user
        environment['UID'] = uid

        system_path = self.app.config.get("salt-packets", "system_path")
        system = self.app.utils.yaml_silent(system_path)

        self.app.log.debug(SEP)
        self.app.log.debug("Setting Environment Variables")
        self.app.log.debug(SEP)

        packet_env = packet.get("environment", {})
        search_for_env_vars = [
            k.upper() for k in 
            list(packet_env.keys()) +
            packet.get('requires_environment', []) +
            packet.get('shell_environment', [])
        ]

        for k in search_for_env_vars:
            k = k.upper()
            if k in extra_env:
                self.app.log.debug(
                    "Received --env argument for: %s = %s"%(k, extra_env[k])
                )
                environment[k] = extra_env[k]
                continue
            if k in os.environ:
                self.app.log.debug(
                    "Using ENV value for: %s = %s"%(k, os.environ[k])
                )
                environment[k] = os.environ[k]
                continue
            if k in system.get("environment", {}):
                self.app.log.debug(
                    "Using system value for: %s = %s"%(k, system["environment"][k])
                )
                environment[k] = system['environment'][k]
                continue
            if k in packet_env:
                self.app.log.debug("Defaulting environment to value from project's salt-packet.yml: %s = %s "%(k, v))
                environment[k] = packet_env[k]

        if not list(topfile.keys()) == ["base"]:
            self.app.log.error("Topfile is expected to have exactly one 'base' key")
            sys.exit(1)

        if not minion_id and list(topfile["base"].keys()) != ["*"]:
            print()
            print()
            print("This topfile supports multiple installation profiles:")
            for key, states in topfile["base"].items():
                print(key)
                for state in states:
                    print("  -", state)
            print("You must pick a minion_id for this installation.")
            print("Your minion ID will regex match against the profiles in the topfile")
            print("to determine which states will apply to this installation.")
            print("Please enter a minion_id:")
            minion_id = input()
            while not (
                minion_id.isascii() and "_" not in minion_id and "/" not in minion_id
            ):
                print("Please enter a valid minion_id:")
                minion_id = input()
        else:
            minion_id = minion_id or "".join(
                random.choice("abcdefghijklmnopqrstuvwxyz1234567890") for _ in range(8)
            )

        profile = {
            "minion_id": minion_id,
            "project_name": os.path.basename(project_path),
            "project_path": project_path,
            "repo_url": repo_url,
            "topfile": top_path,
            "salt_base": os.path.dirname(top_path),
            "environment": environment,
        }

        for env in packet.get("requires_environment", []):
            if not env.upper() in environment:
                self.app.log.error("Requires environment: %s" % env.upper())
                sys.exit(1)

        if True or not os.path.exists(profile_path):
            self.app.log.info("Saving project profile: %s" % profile_path)
            yaml.dump(profile, open(profile_path, "w+"))
        else:
            profile = self.app.utils.yaml_silent(profile_path)
            
        self.app.log.debug(SEP)
        self.app.log.debug("project profile:")
        self.app.log.debug("\n"+yaml.dump(profile))
        self.app.log.debug(SEP)

        installed = self.yaml_silent(self.installed_path()) or []

        for req in packet.get("requires", []):
            self.app.log.info("Requires packet: %s" % req)
            already = [
                p for p in installed
                if self.get_config(p)['profile']['repo_url'] == req
            ]
            if already:
                self.app.log.info("Requirement satisfied: %s" % req)
            else:
                self.add_packet(req, minion_id, extra_env=environment)
                            
        installed = self.yaml_silent(self.installed_path()) or []

        if not project in installed:
            installed += [project,]
        with open(self.installed_path(), 'w+') as fh:
            yaml.dump(installed, fh)
        
        if packet.get("post_install", ""):
            for line in packet["post_install"]:
                self.app.utils.raw_exec(*line)


    def git_pull(self, project):
        config = self.get_config(project)
        os.chdir(config["profile"]["project_path"])
        output = self.raw_exec(
            "git", "pull", "origin", config["profile"].get("branch", "master")
        )
        self.influx_count_many(config, {"git_pull": {"executions": 1}})
        return output

    def git_hard_pull(self, project):
        config = self.get_config(project)
        os.chdir(config["profile"]["project_path"])
        self.raw_exec("git", "fetch", "--all")
        self.influx_count_many(config, {"git_fetch": {"executions": 1}})
        return self.raw_exec(
            "git",
            "reset",
            "--hard",
            "origin/%s" % config["profile"].get("branch", "master"),
        )

    def create_daily_random_cronjob(self, project):
        hour = random.choice([0, 1, 2, 3])
        minute = random.choice(range(60))
        schedule = "%s %s * * *" % (hour, minute)
        print("Creating daily update cronjob at a random time:")
        print(schedule)
        return self.create_cronjob(project, schedule)

    def create_cronjob(self, project, schedule):
        config = self.get_config(project)
        with open(config["cronjob_path"], "w+") as fh:
            fh.write(
                '%s root echo "Cronjob trigger: %s @ $(date)">> /var/log/salt-packet.%s\n'
                % (schedule, project, project)
            )
            fh.write(
                "%s root /usr/local/bin/salt-packets update %s >> /var/log/salt-packet.%s\n"
                % (schedule, project, project)
            )

    def delete_cronjob(self, project):
        config = self.get_config(project)
        os.unlink(config["cronjob_path"])
