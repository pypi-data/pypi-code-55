import time
import subprocess
import sys
import logging


class GitDirectoryError(Exception):
    """Directory not a git repository"""


def generate(directory=".") -> str:
    commitDate = 0
    try:
        commitDate = int(
            subprocess.check_output(
                "git show -s --format='%ct'", shell=True, cwd=directory
            )
            .decode()
            .strip()
        )
    except subprocess.CalledProcessError:
        raise GitDirectoryError("Directory not a git repository")
    return time.strftime("%y.%j.%k%M%S", time.localtime(commitDate))


if __name__ == "__main__":
    try:
        print(generate(**dict(arg.split("=") for arg in sys.argv[1:])))
    except GitDirectoryError as e:
        logging.error("%s %s", "[DateVersioning]", e)
