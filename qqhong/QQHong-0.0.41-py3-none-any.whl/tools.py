#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: QQHong

"""
一些较为零散的常用函数组成的工具模块
"""

import os
import io
import re
import bson
import hmac
import json
import time
import random
import string
import base64
import socket
import hashlib
import zipfile
import requests
import itertools
import subprocess
import multiprocessing
from urllib import parse
from wsgiref.simple_server import make_server

import exrex
import pymongo
from PIL import Image
from PIL import ImageChops
from Crypto.Cipher import AES
from selenium import webdriver


def get_headers(is_random=None, headers=None):
    """
    获取HTTP的请求头
    :param is_random: 请求头的值是否随机
    :param headers: 指定的headers字段s
    :return:
    """
    default_headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:57.0) Gecko/20100101 Firefox/57.0",
        "Referer": "https://www.google.com/",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache"
    }

    if is_random:
        resource = os.path.join(os.path.dirname(__file__), "./resource/headers")
        for header in ["User-Agent"]:
            default_headers[header] = random.choice(open(os.path.join(resource, header)).readlines()).strip()

    if headers:
        default_headers.update(headers)

    return default_headers


def get_paths(path, recursive=False):
    """
    获取文件夹下的所有文件的路径
    :param path: 文件夹的路径
    :param recursive: 是否递归该文件夹
    :return: 所有文件路径组成的列表
    """
    paths = []
    if os.path.isdir(path):
        if recursive:
            for root, dirs, filenames in os.walk(path):
                for filename in filenames:
                    paths.append(os.path.join(root, filename))
        else:
            for filename in os.listdir(path):
                paths.append(os.path.join(path, filename))
    else:
        paths.append(path)
    return paths


def get_hashs(path, hash_algorithms=None):
    """
    计算文件的hash值
    :param path: 文件路径
    :param hash_algorithms: 需要的哈希算法所组成的列表，例如：["md5"]
    :return: hash 字段及值组成的字典
    """
    if hash_algorithms is None:
        hash_algorithms = ["md5", "sha1", "sha256"]
    hash_values = {}
    content = open(path, "rb").read()
    for hash_algorithm in hash_algorithms:
        hash_values[hash_algorithm] = getattr(hashlib, hash_algorithm)(content).hexdigest()
    return hash_values


def file_split(path, size=1024*1024*1024):
    """
    对文件(通常为大文件)进行分割
    :param path: 文件路径
    :param size: 分割后每一份文件的大小，单位为byte
    :return:
    """
    with open(path, "rb") as src:
        index = 0
        if size > 1024*104*1024:
            src.read(size)
        content = src.read(size)
        while content != b"":
            open(path + "." + str(index), "wb").write(content)
            index += 1
            content = src.read(size)


def file_merge(path):
    """
    对文件进行合并
    :param path: 文件路径
    :return:
    """
    with open(path, "wb") as f:
        index = 0
        src = path + "." + str(index)
        while os.path.exists(src):
            content = open(path + "." + str(index), "rb").read()
            f.write(content)
            index += 1
            src = path + "." + str(index)


def duplicate_removal(old_list, sort=False):
    """
    对列表去重
    :param old_list: 原有列表
    :param sort: 是否保持原有排序
    :return: 去重后的新列表
    """
    new_list = list(set(old_list))
    if sort:
        new_list.sort(key=old_list.index)
    return new_list


def duplicate_removal_file(old_file_path, new_file_path, sort=False):
    """
    对文件内容按行进行去重
    :param old_file_path: 需去重的文件路径
    :param new_file_path: 去重后文件的保存路径
    :param sort: 是否需要保持原有排序，默认不保存
    :return:
    """
    lines = [line for line in open(old_file_path, encoding="utf-8").readlines()]
    lines = duplicate_removal(lines, sort)
    open(new_file_path, "w", encoding="utf-8").write("".join(lines))


