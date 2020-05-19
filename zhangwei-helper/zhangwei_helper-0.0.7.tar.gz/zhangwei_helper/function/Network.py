# -*- coding:utf-8 -*-
'''
网络相关操作
extract_protocol_from_url(url)：获得协议http或者https
extract_host_from_url(url)：获得host
extract_base_url_from_url(url)：获得基础url  https://github.com
gen_proxies_from_ip(ip): 根据IP生成request/request_html需要的代理
detect_if_need_proxy(url): Boolean:是否需要代理
detect_if_proxy_usable(proxies, timeout=5, url='https://www.baidu.com'）：Boolean：代理是否有效
detect_url_exist(url, proxies, headers): url是否存在（返回404）
send_request_get_response(**args): request_html或者error。同步获得页面html
async_send_request_get_response(**args): request_html或者error。异步获得页面html
download_file(url,save_path): Error(下载失败）；None（下载成功）
download_unzip_chrome_driver:
download_unzip_firefox_driver:
'''
from urllib.parse import urlparse
import os

# requests 用来为requests_html提供Error
import requests
from requests_html import HTMLSession
from requests_html import AsyncHTMLSession

import zhangwei_helper.const.Const as self_const
import zhangwei_helper.enum.SelfEnum as self_enum
import zhangwei_helper.function.Os as self_os
import zhangwei_helper.function.Software as self_software


def extract_protocol_from_url(url):
    '''

    :param url:
    :return: http或者https
    '''
    return urlparse(url).scheme


def extract_host_from_url(url):
    '''

    :param url:
    :return: github.com
    '''
    return urlparse(url).netloc


def extract_base_url_from_url(url):
    return urlparse(url).scheme+'://'+urlparse(url).netloc


def gen_proxies_from_ip(ip):
    return None if ip == "" else {'http':ip,'https':ip}


def detect_if_need_proxy(url):
    try:
        HTMLSession().get(url, headers=self_const.HEADER, timeout=10)
    except requests.exceptions.Timeout as e:
        print('不通过代理发起的请求超时，需要使用代理')
        return True
    except requests.exceptions.ConnectionError as e:
        print('不通过代理发起的请求连接错误，需要使用代理')
        return True
    return False


def detect_if_proxy_usable(proxies, timeout=5, url='https://www.baidu.com'):
    try:
        # ssl._create_default_https_context = ssl._create_unverified_context
        HTMLSession().get(url, headers=self_const.HEADER,
                          proxies=proxies, timeout=timeout)

        # if r.status_code != 200:
        #     return False
    except requests.exceptions.Timeout as e:
        print('代理无效：超时')
        return False
    except requests.exceptions.ProxyError as e:
        print('代理无效：代理错误')
        return False
    except requests.exceptions.ConnectionError as e:
        print('代理无效：连接错误')
        return False
    return True


def detect_url_exist(url, proxies, headers=self_const.HEADER):
    '''
    检测url是否存在（是否返回404）
    :param url:
    :param proxies:
    :param headers:
    :return:
    '''
    r = HTMLSession().get(url, headers=headers, proxies=proxies)
    return r.status_code != 404


def send_request_get_response(url, if_use_proxy=False, proxies=None,
                              header=self_const.HEADER,
                              force_render=False):
    '''
    为了和async_send_request_get_response的参数保持一致，取消force_render
    :param url:
    :param if_use_proxy:  boolean
    :param proxies: dict，如果if_need_proxy为true，传入代理
    :param header: request的header
    :param force_render: 是否要进行render，默认True。如果是静态页面，无需render
    :return:
    '''
    # ssl._create_default_https_context = ssl._create_unverified_context
    if if_use_proxy:
        r = HTMLSession().get(url, headers=header, proxies=proxies,
                              timeout=5)
    else:
        r = HTMLSession().get(url, headers=header, timeout=2)

    if r.status_code != 200:
        # print('错误代码 %s' % r.status_code)
        raise requests.exceptions.HTTPError('错误代码 %s' % r.status_code)

    if force_render:
        r.html.render()
    return r


async def async_send_request_get_response(url, if_use_proxy=False, proxies=None,
                                          header=self_const.HEADER,
                                          force_render=False):
    '''
    requests-html的异步模式下，必须返回await asession.get
    :param url: request的地址
    :param if_use_proxy:
    :param proxies: 用来来接待代理网页的代理
    :param header:
    :param force_render: 是否要进行render，默认True。如果是静态页面，无需render
    :return: 无
    '''
    if if_use_proxy:
        r = await AsyncHTMLSession().get(url, headers=header, proxies=proxies,
                                  timeout=5)
    else:
        r = await AsyncHTMLSession().get(url, headers=header, timeout=2)

    if force_render:
        await r.html.arender()
    return r


def download_file(url, save_path, headers=self_const.HEADER, proxies=None):
    '''
    下载文件
    :param url:
    :param save_path:
    :return: Error（下载失败）；None（下载成功）
    '''
    try:
        if proxies is not None:
            r = requests.get(url, proxies=proxies, headers=headers)
        else:
            r = requests.get(url, headers=headers)
        with open(save_path, "wb") as code:
            code.write(r.content)
    except Exception as e:
        raise e

    return None


