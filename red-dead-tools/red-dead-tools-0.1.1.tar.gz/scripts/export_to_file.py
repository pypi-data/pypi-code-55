import os

from red_dead import base_dir
from red_dead.export import write_export

# private sub-module for portable local dev
AUTH_PATH = base_dir / 'red-dead-tools-private/.data/red-dead-tools-b475e08cb189.json'

EXPORT_PATH = base_dir / 'exports'


def export():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = str(AUTH_PATH)

    write_export(EXPORT_PATH)


if __name__ == '__main__':
    export()