def start_http_sever_by_wsgi(port=80, root_dir="."):
    """
    WSGI构建的简要的文件下载服务器(不考虑性能|安全等问题，仅供自身使用，切勿对外提供服务)
    :param port: 端口
    :param root_dir: 根目录
    :return:
    """
    # 列目录时展示的文件夹、文件的图标及默认返回的响应体(定义编码方式)
    folder_img = "data:image/gif;base64,R0lGODlhEAAQALMAAJF7Cf8A//zOLQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" \
                 "AAAAAAACH5BAEAAAEALAAAAAAQABAAAAQqMMhJqwQ42wmE/8AWdB+YaWSZqmdWsm9syjJGx/YN6zPv5T4gr0UkikQRADs="
    file_img = "data:image/gif;base64,R0lGODlhEAAQALMAAAAAAIAAAACAAICAAAAAgIAAgACAgMDAwICAgP8AAAD/AP//AAAA//8A/wD" \
               "//////yH5BAEAAA0ALAAAAAAQABAAAAQwsDVEq5V4vs03zVrHIQ+SkaJXYWg6sm5nSm08h3EJ5zrN9zjbLneruYo/JK9oaa4iADs="
    default_body = '<meta charset="UTF-8">'
    # 每次请求所调用的函数

    def application(environ, start_response):
        # Wsgi会对值进行latin1解码，导致中文异常，故此先用latin1编码再用utf-8进行解密
        requests_path = environ['PATH_INFO'].encode("latin1").decode("utf-8")
        local_path = os.path.join(root_dir + requests_path)
        headers = {
            "Content-Type": "text/html"
        }
        if os.path.exists(local_path):
            # 文件直接提供下载
            if os.path.isfile(local_path):
                body = open(local_path, "rb").read()
                headers.update({
                    "Content-Type": "application/octet-stream",
                    "Content-Length": str(len(body))
                })
                start_response('200 OK', list(headers.items()))
            # 文件夹则列出目录
            elif os.path.isdir(local_path):
                start_response('200 OK', list(headers.items()))
                body = default_body + '<style>a {text-decoration: none}</style>'
                dirs, files, show = '', '', '<img src="{}"> <a href="{}">{}<a><br/>'
                for each in os.listdir(local_path):
                    one = os.path.join(local_path, each)
                    if os.path.isdir(one):
                        dirs += show.format(folder_img, os.path.join(requests_path, each), each)
                    else:
                        files += show.format(file_img, os.path.join(requests_path, each), each)
                body += dirs + files
            else:
                start_response('500 Internal Server Error', list(headers.items()))
                body = default_body + "未知错误"
        else:
            start_response('404 Not Found', list(headers.items()))
            body = default_body + "页面不存在"
        if type(body) != bytes:
            body = body.encode("utf-8")
        return [body]
    # 启动WSGI文件服务器
    httpd = make_server('0.0.0.0', port, application)
    httpd.serve_forever()


def request_by_socket(url):
    """
    socket构造的HTTP 协议的GET请求，可在某些特殊场景下使用
    :param url: 需请求的URL
    :return: 响应头, 响应体
    """
    url = parse.urlparse(url)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 80 if url.port is None else url.port
    send_content = "GET " + url.path + "HTTP/1.1\r\nConnection: close\r\n\r\n"
    send_content = send_content.encode()
    client.connect((url.hostname, port))
    client.send(send_content)
    recv_data = b""
    while True:
        content = client.recv(1024)
        if not content:
            break
        recv_data += content
    response_header, response_body = recv_data.split(b"\r\n\r\n", 1)
    return response_header, response_body


def export_mongodb_data_to_json_file(host, port, database_name, collection_name,
                                     filter_condition=None, save_mode="all", save_dir="./"):
    """
    导出mongodb的数据到json文件中
    :param host: 网络地址
    :param port: 端口
    :param database_name: 数据库名
    :param collection_name: 集合名
    :param filter_condition: 数据过滤条件
    :param save_mode: 数据保存方式，all/one，all将所有数据保存至一个json文件，one将每一份数据单独保存至一个json文件
    :param save_dir: json文件保存的路径，文件名函数自生成
    :return:
    """
    client = pymongo.MongoClient(host, port)
    collection = client[database_name][collection_name].with_options(
        codec_options=bson.CodecOptions(unicode_decode_error_handler="ignore"))
    if not filter_condition:
        filter_condition = {}
    documents = collection.find(filter_condition)
    if save_mode == "all":
        data = [document for document in documents]
        save_path = os.path.join(save_dir, collection_name + ".json")
        open(save_path, "w", encoding="utf-8").write(bson.json_util.dumps(data, indent=4, ensure_ascii=False))
    elif save_mode == "one":
        for document in documents:
            save_path = os.path.join(save_dir, str(document["_id"]) + ".json")
            try:
                open(save_path, "w", encoding="utf-8").write(
                    bson.json_util.dumps(document, indent=4, ensure_ascii=False))
            except Exception as e:
                print(document["_id"])


