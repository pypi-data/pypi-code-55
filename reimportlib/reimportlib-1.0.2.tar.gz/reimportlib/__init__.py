"""
reimportlib: refactored imports
"""
# pylint: disable=redefined-builtin
import importlib
import inspect
import json
import operator

DEFAULT_PATH = ".reimport.json"
REMAP_PATHS = {}
IMPORT = __import__

def configure(remap_file=DEFAULT_PATH):
    "Configures mappings from remap_file, if available."
    try:
        with open(remap_file) as reimport_json:
            reimports = json.loads(reimport_json.read())
            for source_import, target_import in reimports.items():
                remap(source_import, target_import)
    finally:
        pass

def get_remapped_name(name):
    "Provides a remapped name if possible."
    found_source_import = ""
    for source_import in REMAP_PATHS:
        if name.startswith(source_import) and len(source_import) > len(found_source_import):
            found_source_import = source_import
    return name.replace(found_source_import, REMAP_PATHS.get(found_source_import, ""), 1)

def remap(source_import=None, target_import=None):
    "Remap source_import -> target_import"
    REMAP_PATHS[source_import] = target_import

def import_(name, globals=None, locals=None, fromlist=(), level=0):
    "Provides an alternative for __import__."
    return IMPORT(get_remapped_name(name), globals=globals, locals=locals,
                  fromlist=fromlist, level=level)

def import_module(name, package=None):
    "Import remapped module."
    return importlib.import_module(get_remapped_name(name), package)

def import_from(name, text=None):
    "Import variable from remapped module."
    if not text:
        text = '*'
    if not isinstance(text, (list, tuple, set)):
        if not isinstance(text, (str)):
            raise ImportError('Cannot import {} from {}'.format(text, name))
        if ',' in text:
            imports = [importText.strip() for importText in text.split(',')]
        else:
            imports = [text]
    package_found = import_(name, globals=True, locals=True, fromlist=list(imports))
    if '*' in text or ',' in text:
        return package_found
    return operator.attrgetter(text)(package_found)

def instantiate(name, text, *args, **kwargs):
    "Import and instantiate from remapped module."
    class_found = import_from(name, text)
    if inspect.isclass(class_found):
        return class_found(*args, **kwargs)
    return None
