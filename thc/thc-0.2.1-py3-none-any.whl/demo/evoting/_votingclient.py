import json
import nacl.hash
import nacl.secret
import requests
from ...thc import THC
from ...utils import prime
from ...crypto.paillier import Paillier, Sum
from ._b64 import *

class Error (Exception):

    def __init__ (self, message):
        self.message = message

class VotingClient:

    def __init__ (self, srv, p, q, r):
        if srv[0:8].lower() != 'https://' and srv[0:7].lower() != 'http://':
            srv = 'https://' + srv
        if srv[-1] != '/': srv += '/'
        try:
            res = requests.get(srv, timeout=3.0)
        except requests.exceptions.SSLError:
            srv = 'http://' + srv[8:]
            res = requests.get(srv, timeout=3.0)
        if res.status_code != requests.codes.ok or \
           res.json() != 'THC demo e-voting server':
            return None
        self._srv = srv
        self._p = p
        self._q = q
        self._r = r
        self._key = self._vote_id()
        self._vote = self._srv + self._key
        self._cs = self._create_box()
        self._hcs = Paillier(p, q)
        self._thc = THC(self._hcs, Sum(), self._r)

    @staticmethod
    def new (srv):
        try:
            p = prime(1024)
            while True:
                q = prime(1024)
                if p != q:
                    break
            r = prime(32)
            return VotingClient(srv, p, q, r)
        except:
            return None

    @staticmethod
    def from_file (path):
        try:
            f = open(path, 'r')
            d = [l.strip() for l in f.readlines()[1:]]
            f.close()
            return VotingClient(d[0], b64d(d[1]), b64d(d[2]), b64d(d[3]))
        except:
            return None

    def dump_vote (self):
        vote = '# Secret THC vote file, '
        vote += 'only share it with other vote participants!\n'
        vote += self._srv + '\n'
        vote += b64e(self._p) + '\n'
        vote += b64e(self._q) + '\n'
        vote += b64e(self._r) + '\n'
        return vote

    def export_vote (self, path):
        try:
            f = open(path, 'w')
            f.write(self.dump_vote())
            f.close()
            return True
        except:
            return False

    def _vote_id (self):
        k = self._p * self._q + self._r
        digest = nacl.hash.sha256(k.to_bytes((k.bit_length() + 7) // 8, 'big'),
                                  encoder=nacl.encoding.URLSafeBase64Encoder)
        return digest.decode()

    def _create_box (self):
        k = (self._p - 1) * (self._q - 1) + self._r
        kl = nacl.secret.SecretBox.KEY_SIZE * 8
        mask = int('1' * kl, 2)
        key = 0
        while k.bit_length() > kl:
            t = k & mask
            key ^= t
            k >>= kl
        while key.bit_length() < kl:
            key <<= 1
        secret = key.to_bytes(nacl.secret.SecretBox.KEY_SIZE, 'big')
        return nacl.secret.SecretBox(secret)

    def _encrypt (self, data):
        return self._cs.encrypt(data.encode(),
                                encoder=nacl.encoding.URLSafeBase64Encoder)

    def _decrypt (self, data):
        return self._cs.decrypt(data,
                                encoder=nacl.encoding.URLSafeBase64Encoder) \
                        .decode('utf-8')

    def get_info (self, res=None):
        try:
            return self._info
        except AttributeError:
            res = requests.get(self._vote, timeout=3.0) if res is None else res
            if res.status_code == requests.codes.ok:
                info = res.json()
                self._info = {
                    'title': self._decrypt(info['title']),
                    'closing': info['closing'],
                    'expiry': info['expiry'],
                    'propositions': [self._decrypt(p)
                                     for p in info['propositions']]
                }
                return self._info
            raise Error(res.json())

    def _ballot (self, ballot):
        fingerprint = json.loads(self._decrypt(ballot['fingerprint']))
        return {
            'author': self._decrypt(ballot['author']),
            'count': self._thc.verify(b64d(ballot['checksum']),
                                      Sum().local(self._r, fingerprint)),
            'fingerprint': fingerprint
        }

    def get_ballot (self, ballot_id):
        res = requests.get(self._vote + '/ballot/' + str(ballot_id),
                           timeout=3.0)
        if res.status_code == requests.codes.ok:
            return self._ballot(res.json())
        raise Error(res.json())

    def get_ballots (self):
        res = requests.get(self._vote + '/ballots', timeout=3.0)
        if res.status_code == requests.codes.ok:
            return [self._ballot(ballot) for ballot in res.json()]
        raise Error(res.json())

    def get_results (self, ballots=None):
        ballots = self.get_ballots() if ballots is None else ballots
        if not ballots:
            return False
        res = requests.get(self._vote + '/results', timeout=3.0)
        if res.status_code == requests.codes.ok:
            results = res.json()
            for i in range(len(results)):
                score = self._thc.verify(b64d(results[i]['score']),
                                         Sum().local(self._r,
                                                     [ballot['fingerprint'][i]
                                                      for ballot in ballots]))
                results[i]['score'] = score
            return [{
                'proposition': self._decrypt(result['proposition']),
                'score': result['score']
            } for result in results]
        raise Error(res.json())

    def cast_ballot (self, author, ballot):
        votes = [self._hcs.encrypt(vote) for vote in ballot]
        fingerprint = [v % self._r for v in votes]
        res = requests.post(self._vote, timeout=3.0, data={
            'author': self._encrypt(author),
            'votes': [b64e(v) for v in votes],
            'fingerprint': self._encrypt(json.dumps(fingerprint))
        })
        if res.status_code == requests.codes.ok:
            return self._ballot(res.json())
        raise Error(res.json())

    def create_vote (self, title, closing, expiry, propositions):
        res = requests.post(self._srv, timeout=3.0, data={
            'key': self._key,
            'mod': b64e(self._hcs.get_modulus() * self._r),
            'title': self._encrypt(title),
            'closing': closing,
            'expiry': expiry,
            'propositions': [self._encrypt(proposition)
                             for proposition in propositions]
        })
        if res.status_code == requests.codes.ok:
            return self.get_info(res)
        raise Error(res.json())
