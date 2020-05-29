import os
import requests

from ybc_config import config
from ybc_exception import InternalError

_COURSE_API_PREFIX = config["course-api-prefix"]
# 每个 HTTP 请求最多的请求次数
_MAX_RETRY_TIMES = 3


def _read_env(key):
    return os.environ[key] if key in os.environ else ''


def _build_headers():
    persistent = _read_env('REFRESH_TOKEN')
    headers = {
        'Cookie': 'persistent=' + persistent,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    return headers


def _to_json(response):
    """
    从 HTTP 请求的响应中获取数据并解析成 JSON 格式
    异步方法: JS requests 库中基于 fetch api, 其 Response.json() 方法返回 Promise

    :param response:
    :return:
    """
    return response.json()


def get(url_rel_path, params=None):
    """
    带失败重试的 HTTP GET 方法

    :param url_rel_path: url 相对路径, 例如 animal-sound
    :param params: 请求参数
    :return: 请求返回的数据, JSON 对象
    """
    url = '{}/{}'.format(_COURSE_API_PREFIX, url_rel_path)
    headers = _build_headers()
    for i in range(_MAX_RETRY_TIMES):
        # TODO: 增加 headers, 注入 cookie 等
        response = requests.get(
            url=url,
            params=params if params else {},
            headers=headers
        )
        # TODO: 根据 status code 决定是否进行重试, 比如 4XX 不应该重试, 5XX 应该重试
        if response.ok:
            return _to_json(response)

    raise InternalError('调用 get 接口失败: url={}, params={}'.format(url, params), __name__)


def post(url_rel_path, data, params=None):
    """
    带失败重试的 HTTP POST 方法

    :param url_rel_path: url 相对路径, 例如 animal-sound
    :param data: 请求的 Body
    :param params: 请求参数
    :return: 请求返回的数据, JSON 对象
    """
    url = '{}/{}'.format(_COURSE_API_PREFIX, url_rel_path)
    headers = _build_headers()
    for i in range(_MAX_RETRY_TIMES):
        response = requests.post(
            url=url,
            json=data,
            params=params if params else {},
            headers=headers,
        )

        if response.ok:
            return _to_json(response)

    raise InternalError('调用 post 接口失败: url={}, data={}, params={}'.format(url, data, params),
                        __name__)
