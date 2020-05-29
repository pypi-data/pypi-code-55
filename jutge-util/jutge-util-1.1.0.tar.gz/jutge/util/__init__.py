"""
Common utilities for Jutge.org's scripts
"""

import logging
import os
import shutil
import socket
import sys
import tarfile
import tempfile
import time

import yaml


# ----------------------------------------------------------------------------
# Ping
# ----------------------------------------------------------------------------

def ping():
    print('pong')


# ----------------------------------------------------------------------------
# Logging
# ----------------------------------------------------------------------------

def init_logging():
    """Configures custom logging options."""

    logging.basicConfig(
        format='%s@%s ' % (get_username(), get_hostname()) + '%(asctime)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )
    logging.getLogger('').setLevel(logging.NOTSET)


# ----------------------------------------------------------------------------
# Environment
# ----------------------------------------------------------------------------


def get_username():
    return os.getenv("USER")


def get_hostname():
    return socket.gethostname()


# ----------------------------------------------------------------------------
# Utilities for lists
# ----------------------------------------------------------------------------

def intersection(a, b):
    return filter(lambda x: x in a, b)


# ----------------------------------------------------------------------------
# Utilities for general directories
# ----------------------------------------------------------------------------


def read_file(name):
    """Returns a string with the contents of the file name."""
    f = open(name)
    r = f.read()
    f.close()
    return r


def write_file(name, txt=""):
    """Writes the file name with contents txt."""
    f = open(name, "w")
    f.write(txt)
    f.close()


def append_file(name, txt=""):
    """Adds to file name the contents of txt."""
    f = open(name, "a")
    f.write(txt)
    f.close()


def del_file(name):
    """Deletes the file name. Does not complain on error."""
    try:
        os.remove(name)
    except OSError:
        pass


def file_size(name):
    """Returns the size of file name in bytes."""
    return os.stat(name)[6]


def tmp_dir():
    """Creates a temporal directory and returns its name."""
    return tempfile.mkdtemp('.dir', get_username() + '-')


def tmp_file():
    """Creates a temporal file and returns its name."""
    return tempfile.mkstemp()[1]


def file_exists(name):
    """Tells whether file name exists."""
    return os.path.exists(name)


def copy_file(src, dst):
    """Copies a file from src to dst."""
    shutil.copy(src, dst)


def copy_dir(src, dst):
    """Recursively copy an entire directory tree rooted at src to dst."""
    shutil.copytree(src, dst)


def move_file(src, dst):
    """Recursively move a file or directory to another location."""
    shutil.move(src, dst)


# ----------------------------------------------------------------------------
# Utilities for yml files
# ----------------------------------------------------------------------------


def print_yml(inf):
    print(yaml.dump(inf, indent=4, width=1000, default_flow_style=False))


def write_yml(path, inf):
    yaml.dump(inf, open(path, "w"), indent=4,
              width=1000, default_flow_style=False)


def read_yml(path):
    return yaml.load(open(path, 'r'), Loader=yaml.FullLoader)


# ----------------------------------------------------------------------------
# Utilities for properties files
# ----------------------------------------------------------------------------


def read_props(path):
    """Returns a dictionary with the properties of file path."""
    dic = {}
    f = open(path)
    for line in f.readlines():
        k, v = line.split(":", 1)
        dic[k.strip()] = v.strip()
    return dic


def write_props(path, inf):
    """Writes to file path the properties of file inf."""
    t = ""
    for k, v in inf.iteritems():
        t += k + ": " + v + "\n"
    write_file(path, t)


# ----------------------------------------------------------------------------
# Utilities for tar/tgz files
# ----------------------------------------------------------------------------


def create_tar(name, filenames, path=None):
    """Creates a tar file name with the contents given in the list of filenames.
    Uses path if given."""
    if name == "-":
        tar = tarfile.open(mode="w|", fileobj=sys.stdout)
    else:
        tar = tarfile.open(name, "w")
    cwd = os.getcwd()
    if path:
        os.chdir(path)
    for x in filenames:
        tar.add(x)
    if path:
        os.chdir(cwd)
    tar.close()


def create_tgz(name, filenames, path=None):
    """Creates a tgz file name with the contents given in the list of filenames.
    Uses path if given."""
    if name == "-":
        tar = tarfile.open(mode="w|gz", fileobj=sys.stdout)
    else:
        tar = tarfile.open(name, "w:gz")
    cwd = os.getcwd()
    if path:
        os.chdir(path)
    for x in filenames:
        tar.add(x)
    if path:
        os.chdir(cwd)
    tar.close()


def extract_tar(name, path):
    """Extracts a tar file in the given path."""
    if name == "-":
        tar = tarfile.open(mode="r|", fileobj=sys.stdin)
    else:
        tar = tarfile.open(name)
    for x in tar:
        tar.extract(x, path)
    tar.close()


def extract_tgz(name, path):
    """Extracts a tgz file in the given path."""
    if name == "-":
        tar = tarfile.open(mode="r|gz", fileobj=sys.stdin)
    else:
        tar = tarfile.open(name, "r:gz")
    for x in tar:
        tar.extract(x, path)
    tar.close()


def get_from_tgz(tgz, name):
    """Returns the contents of file name inside a tgz or tar file."""
    tar = tarfile.open(tgz)
    f = tar.extractfile(name)
    r = f.read()
    f.close()
    tar.close()
    return r


# ----------------------------------------------------------------------------
# Utilities for directories
# ----------------------------------------------------------------------------


def del_dir(path):
    """Deletes the directory path. Does not complain on error."""
    try:
        shutil.rmtree(path)
    except OSError:
        pass


def mkdir(path):
    """Makes the directory path. Does not complain on error."""
    try:
        os.makedirs(path)
    except OSError:
        pass


# ----------------------------------------------------------------------------
# Utilities for dates and times
# ----------------------------------------------------------------------------


def current_year():
    """Returns a string with the current year."""
    return time.strftime("%Y")


def current_time():
    """Returns a string with out format for times."""
    return time.strftime("%Y-%m-%d %H:%M:%S")


def current_date():
    """Returns a string with out format for dates."""
    return time.strftime("%Y-%m-%d")
