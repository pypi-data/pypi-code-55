"""mHealth Lab client

Usage:
  mhlab download <study> [-p | --pid <id> -d | --decrypt <pwd> -f | --folder <folder>]
  mhlab watch [convert -f | --folder <folder> -s | --sr <sampling_rate>]
  mhlab -h | --help
  mhlab -v | --version

Options:
  -h, --help                                Show help message
  -v, --version                             Show program version
  -p <pid>, --pid <pid>                     The participant ID
  -d <pwd>, --decrypt <pwd>                 Use <pwd> to decrypt the downloaded files.
  -f <folder>, --folder <folder>            Local folder for downloaded dataset.
  -s <sampling_rate>, --sr <sampling_rate>  The sampling rate of the converted watch file in Actigraph csv format.
"""

from docopt import docopt
from .main import Client
from .android_watch import AndroidWatch
from loguru import logger


def mhlab():
    arguments = docopt(__doc__, version='mHealth Lab Client 0.3.0')
    logger.debug(arguments)
    if arguments['download']:
        study_name = arguments['<study>']
        if len(arguments['--decrypt']) == 0:
            pwd = None
        else:
            pwd = str.encode(arguments['--decrypt'][0])
        if len(arguments['--folder']) == 0:
            to = './' + study_name
        else:
            to = arguments['--folder'][0]
        if len(arguments['--pid']) == 0:
            pid = None
        else:
            pid = arguments['--pid'][0]
        logger.add(to + "/mhlab_download.log", rotation="500 MB")
        if pid is None:
            download_all(study_name, to, pwd)
        else:
            download_by_participant(study_name, pid, to, pwd)
    elif arguments['watch']:
        if arguments['convert']:
            to = arguments['--folder'][0]
            sr = int(arguments['--sr'][0])
            convert_watch_files(to, sr)


def download_all(study_name, to, pwd):
    client = Client()
    if not client.validate_study_name(study_name):
        exit(1)
    client.connect()
    client.download_all(study_name, to, pwd)


def download_by_participant(study_name, pid, to, pwd):
    client = Client()
    if not client.validate_study_name(study_name):
        exit(1)
    client.connect()
    client.download_by_participant(study_name, pid, to, pwd)


def convert_watch_files(to, sr):
    watch = AndroidWatch(to)
    watch.convert_to_actigraph(sr=sr)


if __name__ == '__main__':
    mhlab()
