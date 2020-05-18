import sys
from .console import Console
from .executor import Executor


def main():
    exit(Executor(Console(sys.stdout)).entrypoint(*sys.argv))
