from base64 import b64encode
import json
from pathlib import Path
from typing import BinaryIO, Dict, Union

import requests


class Transmission:

    def __init__(self, server: str, username: str, password: str) -> None:
        self.server = server
        if username:
            self.auth = (username, password)
        self.session = requests.Session()

    def _post(self, method: str, args: Dict) -> Dict:
        data = {
            'method': method,
            'arguments': args
        }
        r = self.session.post(self.server,
                              headers=self.csrf_token,
                              auth=self.auth,
                              data=json.dumps(data))
        return r.json()

    def _add(self, args: Dict[str, str]) -> Dict:
        args.update({
            'paused': 'false',
            'download-dir': self.server_info['download-dir']
        })
        response = self._post(method='torrent-add', args=args)
        return response['result']

    def add_file(self, file: BinaryIO) -> Dict:
        file_data_bytes = b64encode(file.read())
        file_data = file_data_bytes.decode('utf-8')
        args = {
            'metainfo': file_data
        }
        return self._add(args)

    def add_link(self, magnet_link: str) -> Dict:
        args = {
            'filename': magnet_link
        }
        return self._add(args)

    def get_field(self, id: str, field: str) -> str:
        args = {
            'ids': [id],
            'fields': [field]
        }
        response = self._post(method='torrent-get', args=args)
        return response['arguments']['torrents'][0][field]

    def rename(self, id: str, new_name: str) -> Dict:
        name = self.get_field(id, 'name')
        args = {
            'ids': [id],
            'path': name,
            'name': new_name
        }
        return self._post(method='torrent-rename-path', args=args)

    def move(self, id: str, new_path: Union[str, Path]) -> Dict:
        args = {
            'ids': [id],
            'location': str(new_path),
            'move': True
        }
        return self._post(method='torrent-set-location', args=args)

    @property
    def csrf_token(self) -> Dict[str, str]:
        csrf_key = 'X-Transmission-Session-Id'
        head = self.session.head(self.server, auth=self.auth)
        token = {
            csrf_key: head.headers[csrf_key]
        }
        return token

    @property
    def server_info(self) -> Dict:
        info = self._post('session-get', args={})
        return info['arguments']


class Torrent:
    def __init__(self, torrent_id: str, transmission_client: Transmission) -> None:
        self.client = transmission_client
        self.id = torrent_id
    
    def get_field(self, *args, **kwargs) -> str:
        return self.client.get_field(self.id, *args, **kwargs)
    
    def rename(self, *args, **kwargs) -> Dict:
        return self.client.rename(self.id, *args, **kwargs)
    
    def move(self, *args, **kwargs) -> Dict:
        return self.client.move(self.id, *args, **kwargs)