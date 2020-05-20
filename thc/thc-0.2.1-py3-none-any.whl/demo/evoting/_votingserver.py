import http.server
import urllib.parse
import json
import sqlite3
from time import time
from functools import reduce
from operator import mul

from ._b64 import *

class VotingServer (http.server.BaseHTTPRequestHandler):

    def __init__ (self, db_file, *args, **kwargs):
        self._db_file = db_file
        super().__init__(*args, **kwargs)

    def version_string (self):
        return 'THC demo e-voting server'

    def _response (self, data):
        self.send_header('Content-Type', 'application/json')
        content = bytes(json.dumps(data) + '\n', 'utf-8')
        self.send_header('Content-Length', len(content))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With')
        self.send_header('Access-Control-Request-Headers', 'Content-Length')
        self.end_headers()
        self.wfile.write(content)

    def _ok (self, data):
        self.send_response(200)
        self._response(data)

    def _see_other (self, loc):
        self.send_response(303)
        self.send_header('Location', loc)
        self._response('Vote created.')

    def _bad_request (self, data):
        self.send_response(400)
        self._response(data)

    def _forbidden (self, data):
        self.send_response(403)
        self._response(data)

    def _not_found (self, data):
        self.send_response(404)
        self._response(data)

    def _length_required (self, data):
        self.send_response(411)
        self._response(data)

    def _error (self, data):
        self.send_response(500)
        self._response(data)

    def _parse_route (self):
        self._path = self.path.split('/')
        self._key = self._path[1]
        self._action = self._path[2] if len(self._path) > 2 else ''

    def _do_info (self):
        propositions = self._db.execute(('SELECT title FROM propositions '
                                         'WHERE vote=?'),
                                        (self._vote['id'],)).fetchall()
        self._ok({'title':   self._vote['title'],
                  'closing': self._vote['closing'],
                  'expiry':  self._vote['expiry'],
                  'propositions': [proposition['title']
                                   for proposition in propositions]})

    def _do_ballot (self):
        ballot = self._path[3].split(':') if len(self._path) > 3 else None
        if ballot is None            or \
           len(ballot) != 2          or \
           not ballot[0].isdigit() or \
           len(ballot[1]) != 8:
            self._not_found('Invalid request.')
        else:
            ballot = self._db.execute(('SELECT author, checksum, fingerprint '
                                       'FROM ballots WHERE vote=? AND id=? '
                                       'AND SUBSTR(checksum, 1, 8)=?'),
                                      (self._vote['id'],
                                       ballot[0],
                                       ballot[1])).fetchone()
            if ballot is None:
                self._not_found('Invalid ballot.')
            else:
                self._ok({'author':      ballot['author'],
                          'checksum':    ballot['checksum'],
                          'fingerprint': ballot['fingerprint']})

    def _do_ballots (self):
        if self._vote['closing'] > time():
            self._forbidden('This vote is not closed yet.')
        else:
            ballots = self._db.execute(('SELECT author, checksum, fingerprint '
                                        'FROM ballots WHERE vote=?'),
                                       (self._vote['id'],)).fetchall()
            self._ok([{'author':      ballot['author'],
                       'checksum':    ballot['checksum'],
                       'fingerprint': ballot['fingerprint']}
                      for ballot in ballots])

    def _do_results (self):
        if self._vote['closing'] > time():
            self._forbidden('This vote is not closed yet.')
        else:
            results = self._db.execute(('SELECT title, score '
                                        'FROM propositions '
                                        'WHERE vote=? ORDER BY id ASC'),
                                 (self._vote['id'],)).fetchall()
            self._ok([{'proposition': result['title'],
                       'score':       result['score']}
                      for result in results])

    def _do_create_vote (self, data):
        if 'key' not in data                                  or \
           'mod' not in data                                  or \
           'title' not in data                                or \
           'closing' not in data                              or \
           'expiry' not in data                               or \
           'propositions' not in data                         or \
            not valid_b64(data['key'][0])                     or \
            not valid_b64(data['mod'][0])                     or \
            not valid_b64(data['title'][0])                   or \
            not data['closing'][0].isdigit()                or \
            not data['expiry'][0].isdigit()                 or \
            int(data['closing'][0]) >= int(data['expiry'][0]) or \
            int(data['closing'][0]) < time()                  or \
            not all(valid_b64(p) for p in data['propositions']):
            self._bad_request('Malformed request.')
        else:
            try:
                if self._db.execute('SELECT 1 FROM votes WHERE key=?',
                                    (data['key'][0],)).fetchone() is not None:
                    self._bad_request('This vote already exists.')
                else:
                    vote_id = self._db.execute(('INSERT INTO votes VALUES '
                                                '(NULL, ?, ?, ?, ?, ?)'),
                                               (data['key'][0],
                                                data['mod'][0],
                                                data['title'][0],
                                                data['closing'][0],
                                                data['expiry'][0])) \
                                      .lastrowid
                    self._db.executemany(('INSERT INTO propositions VALUES '
                                          '(NULL, ?, ?, ?)'),
                                         [(vote_id,
                                           proposition,
                                           b64e(1))
                                          for proposition
                                          in data['propositions']])
                    self._db.commit()
                    self._see_other('/' + data['key'][0])
            except:
                self._error('Database failure.')

    def _do_cast_ballot (self, data):
        vote = self._db.execute(('SELECT id, mod, closing '
                                 'FROM votes WHERE key=?'),
                                (self._key,)).fetchone()
        if vote is None:
            self._not_found('Invalid vote.')
        elif vote['closing'] < time():
            self._forbidden('This vote is closed.')
        else:
            propositions = self._db.execute(('SELECT id, score '
                                             'FROM propositions '
                                             'WHERE vote=? ORDER BY id ASC'),
                                      (vote['id'],)).fetchall()
            if 'author' not in data                         or \
               'votes' not in data                          or \
               'fingerprint' not in data                    or \
               not valid_b64(data['author'][0])             or \
               not all(valid_b64(v) for v in data['votes']) or \
               not valid_b64(data['fingerprint'][0])        or \
               len(data['votes']) != len(propositions):
                self._bad_request('Malformed request.')
            else:
                try:
                    checksum = self._sum_votes(data['votes'], vote['mod'])
                    ballot_id = self._db.execute(('INSERT INTO ballots VALUES '
                                                  '(NULL, ?, ?, ?, ?)'),
                                                 (vote['id'],
                                                  data['author'][0],
                                                  checksum,
                                                  data['fingerprint'][0])) \
                                        .lastrowid
                    self._db.executemany(('INSERT INTO entries VALUES '
                                          '(?, ?, ?)'),
                                         [(ballot_id,
                                           propositions[i]['id'],
                                           data['votes'][i])
                                          for i in range(len(propositions))])
                    self._db.executemany(('UPDATE propositions '
                                          'SET score=? WHERE id=?'),
                                         [(self._sum_votes(
                                             [propositions[i]['score'],
                                              data['votes'][i]],
                                             vote['mod']),
                                           propositions[i]['id'])
                                          for i in range(len(propositions))])
                    self._db.commit()
                    self._see_other('/' + self._key + '/ballot/' +
                                    str(ballot_id) + ':' + checksum[0:8])
                except:
                    self._error('Database failure.')

    def do_OPTIONS (self):
        self.send_response(200)
        self.send_header('Allow', 'GET, POST, OPTIONS')
        self.send_header('Accept-Charset', 'utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Method', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With')
        self.send_header('Access-Control-Request-Headers', 'Content-Length')
        self.send_header('Content-Length', 0)
        self.end_headers()

    def do_GET (self):
        self._parse_route()
        if self._key == '':
            self._ok(self.version_string())
        else:
            self._db = sqlite3.connect(self._db_file)
            self._db.row_factory = sqlite3.Row
            self._vote = self._db.execute(('SELECT id, title, closing, expiry '
                                           'FROM votes '
                                           'WHERE key=? AND expiry>?'),
                                    (self._key, int(time()))).fetchone()
            if self._vote is None:
                self._not_found('Invalid vote.')
            else:
                if   self._action == '':        self._do_info()
                elif self._action == 'ballot':  self._do_ballot()
                elif self._action == 'ballots': self._do_ballots()
                elif self._action == 'results': self._do_results()
                else: self._not_found('Invalid resource.')
            self._db.close()

    def do_POST (self):
        self._parse_route()
        if 'Content-Length' not in self.headers:
            self._length_required('HTTP Content-Length header is missing.')
        else:
            content_length = int(self.headers['Content-Length'])
            content = self.rfile.read(content_length).decode('utf-8')
            data = urllib.parse.parse_qs(content)
            self._db = sqlite3.connect(self._db_file)
            self._db.row_factory = sqlite3.Row
            if self._key == '': self._do_create_vote(data)
            else: self._do_cast_ballot(data)
            self._db.close()

    def _sum_votes (self, votes, mod):
        return b64e(reduce(mul, [b64d(v) for v in votes]) % b64d(mod))