def multiple_decompress(path):
    """
    对文件夹（含子文件夹）下的所有压缩文件或某个单独的压缩文件进行递归形式的解压缩，实现对多重压缩包的解压
    :param path: 文件夹或文件路径
    :return:
    """
    if os.path.isdir(path):
        compressed_files = get_paths(path, recursive=True)
    else:
        compressed_files = [path]
    for compressed_file in compressed_files:
        target_dir = os.path.splitext(compressed_file)[0]
        command = "7z x -r -aos {} -o{}".format(compressed_file, target_dir)
        pi = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        for i in iter(pi.stdout.readline, b""):
            print(i.decode("GBK"), end="")
        if os.path.exists(target_dir) and os.path.isdir(target_dir):
            multiple_decompress(target_dir)


def get_proxies_by_data5u(order, random=1):
    """
    通过无忧代理（http://www.data5u.com/）API接口获取代理
    :param order: IP提取码
    :param random: 结果定制，默认优先返回速度快的IP
    :return:
    """
    url = "http://api.ip.data5u.com/dynamic/get.html?order={}&ttl=1&json=1&random={}&sep=3".format(order, random)
    proxies = dict()
    for i in range(3):
        try:
            response = requests.get(url, timeout=(10, 10))
            response = json.loads(response.text)
            if response["success"]:
                proxy = "http://{}:{}".format(response["data"][0]["ip"], response["data"][0]["port"])
                proxies["http"] = proxy
                proxies["https"] = proxy
                return proxies
            else:
                print(response["msg"])
        except Exception as e:
            print(repr(e))


def get_proxies():
    url = "http://api.ip.data5u.com/dynamic/get.html?order=53e108334f5e999dad0e9cc62c57beaa&ttl=1&json=1&random=true"
    proxies = dict()
    while True:
        try:
            response = requests.get(url, timeout=(10, 10))
            response_result = json.loads(response.text)
            if response_result["success"]:
                proxy = "http://{}:{}".format(response_result["data"][0]["ip"], str(response_result["data"][0]["port"]))
                proxies["http"] = proxy
                proxies["https"] = proxy
                return proxies
            else:
                print("获取代理失败：{}".format(response_result))
        except Exception as e:
            print("[*]获取代理失败：" + repr(e))


def start_web_server(protocol="http", host="0.0.0.0", port=None, cert="./resource/cert.crt",
                     private_key="./resource/private.key"):
    """
    启动一个web服务器
    :param protocol: 服务器的协议类型，默认为http
    :param host: 监听地址
    :param port: 监听端口，http默认80端口，https默认443端口
    :param cert: SSL证书文件路径，如果类型类型为https，此项有效，已内置默认证书
    :param private_key: 证书的私钥文件路径，如果类型类型为https，此项有效，已内置默认私钥
    :return:
    """
    from flask import Flask
    app = Flask(__name__)

    @app.errorhandler(404)
    def page_not_found(e):
        return "Hello World"

    if not port:
        port = 443 if protocol == "https" else 80

    if protocol == "http":
        app.run(host=host, port=port, threaded=True)
    elif protocol == "https":
        os.chdir(os.path.dirname(__file__))
        app.run(host=host, port=port, ssl_context=(cert, private_key), processes=True)
    else:
        raise Exception("{}: 本函数不支持该协议".format(protocol))


def start_https_server(host="0.0.0.0", port=443, cert="./resource/cert.crt", private_key="./resource/private.key",
                       handler="SimpleHTTPRequestHandler"):
    """
    启动一个https服务器
    PS：在shell中运行该函数，按下两次 Ctrl+C 才能结束，IDLE 中需 restart shell
    :param host: 监听地址
    :param port: 监听端口
    :param cert: SSL证书文件路径
    :param private_key: 私钥文件路径
    :param handler: 如何响应，默认使用SimpleHTTPRequestHandler进行响应，如果不是，则对任意路径都响应"hello, world"
    :return:
    """
    import ssl
    from http import server

    if handler == "SimpleHTTPRequestHandler":
        https_server = server.HTTPServer((host, port), server.SimpleHTTPRequestHandler)
    else:
        """
        响应任意路径
        """
        class ResponseAnyPathHttpServer(server.BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200, message='OK')
                self.end_headers()
                self.wfile.write("hello, world".encode())
        https_server = server.HTTPServer((host, port), ResponseAnyPathHttpServer)
    os.chdir(os.path.dirname(__file__))
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(cert, private_key)
    https_server.socket = context.wrap_socket(https_server.socket, server_side=True)
    https_server.serve_forever()


