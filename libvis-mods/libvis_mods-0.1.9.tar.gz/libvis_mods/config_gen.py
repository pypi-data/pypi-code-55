import configparser
from pathlib import Path
from libvis_mods.utils import only_required_kwargs_call

filename = 'libvis-mod.conf'

BUILTIN_ABBREVIATIONS = {
    "gh": "https://github.com/{0}.git",
    "gl": "https://gitlab.com/{0}.git",
    "bb": "https://bitbucket.org/{0}",
}

def module_path(module):
    maybe_path = module.__path__
    try:
        path = maybe_path.pop()
    except (TypeError, AttributeError):
        # For _NamespacePath. Maybe I'm doing it wrong?
        path = maybe_path._path.pop()
    return path

def config_of_module(module):
    path = module_path(module)
    config = read_config(path)
    return config

def with_libvis_config(cmd, path='.'):
    def ncmd(*args, **kwargs):
        config = dict(read_config(Path(path)))
        for key, value in kwargs.items():
            if value is not None:
                config[key] = value
        print(config)
        return only_required_kwargs_call(cmd, *args, **config)
    ncmd.__name__ = cmd.__name__
    ncmd.__doc__ = cmd.__doc__
    return ncmd

def read_config(path):
    path = Path(path)
    config=configparser.ConfigParser()
    config.read(path / filename)
    if 'Module' in config.sections():
        mod = config['Module']
        mod['name'] =mod['modname']
        return dict(mod)
    else: return {}

def write_config(conf_dict, path):
    config=configparser.ConfigParser()
    config['Module'] = conf_dict
    with open(path / filename, 'w') as f:
        config.write(f)
