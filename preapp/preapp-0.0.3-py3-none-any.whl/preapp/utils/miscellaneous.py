import subprocess
from typing import Any


def bash(command: str) -> Any:
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,)
    stdout, _ = process.communicate()
    return stdout
