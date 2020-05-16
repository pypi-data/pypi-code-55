'''
这是一个爬有道的API小程序
我居然成功了！
'''
__all__ = ['mainAPI']
from requests import post as _post
from hashlib import md5 as _md5
from time import time as _time
from random import randint as __RDI

def _nmd5(s):
    return _md5(s.encode()).hexdigest()

def _gents():
    return str(int(round(_time(), 3)*1000))

def mainAPI(s, fr='AUTO', to='AUTO'):
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'Host': 'fanyi.youdao.com',
        'Origin': 'http://fanyi.youdao.com',
        'Referer': 'http://fanyi.youdao.com/',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4133.0 Safari/537.36 Edg/84.0.508.0'
    }
    ts = _gents()
    headers['Cookie'] = f'OUTFOX_SEARCH_USER_ID=-2117617218@10.108.160.101; JSESSIONID=aaaB8nmy0x15aeqDporix; OUTFOX_SEARCH_USER_ID_NCOO=1552295287.6610472; ___rl__test__cookies={ts}'
    data = {
        'i': s,
        'from': fr,
        'to': to,
        'smartresult': 'dict',
        'client': 'fanyideskweb',
        'doctype': 'json',
        'version': '2.1',
        'keyfrom': 'fanyi.web',
        'action': 'FY_BY_REALTlME'
    }
    data['ts'] = str(ts)
    data['bv'] = _nmd5('5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4133.0 Safari/537.36 Edg/84.0.508.0')
    data['salt'] = ts+str(__RDI(3, 6))
    data['sign'] = _nmd5('fanyideskweb'+s+data['salt']+'Nw(nmmbP%A-r6U3EUn]Aj')
    rex = _post('http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule', data=data, headers=headers)
    return rex.text
