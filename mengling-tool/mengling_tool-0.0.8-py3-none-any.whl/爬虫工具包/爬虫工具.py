from urllib import request
import re
import time
import requests
import json
import socket
from bs4 import BeautifulSoup
import sqlite3
import os
import sys
import ctypes.wintypes
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import mengling_tool.异步工具 as yb
from lxml import etree

cro_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/51.0.2704.63 Safari/ 537.36'}

fi_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0"}


# 字符串转headers
def getHeaders_str(string):
    headers = dict()
    lines = string.split('\n')
    for line in lines:
        line = line.strip()
        if line != '':
            key, value = str(re.match('.+?:', line).group()[0:-1]), str(re.search(':.+', line).group()[1:])
            headers[key] = value.strip()
    return headers


'''用于解密encrypted_value的配套方法'''


def __dpapi_decrypt(encrypted):
    class DATA_BLOB(ctypes.Structure):
        _fields_ = [('cbData', ctypes.wintypes.DWORD),
                    ('pbData', ctypes.POINTER(ctypes.c_char))]

    p = ctypes.create_string_buffer(encrypted, len(encrypted))
    blobin = DATA_BLOB(ctypes.sizeof(p), p)
    blobout = DATA_BLOB()
    retval = ctypes.windll.crypt32.CryptUnprotectData(
        ctypes.byref(blobin), None, None, None, None, 0, ctypes.byref(blobout))
    if not retval:
        raise ctypes.WinError()
    result = ctypes.string_at(blobout.pbData, blobout.cbData)
    ctypes.windll.kernel32.LocalFree(blobout.pbData)
    return result


def __aes_decrypt(encrypted_txt):
    with open(os.path.join(os.environ['LOCALAPPDATA'],
                           r"Google\Chrome\User Data\Local State"), encoding='utf-8', mode="r") as f:
        jsn = json.loads(str(f.readline()))
    encoded_key = jsn["os_crypt"]["encrypted_key"]
    encrypted_key = base64.b64decode(encoded_key.encode())
    encrypted_key = encrypted_key[5:]
    key = __dpapi_decrypt(encrypted_key)
    nonce = encrypted_txt[3:15]
    cipher = Cipher(algorithms.AES(key), None, backend=default_backend())
    cipher.mode = modes.GCM(nonce)
    decryptor = cipher.decryptor()
    return decryptor.update(encrypted_txt[15:])


def __chrome_decrypt(encrypted_txt):
    if sys.platform == 'win32':
        try:
            if encrypted_txt[:4] == b'x01x00x00x00':
                decrypted_txt = __dpapi_decrypt(encrypted_txt)
                return decrypted_txt.decode()
            elif encrypted_txt[:3] == b'v10':
                decrypted_txt = __aes_decrypt(encrypted_txt)
                return decrypted_txt[:-16].decode()
        except WindowsError:
            return None
    else:
        raise WindowsError


# 获取当地谷歌浏览器的cookies文件数据
def getLocalChromeCookieList(*domains):
    cookiepath = os.environ['LOCALAPPDATA'] + r"\Google\Chrome\User Data\Default\Cookies"
    sql = "select host_key,name,encrypted_value from cookies"
    if len(domains) > 0:
        sql += " where "
        for domain in domains:
            sql += "host_key='%s' or " % domain
        sql = str(sql[:-4])
    cookielist = []
    with sqlite3.connect(cookiepath) as conn:
        cu = conn.cursor()
        cls = cu.execute(sql).fetchall()
        lie0 = cu.description  # 获取列
        # 记录列名
        if lie0 != None:
            lies = [lie[0] for lie in lie0]
        else:
            lies = []
        for ts in cls:
            cookies = dict()
            for i in range(len(ts)):
                if lies[i] == 'encrypted_value':  # 加密处理
                    cookies[lies[i]] = __chrome_decrypt(ts[i])
                    # 记录到value值
                    cookies['value'] = __chrome_decrypt(ts[i])
                elif lies[i] == 'value':  # 原value不记录
                    continue
                elif lies[i] == 'host_key':
                    cookies['domain'] = ts[i]
                else:
                    cookies[lies[i]] = ts[i]
            cookielist.append(cookies)
    return cookielist


# 获取原网页,动态网址不能直接获取
def getHtml_get(url, **args):
    global cro_headers
    headers = args.get('headers', cro_headers)
    timeout = args.get('timeout', 20)
    encoding = args.get('encoding', None)
    proxies = args.get('proxies', None)
    valuetype = args.get('valuetype', 'text')
    if headers != cro_headers:
        if 'User-Agent' not in headers.keys():
            headers['User-Agent'] = cro_headers['User-Agent']
    try:

        r = requests.get(url, headers=headers, proxies=proxies, timeout=timeout)
        r.raise_for_status()  # 如果状态不为200，返回异常
        # 原始对象
        if valuetype == 'text':
            r.encoding = r.apparent_encoding if encoding == None else encoding
            return r.text
        elif valuetype == 'content':
            return r.content
        else:
            return r
    except Exception as e:
        print(e)
        return ""


def getHtml_get_threadPool(urls, n, **args):
    sum = dict()
    values = [(url, args) for url in urls]
    ci = args.get('ci', 3)
    sleeptime = args.get('sleeptime', 1)

    def temp_get(url, args):
        nonlocal ci
        nonlocal sum
        nonlocal sleeptime
        for i in range(ci):
            try:
                html = getHtml_get(url, **args)
                if html == '':
                    raise Exception()
                else:
                    break
            except:
                time.sleep(sleeptime)
                continue
            time.sleep(sleeptime)
        if html == '': print('获取源码失败：', url)
        sum[url] = html

    pool, ps = yb.threadPool(n, temp_get, values)
    pool.shutdown()
    return sum


