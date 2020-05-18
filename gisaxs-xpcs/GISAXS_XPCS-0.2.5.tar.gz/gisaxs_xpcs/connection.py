import logging
from pathlib import Path

import pysftp

CACHE_FOLDER: Path = Path(__file__).parent / 'temp'

if not CACHE_FOLDER.is_dir():
    CACHE_FOLDER.mkdir()


class Connection(object):
    CACHE_SIZE = 100  # number of allowed files to store in cache

    log = logging.getLogger(__name__)

    def __init__(self):
        self.__auth_dict = {}
        self._sftp = None
        self._cache_folder = Path(__file__).parent / 'temp'
        self.clear_cache()

    def set_auth(self, username: str, password: str, host: str = 'moneta.uni-tuebingen.de', port: int = 22):
        self.__auth_dict = dict(host=host, port=port, username=username, password=password)

    @property
    def cache(self) -> Path:
        return self._cache_folder

    @property
    def sftp(self):
        return self._sftp

    def connect(self):
        if not self.__auth_dict:
            self.log.error('Authentication parameters are not set!')
            return False

        self.log.info(f'Connecting to the server '
                      f'{self.__auth_dict["username"]}@{self.__auth_dict["host"]}:{self.__auth_dict["port"]}.'
                      f'Please, wait ... ')
        self.disconnect()
        try:
            self._sftp = pysftp.Connection(**self.__auth_dict)
            self.log.info('Successfully connected to the server!')
        except pysftp.AuthenticationException as err:
            self.log.error(f'Invalid username or password: {err}')
            return False
        except pysftp.ConnectionException as err:
            self.log.error(f'Could not connect to the server: {err}')
            return False
        except Exception as err:
            self.log.exception(err)
            return False
        return True

    def disconnect(self):
        if self.sftp:
            try:
                self._sftp.close()
                self.log.info('Disconnected from the server.')
                self._sftp = None
            except Exception as err:
                self.log.exception(err)

    def clear_cache(self):
        for p in self.cache.glob('*'):
            p.unlink()

    def update_cache(self):
        temp_files = list(self.cache.glob('*'))
        if len(temp_files) > self.CACHE_SIZE:
            for p in temp_files:
                p.unlink()

    def save_file(self, src: str):
        filename = src.split('/')[-1]
        dest = f'{str(self.cache.resolve())}/{filename}'
        self.update_cache()
        self.sftp.get(src, dest)
        self.log.info(f'File is saved locally from {src} to {dest}.')
        return dest

    def __del__(self):
        self.disconnect()
