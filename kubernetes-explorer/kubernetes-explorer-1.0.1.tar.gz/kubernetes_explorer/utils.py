import argparse
import os
import yaml


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def read_yaml(filename: str) -> dict:
    if not file_exists(filename):
        return {}

    with open(filename, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as e:
            print(e)


def file_exists(filename: str) -> bool:
    return os.path.isfile(filename) and os.access(filename, os.R_OK)
