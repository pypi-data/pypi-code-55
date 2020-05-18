from pathlib import Path
from . import utils

def generate_index(import_str, mod_dir):
    mod_dir = Path(mod_dir)
    mods = [x.name for x in mod_dir.iterdir() if x.is_dir()]
    x = '\n'.join(map(import_str, mods))
    return x

def generate_index_py(import_str, mod_dir):
    mod_dir = Path(mod_dir)
    mods = [x.name for x in mod_dir.iterdir() if x.is_dir()]
    mods = [x for x in mods if x!='__pycache__']
    x = '\n'.join(map(import_str, mods))
    return x

## Python

def _import_str_py(modname):
    return f"from .{modname} import {modname}"

def index_import_py(usr_mods):
    index = generate_index_py(_import_str_py, usr_mods)
    utils.write_to(index, usr_mods/'__init__.py')

def root_import_py(src_file, moddir):
    """Put `__init__.py` in `moddir` to export `moddir.name` from `src_file`."""
    modname = moddir.name
    utils.write_to(f"from .{src_file.stem} import {modname} ",
             moddir/'__init__.py')

## JS

def _import_str_js(modname):
    return f"export {{default as {modname}}} from './{modname}'"

def index_import_js(usr_mods):
    index = generate_index(_import_str_js, usr_mods)
    utils.write_to(index, usr_mods/'index.js')

def root_import_js(src_file, moddir):
    """Put `index.js` in `moddir` to export
    default as `moddir.name` from `src_file`."""
    modname = moddir.name
    x = f"import {{default as {modname}}} from './{src_file.name}';\
            export default {modname}"
    utils.write_to(x, moddir/'index.js')

