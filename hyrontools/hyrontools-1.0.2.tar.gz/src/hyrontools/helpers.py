import os
from dataclasses import field


def load_file(filename, handler):
    with open(filename, 'r') as infile:
        return handler(infile)


def get_base_dir(filename):
    return os.path.dirname(os.path.realpath(filename))


def get_pkg_dir():
    return get_base_dir(__file__)


def get_pkg_filename(*args):
    return os.path.join(get_pkg_dir(), *args)


def get_asset_filename(name, ext="txt"):
    return get_pkg_filename("assets", f"{name}.{ext}")


def load_text_asset(name):
    return load_file(get_asset_filename(name), lambda x: x.read())


def default(factory):
    return field(default_factory=factory)
