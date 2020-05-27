#! /usr/bin/env python

import os
import shlex
from argparse import ArgumentParser
from yaml import load, Loader

from deploy.permissions import check_permissions_and_ownership

DEFAULT_SETTINGS_FILE = "ems-deploy.yml"


def run():
    parser = ArgumentParser("Deploy Utilities")
    parser.add_argument("-d", action="store_true", help="Adds a detach flag to the command")
    parser.add_argument("-a", action="store_true", help="Forces no detach flag to the command")
    parser.add_argument("-v", action="store_true", help="Writes the command to the console")
    parser.add_argument("--dry-run", action="store_true", help="Does not execute the commands")
    parser.add_argument("--flags", help="Change default flags. Must specify a sting afterwards")
    parser.add_argument("tag", nargs='?', help="The tag to run")
    parser.add_argument("--init", action="store_true", help="Only checks for directories and files")
    parser.add_argument("--ignore-checks", action="store_true", help="Ignores checks for files and directories")

    config_file_args = None
    dirs_to_check = {}
    files_to_check = []
    flags = ["--force-recreate", "--renew-anon-volumes", "--build"]
    if os.path.exists(DEFAULT_SETTINGS_FILE):
        with open(DEFAULT_SETTINGS_FILE) as f:
            x = load(f.read(), Loader=Loader)
            dirs_to_check = x.get("dirs", {})
            files_to_check = x.get("files", [])
            if "flags" in x:
                flags = shlex.split(x["flags"])

    # Parse inputs from console
    args = parser.parse_args(namespace=config_file_args)

    if not args.ignore_checks:
        check_permissions_and_ownership(dirs_to_check, True)
        for f in files_to_check:
            if not os.path.exists(f):
                print(f"File {f} is missing.")

    if args.init:
        exit(0)

    files_to_include = []

    # Find available files
    base_file = 'docker-compose.yml'
    if not os.path.exists(base_file):
        print(f"Could not find '{base_file}'")
        exit(1)

    files_to_include.append(base_file)

    # Parse environment
    if not args.tag:
        environment = 'deploy'
        tags = ['deploy'] if os.path.exists('docker-compose.deploy.yml') else []
    else:
        # Strip prefix and suffix if it is a file
        tags = args.tag.split(".")
        if os.path.exists(args.tag):
            tags = tags[1:-1]

        environment = tags[0]
        tags = ['.'.join(tags[:(x+1)]) for x in range(len(tags))]

    for t in tags:
        additional = f'docker-compose.{t}.yml'
        if not os.path.exists(additional):
            print(f"Could not find '{additional}'")
            exit(1)
        files_to_include.append(additional)

    if args.flags:
        flags = args.flags.split(' ')

    if not args.a and (environment == 'deploy' or args.d):
        flags.append("-d")

    # We build command
    cmd = f'docker-compose -p {environment} -f {" -f ".join(files_to_include)} up {" ".join(flags)}'

    if args.v:
        print(cmd)

    if not args.dry_run:
        os.system(cmd)

        if "-d" in flags:
            os.system(f"docker-compose -p {environment} logs -f")


if __name__ == "__main__":
    run()