def get_subs(src, limit_deep=None, current_deep=1):
    """
    递归获取所有子项
    :param src:
    :param limit_deep: 最大递归深度
    :param current_deep: 当前递归深度
    :return:
    """
    results = []
    if type(src) in [list, set, dict] and (not limit_deep or (limit_deep and current_deep <= limit_deep)):
        if type(src) == dict:
            src = list(src.values())
        for sub in src:
            results.extend(get_subs(sub, limit_deep=limit_deep, current_deep=current_deep+1))
    else:
        results.append(src)
    return results


def normalize(path, format="json"):
    """
    将文件中的内容的格式进行标准化
    :param filepath: 文件路径
    :param format: 文件格式，如json、javascript等
    :return:
    """
    if format == "json":
        content = open(path, "r", encoding="utf-8")
        content = json.load(content)
        content = json.dumps(content, indent=4, ensure_ascii=False)
        open(path, "w", encoding="utf-8").write(content)
    elif format == "javascript":
        pass
    else:
        raise Exception("{} format error".format(path))


def base64urlencode(plaintext):
    if type(plaintext) is not bytes:
        plaintext = plaintext.encode("utf-8")
    return base64.b64encode(plaintext).strip(b"=").replace(b'+', b'-').replace(b'/', b'_')


def base64urldecode(ciphertext):
    if type(ciphertext) is not bytes:
        ciphertext = ciphertext.encode("utf-8")
    plaintext = ciphertext.replace(b'-', b'+').replace(b'_', b'/')
    plaintext = plaintext + b'=' * ((4 - (len(plaintext) % 4)) % 4)
    return base64.b64decode(plaintext)


class JWT:
    def __init__(self):
        self.typ = "JWT"
        self.alg = "HS256"

    def decode(self, message):
        message = message.split(".")
        header, payload, signature = message[0], message[1], message[2]
        header = base64urldecode(header)
        payload = base64urldecode(payload)
        return header, payload

    def encode(self, header, payload, key=None):
        data = base64urlencode("{}.{}".format(header, payload))
        if header["alg"].lower() == "none":
            return data
        elif header["alg"] == "HS256":
            return hmac.new(key, data, digestmod="sha256")
        else:
            raise Exception("暂不支持该种加密方式")

    def crack(self, message, dictionary=None, reg="[0-9]{1,6}"):
        message = message.split(".")
        header, payload, signature = message[0], message[1], message[2]
        return Cracker().run(alg=json.loads(base64urldecode(header))["alg"],
                             dictionary=dictionary, reg=reg, args=(header+"."+payload, signature, ))


class Cracker:
    def __init__(self, process_number=1):
        self.passwords_queue = multiprocessing.Manager().Queue(1000000)
        self.process_number = process_number

    def run(self, alg=None, dictionary=None, reg="[0-9]{1,6}", args=None):
        p = multiprocessing.Process(target=self.put_passwords, args=(dictionary, reg,))
        p.start()

        pool = multiprocessing.Pool(self.process_number)
        results = []
        for i in range(self.process_number):
            if alg.lower() == "hs256":
                result = pool.apply_async(func=self.hs256, args=args)
                results.append(result)
            else:
                raise Exception("暂不支持该种加密方式")
        while True:
            for result in results:
                if result.ready():
                    p.terminate()
                    return result.get()

    def put_passwords(self, dictionary, reg):
        """
        生成密码并放入队列
        :param dictionary: 字典文件路径
        :param reg: 如果没有字典文件，则根据正则表达式生成符合条件的字典
        :return:
        """
        if dictionary:
            passwords = [line.strip() for line in open(dictionary, "rb").readlines()]
        else:
            passwords = exrex.generate(reg)
        for password in passwords:
            self.passwords_queue.put(password)
        self.passwords_queue.put(None)

    def md5(self):
        pass

    def hs256(self, plaintext, ciphertext):
        while True:
            password = self.passwords_queue.get()
            if not password:
                self.passwords_queue.put(None)
                break
            if base64urlencode(hmac.new(password.encode(), plaintext.encode(), digestmod="sha256").digest()) == ciphertext.encode():
                print("[-] password: {}".format(password))
                self.passwords_queue.put(None)
                return password
            else:
                print("[-] error: {}".format(password))


