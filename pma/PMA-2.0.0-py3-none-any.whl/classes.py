"""
MIT License

Copyright (c) 2018-2020 Nihaal Sangha (Orangutan)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import hashlib
import json
from itertools import zip_longest
from pathlib import Path
from typing import List

import requests

from pma.exceptions import InvalidLogin

__all__ = ['ALL_PLCS', 'User']

BASE_URL = 'https://mathsapp.pixl.org.uk/PMA2/'
VERSION_NUMBER = '4.81'

with open(Path(__file__).parent.joinpath('plcs.json')) as fp:
    ALL_PLCS = json.load(fp)


def _plc_id_from_question(question: str) -> int:
    for i in ALL_PLCS:
        if i['question'] == question:
            return int(i['plcid'])
    raise ValueError()


def _marks_from_question(question: str) -> int:
    for i in ALL_PLCS:
        if i['question'] == question:
            return int(i['marks'])
    raise ValueError()


def _generate_password_id(password: str) -> str:
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='
    result = []

    def grouper(iterable, n, fill_value=None):
        args = [iter(iterable)] * n
        return zip_longest(*args, fillvalue=fill_value)

    def garbage(x):
        if 0 <= x < len(alphabet):
            result.append(alphabet[x])

    key = '27547926900371943559504075757240789858832978611624259782'
    processed = [c + ord(key[i % len(key) - 1]) for i, c in enumerate(map(ord, password))]
    for a, b, c in grouper(processed, 3):
        garbage(a >> 2)
        garbage((a & 3) << 4 | (0 if b is None else b) >> 4)
        garbage(64 if b is None else (b & 15) << 2 | (0 if c is None else c) >> 6)
        garbage(64 if b is None or c is None else c & 63)
    return ''.join(result)


def _general_request(endpoint: str, headers: dict = None, method: str = 'GET', payload=None) -> requests.Response:
    headers = headers or {}
    headers['Referer'] = 'https://mathsapp.pixl.org.uk/PiXL%20PMA4.swf'
    return requests.request(method, BASE_URL + endpoint, headers=headers, data=payload)


def _var1_response_to_json(response: str) -> dict:
    return json.loads(response[5:])


class LeaderboardEntry:
    def __init__(self, id_value: int, username: str, score: int, total_score: int, match: bool):
        self._id_value = id_value
        self._username = username
        self._score = score
        self._total_score = total_score
        self._match = match

    @classmethod
    def from_api(cls, response: dict):
        return cls(
            int(response['idvalue']),
            response['username'],
            int(response['score']),
            int(response['totalscore']),
            bool(int(response['match']))
        )

    def __repr__(self):
        return f'<LeaderboardEntry username={self.username}>'

    @property
    def username(self) -> str:
        return self._username

    @property
    def score(self) -> int:
        return self._score


class User:
    def __init__(self, id_value: str, token: int, school_id: str, json_feed: list):
        self._id_value = id_value
        self._token = token
        self._school_id = school_id
        self._json_feed = json_feed

    @property
    def token123(self) -> str:
        return hashlib.md5(f'{self._id_value}{self._token}'.encode('utf-8')).hexdigest()

    @classmethod
    def login(cls, username: str, password: str, school_id: str):
        r = _var1_response_to_json(_general_request('MDTSloginsecure2.php', None, 'POST',
                                                    {
                                                        'userid': username,
                                                        'passwordid': _generate_password_id(password),
                                                        'schoolname': school_id,
                                                        'versionnumber': VERSION_NUMBER
                                                    }).content)

        if r['status'] != 'success':
            raise InvalidLogin(r['status'])

        return cls(r['idvalue'], r['token'], r['sessionid'], r['datajson1'])

    def send_score(self, engagement_points: int, question: str):
        r = _general_request('MDTSsavesecure3.php', None, 'POST', {
            'userid': self._id_value,
            'jsonfeed': self._json_feed,
            'schoolid': self._school_id,
            'engagementpoint': engagement_points,
            'chosenplcid': _plc_id_from_question(question),
            'token123': self.token123,
            'questiontosave': question,
            'scorefromquestion': _marks_from_question(question)
        })

        token = r.content[8:]

        if token == 'false':
            raise Exception()

        self._token = int(token)

    def get_leaderboard(self) -> List[LeaderboardEntry]:
        r = _general_request('MDTSscoreboard.php', None, 'POST', {
            'userid': self._id_value,
            'schoolname': self._school_id
        })

        out = []

        for leaderboard_entry in _var1_response_to_json(r.content):
            out.append(LeaderboardEntry.from_api(leaderboard_entry))

        return out
