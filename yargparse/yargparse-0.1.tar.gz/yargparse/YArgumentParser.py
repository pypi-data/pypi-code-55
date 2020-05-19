import yaml
import argparse
import ast
from argparse import Namespace

def dicts_to_namespaces(config):
    new_config = {}
    for key, val in config.items():
        if isinstance(val, dict):
            new_config[key] = dicts_to_namespaces(val)
        else:
            new_config[key] = val
    return Namespace(**new_config)

class YArgumentParser(argparse.ArgumentParser):
    def __init__(self, yaml_flag, yaml_dest, yaml_default=None, **kwargs):
        super().__init__(**kwargs)

        self.add_argument(yaml_flag, yaml_dest, default=yaml_default)
        self.yaml_dest = yaml_dest[2:]

    def parse_args(self, **kwargs):
        args, overrides = super().parse_known_args()
        args = vars(args)
        config = yaml.load(open(args[self.yaml_dest]))

        overrides = ' '.join(overrides)
        overrides = [s.strip() for s in overrides.split('--') if s != '']

        for override in overrides:
            keystr, value = override.split('=', 1)

            keys = keystr.split('.') if '.' in keystr else [keystr]

            root = config
            for key in keys[:-1]:
                root = root[key]
                    
            if type(root[keys[-1]]) != str:
                root[keys[-1]] = ast.literal_eval(value)
            else:
                root[keys[-1]] = value

        config = {**config, **args}
        return dicts_to_namespaces(config)