class AESCipher:
    def __init__(self, key):
        self.key = self.handle_key(key)
        self.mode = AES.MODE_ECB

    @staticmethod
    def handle_key(key):
        """
        对密钥进行处理
        :param key: 密钥
        :return:
        """
        if type(key) != bytes:
            key = key.encode("utf-8")
        if len(key) < 16:
            key += (16 - len(key)) * b"\x00"
        return key[:16]

    @staticmethod
    def handle_plaintext(plaintext):
        """
        对明文进行处理
        :param plaintext: 明文
        :return:
        """
        if type(plaintext) != bytes:
            plaintext = plaintext.encode("utf-8")
        if len(plaintext) % 16 != 0:
            plaintext += (16 - len(plaintext) % 16) * b"\x00"
        return plaintext

    @staticmethod
    def handle_ciphertext(ciphertext):
        """
        对密文进行处理
        :param ciphertext: 密文
        :return:
        """
        if type(ciphertext) != bytes:
            ciphertext = ciphertext.encode("utf-8")
        ciphertext = base64.b64decode(ciphertext)
        return ciphertext

    def encode(self, plaintext):
        """
        AES加密
        :param plaintext: 明文
        :param key: 密钥
        :return:
        """
        plaintext = self.handle_plaintext(plaintext)
        ciphertext = AES.new(self.key, self.mode).encrypt(plaintext)
        ciphertext = base64.b64encode(ciphertext)
        return ciphertext

    def decode(self, ciphertext):
        """
        AES解密
        :param ciphertext: 密文
        :param key: 密钥
        :return:
        """
        ciphertext = self.handle_ciphertext(ciphertext)
        plaintext = AES.new(self.key, self.mode).decrypt(ciphertext)
        return plaintext

    def encode_by_opensslway(self):
        pass

    def decode_by_opensslway(self):
        pass


class CaptchaCracker:
    def __init__(self):
        pass

    def slide(self):
        pass

    def tup(self):
        pass

    def huidu(self):
        pass

    def jiangzao(self):
        pass


class Gestest:
    def __init__(self, browser):
        self.browser = browser

    def start(self, by="class name", value="geetest_btn"):
        self.browser.find_element(by, value).click()

    def fullpage(self, by="class name", value="geetest_btn"):
        """
        智能组合
        :return:
        """
        self.start(by, value)
        time.sleep(1)
        if "验证成功" in self.browser.find_element(by, value).text:
            return
        elif "请完成验证" in self.browser.find_element(by, value).text:
            self.slide()

    def slide(self):
        """
        滑动验证
        :return:
        """
        distance = self.get_distance()
        tracks = self.generate_tracks(distance)
        self.move(tracks)

    def get_distance(self):
        """
        比对背景图与全图，获取验证码缺口距离
        :return:
        """
        bg = self.get_image("geetest_canvas_bg")
        fullpg = self.get_image("geetest_canvas_fullbg")
        diff = ImageChops.difference(bg, fullpg).convert("L")
        diff.save(r"C:\Users\LQH\Desktop\fullpage.png")
        for x in range(diff.width):
            difference = 0
            for y in range(diff.height):
                difference += diff.getpixel((x, y))
            if difference > 2000:
                print("distance: ", x)
                return x

    def get_image(self, classname):
        """
        获取页面图片的Image对象
        :param classname:
        :return:
        """
        image = self.browser.execute_script(
            "return document.getElementsByClassName('{}')[0].toDataURL('image/png');".format(classname))
        image = base64.b64decode(image.replace("data:image/png;base64,", ""))
        image = io.BytesIO(image)
        image = Image.open(image)
        return image

    def generate_tracks(self, distance):
        """
        轨迹
        :return:
        """
        distance += 20
        v = 0
        t = 0.2
        forward_tracks = []
        current = 0
        mid = distance * 3 / 5  # 减速阀值
        while current < distance:
            if current < mid:
                a = 2  # 加速度为+2
            else:
                a = -3  # 加速度-3
            s = v * t + 0.5 * a * (t ** 2)
            v = v + a * t
            current += s
            forward_tracks.append(round(s))
        back_tracks = [-3, -3, -2, -2, -2, -2, -2, -1, -1, -1]
        forward_tracks.extend(back_tracks)
        print("forward_tracks: ", forward_tracks)
        return forward_tracks

    def move(self, tracks):
        """
        移动
        :return:
        """
        slider = self.browser.find_element("class name", "geetest_slider_button")
        action = webdriver.ActionChains(self.browser)
        webdriver.ActionChains(self.browser).click_and_hold(slider).perform()
        for x in tracks:
            action.move_by_offset(x, 0)
        action.release().perform()

    def client(self):
        """
        点选验证
        :return:
        """


