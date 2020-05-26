import yaml


def get_version():
    with open('version.yaml', "r") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    return data['version']
