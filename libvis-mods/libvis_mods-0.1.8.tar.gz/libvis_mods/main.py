from os import makedirs
import os
import time
import sys
from pathlib import Path
from loguru import logger as log

from . import utils
from .python_hot_reload import python_dev_server
from .imports import (
      index_import_py , root_import_py
    , index_import_js , root_import_js
)

from libvis_mods.paths_config import (
    manager_path,
    web_src, web_user_mods,
    build_dir, python_user_mods
)

def _prepare_dir_struct(src, usr_mods, modname, action):
    """
    :arg src: source directory of module
    :arg usr_mods: a root directory of modules installed
    :arg modname: module name
    :arg action: copy, link or whatever function that takes src and moddir
    """
    moddir = usr_mods / modname
    makedirs(usr_mods, exist_ok=True)
    if src.is_file():
        makedirs(moddir, exist_ok=True)
    action(src.absolute(), moddir)
    return moddir

def _update_imports():
    index_import_py(python_user_mods)
    index_import_js(web_user_mods)

def _process_py(modname, back_src, action=utils.copy):
    back_moddir = _prepare_dir_struct(back_src, python_user_mods, modname,
                                      action=action)
    if back_src.is_file():
        root_import_py(back_src, back_moddir)

def _process_js(modname, front_src, action=utils.copy):
    front_moddir = _prepare_dir_struct(front_src, web_user_mods, modname,
                                           action=action)
    if front_src.is_file():
        root_import_js(front_src, front_moddir)

## ## ## API ## ## ##  

def develop(modname, back_src, front_src):
    log.remove()
    log.add(sys.stdout, level='DEBUG')
    back_src, front_src = Path(back_src), Path(front_src)
    _process_py(modname, back_src, action=utils.ln)
    _process_js(modname, front_src, action=utils.ln)

    _update_imports()

    print(f"watching python src dir")
    python_dev_server(modname, back_src)

    print(f"Running webpack devolopment server from {web_src}...")

    p = os.getcwd()
    os.chdir(web_src)
    utils.run_cmd([manager_path/'develop.sh', web_src])
    os.chdir(p)

def install(modname, back_src, front_src,
            post_cmd=None, pre_cmd=None
           ):
    try:
        back_src, front_src = Path(back_src), Path(front_src)
        _process_py(modname, back_src, action=utils.copy)
        _process_js(modname, front_src, action=utils.copy)

        if pre_cmd:
            print("Running pre install", post_cmd)
            utils.run_cmd(pre_cmd.split())

        _update_imports()
        ## Build the front and copy dist
        print(f"Building the app from {web_src}...")
        utils.run_cmd([manager_path/'build.sh', web_src])
        utils.copy(web_src/'dist', build_dir)
        print(f"Successfully installed module {modname}")
    except:
        uninstall(modname)
        raise
    finally:
        _update_imports()
        if post_cmd:
            print("Running post install", post_cmd)
            utils.run_cmd(post_cmd.split())

def uninstall(modname):
    utils.rm(python_user_mods / modname)
    utils.rm(web_user_mods / modname)
    _update_imports()
    print(f"Uninstalled module {modname}")

def installed():
    import libvis.modules.installed as installed
    return [x for x in installed.__dir__() if x[0] != '_']