def binary_search(arr, judge_function, mode="three"):
    """
    二分查找法
    :param arr:
    :param func: < 为 -1, = 为 0, > 为 1,
    :return:
    """
    left = 0
    right = len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        judge_result = judge_function(arr[mid])
        if mode == "three":
            if judge_result  == -1:
                left = mid -1
            elif judge_result == 1:
                right = mid + 1
            elif judge_result == 0:
                return mid
            else:
                raise Exception("判断函数编写错误，请检查所有输入都有对应且正确的输出")
        elif mode == "two":
            if judge_result == -1:
                left = mid
            elif judge_result == 1:
                right = mid
            else:
                raise Exception("判断函数编写错误，请检查所有输入都有对应且正确的输出")
            if right - left == 1:
                return left

        print(left, right)


def shell():
    """
    :return:
    """
    pass


def dns_shell():
    """
    dns隧道
    :return:
    """
    pass


def get_ioc_type(ioc):
    """
    判定ioc的类型
    :param ioc:
    :return:
    """
    if is_ip(ioc):
        return "ip"
    if is_url(ioc):
        return "url"
    if is_domain(ioc):
        return "domain"
    return "unknown"


def is_domain(string):
    """
    判断字符串是否符合域名格式
    :param string:
    :return:
    """
    domain = re.compile(r"^[0-9a-zA-Z]+[0-9a-zA-Z\.-]*\.[a-zA-Z]{2,12}$")
    return True if re.match(domain, string) else False


def is_url(string):
    """
    判断字符串是否符合url格式
    :param string:
    :return:
    """
    url = re.compile(r"^(http|https):\/\/[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&\/\/=]*)$")
    return True if re.match(url, string) else False


def is_ip(string):
    """
    判断字符串是否符合ip格式
    :param string:
    :return:
    """
    ip = re.compile(r"^(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}$")
    return True if re.match(ip, string) else False


def multiprocess(traget, args, number=10):
    """
    创建多进程任务
    :param traget:
    :param queue: multiprocessing.Queue 对象
    :param number:
    :return:
    """
    pool = multiprocessing.Pool(number)
    for i in range(number):
        pool.apply_async(traget, args)
    pool.close()
    pool.join()


def get_second_level_domain(domain):
    """
    获取域名的二级域名
    :param domain:
    :return:
    """
    domain = domain.split(".")
    second_level_domain = domain[-2] + "." + domain[-1]
    return second_level_domain


def get_alexa_rank(domain):
    """
    获取网站在alexa的排名
    :param domain: 域名，或者是域名组成的列表
    :return: dict, 返回alexa排名，如果未查询到，则返回-1
    """
    file = os.path.join(os.path.dirname(__file__), r"./resource/top-1m.csv")
    # 当不存在alexa的排名记录文件或者文件的下载日期超过了一周时，重新获取排名记录文件
    if not os.path.exists(file) or time.time() - os.path.getctime(file) > 60*60*24*7:
        api = "http://s3.amazonaws.com/alexa-static/top-1m.csv.zip"
        alexa = requests.get(api).content
        alexa = zipfile.ZipFile(io.BytesIO(alexa))
        alexa = alexa.read(alexa.namelist()[0])
        open(file, "wb").write(alexa)
    # 将排名记录文件读取并解析
    lines = open(file).readlines()
    rank = {}
    for line in lines:
        i, j = line.strip().split(",")
        rank[j] = int(i)
    # 域名格式处理
    domains = []
    if type(domain) == list:
        domains.extend(domain)
    else:
        domains.append(domain)
    # 根据二级域名获取alexa排名
    results = dict()
    for domain in domains:
        second_level_domain = get_second_level_domain(domain)
        if second_level_domain in rank:
            results[domain] = rank[second_level_domain]
        else:
            results[domain] = -1
    return results


def port_reuse():
    """ 端口复用 """
    socket = ""


if __name__ == '__main__':
    pass
