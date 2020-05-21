import os,sys
from dotenv.main import dotenv_values


def load_configs(path):
    configs = []
    try:
        if os.path.isfile(path):
            return [dotenv_values(dotenv_path=path)]
        configFiles = os.listdir(path)
        for file in configFiles:
            file_path = ('{}/{}'.format(path,file))
            configs.append(dotenv_values(dotenv_path=file_path))
    except FileNotFoundError:
        print('Invalid path: {}'.format(path))
        sys.exit(0)

    return configs