def download_unzip_firefox_driver(python_dir, browser_ver, os_type,os_bits,proxies=None,headers=None):
    '''
    下载浏览器对应的driver到python目录下，然后解压
    :param python_dir:
    :param browser_ver: str，通过get_firefox_version或者get_chrome_version获得
    :param os_type:enum，Win或者Linux
    :param os_bits：enum，32或64bit
    :param proxies:下载文件需要的代理
    :param headers：下载文件需要的header
    :return:
    '''

    # firefox的版本必须大于60
    if int(browser_ver.split('.')[0]) < 60:
        raise EnvironmentError("当前Firefox版本过低，请升级到60或者以上版本")
    # 根据os_type和os_bits确定url
    url_dict ={
        'WindowsWin32':'https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-win32.zip',
        'WindowsWin64': 'https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-win64.zip',
    }
    if os_type == self_enum.OsType.Linux:
        raise EnvironmentError("当前尚不支持Linux")

    url = url_dict[os_type.name + os_bits.name]
    file_name = url.split('/')[-1]
    save_path = os.path.join(python_dir, file_name)
    if os.path.exists(save_path) and self_software.is_valida_zip_file(save_path):
        self_software.unzip_file(file_path=save_path, save_path=python_dir)
        return
    # print('开始时下载')
    # 检测是否需要代理
    base_url = extract_base_url_from_url(url)
    if detect_if_need_proxy(url=base_url):
        if proxies is None:
            raise ValueError("需要使用代理，但是未设置代理")
        # 检测代理是否可用
        if not detect_if_proxy_usable(proxies=proxies, timeout=5, url=base_url):
            raise ValueError("设置的代理无法连接%s" % base_url)
        # 代理下载
        download_file(url=url, save_path=save_path, proxies=proxies,headers=headers)
    else:
        # 非代理下载
        download_file(url=url, save_path=save_path)

    self_software.unzip_file(file_path=save_path, save_path=python_dir)


def download_unzip_chrome_driver(python_dir, browser_ver, os_type,os_bits,proxies=None,headers=None):
    '''
    下载浏览器对应的driver到python目录下，然后解压
    :param python_dir:
    :param browser_ver: str，通过get_firefox_version或者get_chrome_version获得
    :param os_type:enum，Win或者Linux
    :param os_bits：enum，32或64bit
    :param proxies:下载文件需要的代理
    :param headers：下载文件需要的header
    :return:
    '''

    # chrome的版本必须大于70
    if int(browser_ver.split('.')[0]) < 70:
        raise EnvironmentError("当前Chrome版本过低，请升级到70或者以上版本")

    if os_type == self_enum.OsType.Linux:
        raise EnvironmentError("当前尚不支持Linux")

    url = 'https://npm.taobao.org/mirrors/chromedriver/%s/chromedriver_win32.zip' % browser_ver
    file_name = url.split('/')[-1]
    save_path = os.path.join(python_dir, file_name)
    if os.path.exists(save_path) and self_software.is_valida_zip_file(save_path):
        self_software.unzip_file(file_path=save_path, save_path=python_dir)
        return
    # print(url)
    # 检测是否需要代理
    if detect_if_need_proxy(url):
        if proxies is None:
            raise ValueError("需要使用代理，但是未设置代理")
        # 检测代理是否可用
        base_url = extract_base_url_from_url(url)
        if not detect_if_proxy_usable(proxies=proxies, timeout=5, url=base_url):
            raise ValueError("设置的代理无法连接%s" % base_url)
        # 代理下载
        if not detect_url_exist(url=url,proxies=proxies,headers=headers):
            raise ValueError("指定的下载链接%s不存在，Chrome %s可能不是稳定版" % (url, browser_ver))
        download_file(url=url, save_path=save_path, proxies=proxies,headers=headers)
    else:
        # 非代理下载
        if not detect_url_exist(url=url,proxies=proxies,headers=headers):
            raise ValueError("指定的下载链接%s不存在，Chrome %s可能不是稳定版" % (url, browser_ver))
        download_file(url=url, save_path=save_path)

    self_software.unzip_file(file_path=save_path, save_path=python_dir)


if __name__ == '__main__':
    pass
    # proxies= gen_proxies_from_ip('87.254.212.121:8080')
    # # download_file(url='http://selenium-release.storage.googleapis.com/3.141/IEDriverServer_x64_3.141.5.zip',
    # #               save_path='d:\\IEDriverServer_x64_3.141.5.zip',proxies=proxies)
    #
    # python_dir=self_software.check_minimum_python_version()
    # chrome_ver = self_software.get_chrome_version()
    # download_unzip_chrome_driver(python_dir=python_dir,  browser_ver=chrome_ver,
    #                       os_type=self_enum.OsType.Windows,os_bits=self_enum.WindowsBits.Win64, proxies=proxies)