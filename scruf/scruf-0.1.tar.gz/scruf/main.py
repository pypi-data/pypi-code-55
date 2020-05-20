import sys

from scruf.runners import cli


def run(argv):
    # TODO: implement options/config
    # options = get_options(argv)
    filenames = get_files(argv)
    success = True
    for filename in filenames:
        success &= cli.run(filename)

    exit_code = 0 if success else 1
    sys.exit(exit_code)


def get_options(argv):
    # TODO
    return None


def get_files(argv):
    # TODO: just a placeholder
    return argv[1:]
