"""
The build plugin is used to execute the build routines for non-python components
"""
# Import python libs
import os
import shutil
import subprocess
import tempfile
import logging
import sys

log = logging.getLogger(__name__)


def make(hub, bname):
    opts = hub.tiamat.BUILDS[bname]
    build = opts["build"]
    if not build:
        return
    bdir = tempfile.mkdtemp()
    cur_dir = os.getcwd()
    os.chdir(bdir)
    if opts["srcdir"]:
        for fn in os.listdir(opts["srcdir"]):
            shutil.copy(os.path.join(opts["srcdir"], fn), bdir)
    for proj, conf in build.items():
        if not opts["srcdir"]:
            if "sources" in conf:
                sources = conf["sources"]
                if isinstance(sources, str):
                    sources = [sources]
            for source in sources:
                retcode = subprocess.call(f"wget {source}", shell=True)
                if retcode != 0:
                    print("wget failed to download sources with return code: {retcode}")
                    sys.exit(retcode)
        if "make" in conf:
            for cmd in conf["make"]:
                subprocess.call(cmd, shell=True)
        if "src" in conf and "dest" in conf:
            srcs = conf["src"]
            dest = os.path.join(opts["venv_dir"], conf["dest"])
            print(f"Copying: {srcs}->{dest}")
            if not isinstance(srcs, (list, tuple)):
                srcs = [srcs]
            for src in srcs:
                fsrc = os.path.join(bdir, src)
                if os.path.isfile(fsrc):
                    shutil.copy(fsrc, dest)
                    hub.tiamat.BUILDS[bname]["binaries"].append(
                        (os.path.join(dest, os.path.basename(fsrc)), ".")
                    )
                elif os.path.isdir(fsrc):
                    shutil.copytree(fsrc, dest)
    os.chdir(cur_dir)
