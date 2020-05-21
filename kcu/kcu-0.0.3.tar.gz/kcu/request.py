from typing import Dict, Optional
import time, requests, os

from fake_useragent import FakeUserAgent

Response = requests.Response

def download(
    url: str,
    path: str,
    max_request_try_count: int = 3,
    sleep_time: float = 2.5,
    debug: bool = False
) -> bool:
    current_try_count = 0

    while current_try_count < max_request_try_count:
        current_try_count += 1

        if debug:
            print(url + ' | ' + str(current_try_count) + '/' + str(max_request_try_count))
        
        res = __download(
            url,
            path,
            debug=debug
        )

        if res:
            return True
        
        time.sleep(sleep_time)
    
    return False

def __download(
    url: str, 
    path: str,
    debug: bool = False
) -> bool:
    import urllib

    try:
        urllib.request.urlretrieve(url, path)

        return os.path.exists(path)
    except Exception as e1:
        if debug:
            print(e1)
        
        try:
            os.remove(path)
        except Exception as e2:
            if debug:
                print(e2)
        
        return False

def request(
    url: str,
    headers: Dict = None,
    max_request_try_count: int = 10,
    sleep_time: float = 2.5,
    debug: bool = False,
    fake_useragent: bool = False
) -> Optional[Response]:
    current_try_count = 0

    while current_try_count < max_request_try_count:
        current_try_count += 1
        
        if debug:
            print(url + ' | ' + str(current_try_count) + '/' + str(max_request_try_count))

        resp = __request(
            url,
            headers=headers,
            debug=debug,
            fake_useragent=fake_useragent
        )

        if resp is not None:
            return resp
        
        time.sleep(sleep_time)
    
    return None

def __request(
    url: str,
    headers: Dict = None,
    debug: bool = False,
    fake_useragent: bool = False
) -> Optional[Response]:
    if headers is None:
        headers = {}
    
    ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:74.0) Gecko/20100101 Firefox/74.0'

    if fake_useragent:
        ua = FakeUserAgent().random
    
    headers = __headers_by_optionally_setting(headers, {
        'User-Agent':ua,
        'Accept':'*/*',
        'Cache-Control':'no-cache',
        'Accept-Encoding':'gzip, deflate, br',
        'Connection':'keep-alive'
    })

    try:
        resp = requests.get(url, headers=headers)

        if resp is None:
            if debug:
                print('ERROR: Resp is None')
            
            return None

        if resp.status_code != 200:
            if debug:
                print('ERROR:', resp)
            
            return None
        
        return resp
    except Exception as e:
        if debug:
            print('ERROR:', e)

        return None

def __headers_by_optionally_setting(
    headers: Dict, 
    keys_values: Dict
) -> Dict:
    for key, value in keys_values.items():
        if key not in headers:
            headers[key] = value
    
    return headers