def getHtml_session(url, **args):
    global cro_headers
    headers = args.get('headers', cro_headers)
    timeout = args.get('timeout', 20)
    encoding = args.get('encoding', None)
    proxies = args.get('proxies', None)
    ifobject = args.get('ifobject', False)
    if headers != cro_headers:
        if 'User-Agent' not in headers.keys():
            headers['User-Agent'] = cro_headers['User-Agent']
    try:
        session = requests.session()
        html = session.get(url, headers=headers, proxies=proxies, timeout=timeout)
        # 原始对象
        if ifobject: return html
        html.encoding = html.apparent_encoding if encoding == None else 'utf-8'
        return html.text
    except Exception as e:
        print(e)
        return ""


def getHtml_post(url, data, **args):
    global cro_headers
    headers = args.get('headers', cro_headers)
    timeout = args.get('timeout', 20)
    encoding = args.get('encoding', 'utf-8')
    proxies = args.get('proxies', None)
    ifobject = args.get('ifobject', False)
    if headers != cro_headers:
        if 'User-Agent' not in headers.keys():
            headers['User-Agent'] = cro_headers['User-Agent']
    try:
        html = requests.post(url, headers=headers, data=data, proxies=proxies, timeout=timeout)
        # 原始对象
        if ifobject: return html
        html.encoding = encoding
        return html.text
    except Exception as e:
        print(e)
        return ""


def getHtml_open(url, **args):
    global cro_headers
    headers = args.get('headers', cro_headers)
    timeout = args.get('timeout', 20)
    proxies = args.get('proxies', None)
    ifobject = args.get('ifobject', False)
    if headers != cro_headers:
        if 'User-Agent' not in headers.keys():
            headers['User-Agent'] = cro_headers['User-Agent']
    try:
        # 查看路径是否存在
        req = request.Request(url, headers=cro_headers)
        data = request.urlopen(req)
        # 原始对象
        if ifobject:
            return data
        else:
            return data.read()
    except Exception as e:
        print("出错：", e)
        return ''


# 设置获取数据类型
def getDatas(yuan):
    # 获取所有链接
    pattern = '(https?://[^\s)";]+(\.(\w|/)*))'
    link = re.compile(pattern).findall(yuan)
    # 将文件链接去重并统一输出为列表格式
    return list(set([li[0] for li in link]))


# 下载链接至本地
def downData(url, path, newfullname, **args):
    global cro_headers
    headers = args.get('headers', cro_headers)
    timeout = args.get('timeout', 30)
    proxies = args.get('proxies', None)
    tz = args.get('tz', True)
    if headers != cro_headers:
        if 'User-Agent' not in headers.keys():
            headers['User-Agent'] = cro_headers['User-Agent']
    socket.setdefaulttimeout(timeout)  # 解决下载不完全问题且避免陷入死循环
    try:
        # 查看路径是否存在
        if not os.path.exists(path):  os.makedirs(path)
        if proxies != None:
            # 更改ip地址用于下载
            # 创造处理器
            proxy_head = request.ProxyHandler()
            # 创建opener
            opener = request.build_opener(proxy_head)
        else:
            opener = request.build_opener()
        # 载入头文件模拟浏览器行为
        headers = [(key, headers[key]) for key in headers.keys()]
        opener.addheaders = headers
        request.install_opener(opener)
        # 开始下载
        request.urlretrieve(url, path + newfullname)
    except socket.timeout:
        if tz:
            print('下载超时！')
            print(url)
        raise socket.timeout
    except Exception as e:
        if tz:
            print("下载出错：", e)
            print(url)
        raise e


# 多线程下载
def downData_threadPool(urls, n, path, format, **args):
    def dfunc(urls, index, n, path, format, args):
        length = len(urls)
        ci = 0
        head_str = args.get('head_str', '')
        ci_max = args.get('ci_max', 3)
        while True:
            if index >= length: break
            try:
                downData(urls[index], path, ''.join([head_str, str(index), format]), **args)
                index += n
                ci = 0
            except Exception as e:
                ci += 1
                if ci < ci_max:
                    print(e)
                    print('丢失：', urls[index])
                    print('重新下载，先休息...', ci)
                    time.sleep(3)
                else:
                    print('下载失败：', urls[index])
                    index += n
                    ci = 0
            time.sleep(0.5)

    pool, ps = yb.threadPool(6, dfunc, [(urls, i, n, path, format, args) for i in range(n)])
    pool.shutdown()


# 下载链接至本地,写入式
def downData_w(url, path, newfullname, **args):
    global cro_headers
    headers = args.get('headers', cro_headers)
    timeout = args.get('timeout', 30)
    proxies = args.get('proxies', None)
    tz = args.get('tz', True)
    if headers != cro_headers:
        if 'User-Agent' not in headers.keys():
            headers['User-Agent'] = cro_headers['User-Agent']
    try:
        # 查看路径是否存在
        if not os.path.exists(path):  os.makedirs(path)
        req = request.Request(url, headers=cro_headers, timeout=timeout)
        data = request.urlopen(req).read()
        with open(path + newfullname, 'wb') as f:
            f.write(data)
    except Exception as e:
        if tz: print("下载出错：", e)
        raise e


def getSoup(html, BeautifulSoup_value='html.parser'):
    soup = BeautifulSoup(html, BeautifulSoup_value)
    return soup


def getXpath(html, xpath_str):
    return etree.HTML(html).xpath(xpath_str)


def getJson(json_str):
    return json.loads(json_str)
