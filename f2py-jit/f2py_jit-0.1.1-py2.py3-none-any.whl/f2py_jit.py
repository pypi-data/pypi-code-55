# Part of this code is adapted from numpy.f2py module
# Copyright 2001-2005 Pearu Peterson all rights reserved,
# Pearu Peterson <pearu@cens.ioc.ee>
# Permission to use, modify, and distribute this software is given under the
# terms of the NumPy License.

"""
Test just in time create of python modules

Two steps. First register, then import from jit_modules.
"""

from __future__ import division, absolute_import, print_function
import importlib
import numpy
import sys
import subprocess
import os
import numpy as np

modules_dir = 'jit_modules'

__all__ = ['compile_module', 'available_modules', 'register_module', 'clear_modules', 'test']


# Adapted from numpy.f2py
def compile_module(source,
                   name,
                   extra_args='',
                   verbose=True,
                   source_fn=None,
                   extension='.f90'):
    """
    Build extension module from a Fortran source string with f2py.

    Parameters
    ----------
    source : str or bytes
        Fortran source of module / subroutine to compile

        .. versionchanged:: 1.16.0
           Accept str as well as bytes

    name : str, optional
        The name of the compiled python module
    extra_args : str or list, optional
        Additional parameters passed to f2py

        .. versionchanged:: 1.16.0
            A list of args may also be provided.

    verbose : bool, optional
        Print f2py output to screen
    source_fn : str, optional
        Name of the file where the fortran source is written.
        The default is to use a temporary file with the extension
        provided by the `extension` parameter
    extension : {'.f', '.f90'}, optional
        Filename extension if `source_fn` is not provided.
        The extension tells which fortran standard is used.
        The default is `.f`, which implies F77 standard.

        .. versionadded:: 1.11.0

    Returns
    -------
    result : int
        0 on success

    Examples
    --------
    .. include:: compile_session.dat
        :literal:

    """
    import tempfile
    import shlex

    if source_fn is None:
        f, fname = tempfile.mkstemp(suffix=extension)
        # f is a file descriptor so need to close it
        # carefully -- not with .close() directly
        os.close(f)
    else:
        fname = source_fn

    # Input source `src` can be a f90 file or a string containing f90 code"""
    if os.path.exists(source):
        with open(source) as fh:
            source = fh.read()
        
    if not isinstance(source, str):
        source = str(source, 'utf-8')
    try:
        with open(fname, 'w') as f:
            f.write(source)

        args = ['-c', '-m', name, f.name]

        if isinstance(extra_args, np.compat.basestring):
            is_posix = (os.name == 'posix')
            extra_args = shlex.split(extra_args, posix=is_posix)

        args.extend(extra_args)

        c = [sys.executable,
             '-c',
             'import numpy.f2py as f2py2e;f2py2e.main()'] + args
        try:
            output = subprocess.check_output(c, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as exc:
            status = exc.returncode
            output = exc.output
        except OSError:
            # preserve historic status code used by exec_command()
            status = 127
            output = ''
        else:
            status = 0

        try:
            output = output.decode()
        except UnicodeDecodeError:
            pass

        if verbose or status != 0:
            # Recolorize output
            import re
            class colors:
                OK = '\033[92m'
                WARN = '\033[93m'
                FAIL = '\033[91m'
                END = '\033[0m'
                BOLD = '\033[1m'
                UNDERLINE = '\033[4m'
            output = re.sub('[eE]rror', colors.UNDERLINE + colors.BOLD + colors.FAIL + 'Error' + colors.END, output)
            output = re.sub('[wW]arning', colors.UNDERLINE + colors.BOLD + colors.WARN + 'warning' + colors.END, output)
            print(output)
            
            if status != 0:
                raise RuntimeError('f2py compilation failed')
    finally:
        if source_fn is None:
            os.remove(fname)


def register_module(name, force=True):

    # Move module to jit package
    if not os.path.exists(modules_dir):
        os.makedirs(modules_dir)
        with open(os.path.join(modules_dir, '__init__.py'), 'w') as fh:
            pass

    f90 = importlib.import_module(name)
    tmp_module_path = f90.__file__
    module_path = os.path.join(modules_dir, os.path.basename(tmp_module_path))
    if force:
        os.replace(tmp_module_path, module_path)
    else:
        try:
            os.rename(tmp_module_path, module_path)
        except OSError:
            raise ValueError('module exists {}'.format(module_name))

    # Update
    if sys.version_info[0] > 2:
        importlib.invalidate_caches()

        
def _unique_id(db):
    import random
    import string
    current_uids = db.keys()
    while True:
        uid = ''.join(random.choice(string.ascii_lowercase) for _ in range(10))
        if uid not in current_uids:
            return uid

        
def build_module(source, metadata=None, extra_args='', db_file='.atooms_jit.json'):
    import json
    # TODO: acquire lock
    db_file = os.path.join(modules_dir, db_file)
    if os.path.exists(db_file):
        with open(db_file) as fh:
            db = json.load(fh)
    else:
        db = {}

    # If a db entry matches the potential then we reuse that uid
    uid = None
    for current_uid in db:
        if current_uid == "LAYOUT":
            continue
        if db[current_uid] == metadata:
            uid = current_uid
            assert uid in available_modules()
            break

    # If we could not find a matching uid, we get a new one and register it
    if uid is None:
        uid = _unique_id(db)
        assert uid not in available_modules()
        # Compile and register the new module
        compile_module(source, uid, verbose=False, extra_args=extra_args)
        register_module(uid, force=False)

        # Store module in db
        if "LAYOUT" not in db:
            db["LAYOUT"] = 1
        db[uid] = metadata
        with open(db_file, 'w') as fh:
            json.dump(db, fh)
    # TODO: release lock

    return uid


def import_module(name):
    try:
        f90 = importlib.import_module(modules_dir + '.' + name)
        return f90
    except:
        print('problem import module {}'.format(name))
        raise

    
def available_modules():
    if os.path.exists(modules_dir):
        import glob
        import pkgutil
        f90 = importlib.import_module(modules_dir)
        sub_modules = []
        for importer, modname, ispkg in pkgutil.iter_modules(f90.__path__):
            sub_modules.append(modname)
        return sub_modules
    else:
        return []

    
def clear_modules():
    f90 = importlib.import_module(modules_dir)
    # Update 
    if sys.version_info[0] > 2:
        importlib.invalidate_caches()

