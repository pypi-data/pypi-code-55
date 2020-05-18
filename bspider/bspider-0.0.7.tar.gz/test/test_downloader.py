import asyncio
import time

import aiohttp
import requests
from aiohttp import ClientResponse

from bspider.http import Request, Response

proxy = '27.152.204.239:22148'

def get_proxy():
    url = 'http://proxy.baishanglin.top/proxy/'
    proxy = requests.get(url).json()['data']
    print(proxy)
    proxy['proxy'] = 'https://{proxy}'.format(**proxy)
    return proxy

class Test(object):

    async def __assemble_response(self, response: ClientResponse, request: Request) -> Response:
        # 这里只处理 str 类型的数据
        text = await response.text(errors='ignore')
        return Response(
            url=str(response.url),
            status=response.status,
            headers=dict(response.headers),
            request=request,
            cookies={i.key: i.value for i in response.cookies.values()},
            text=text
        )

    async def do(self, req: Request) -> Response:
        """
        执行下载操作
        url': '', # 请求的url 必须
        method': '', # 请求的方法 GET, POST, PUT ,PATCH, OPTIONS, HEAD, DELETE
        request_body': {}, # POST 请求的消息体 字典结构
        cookies': {}, # 请求时携带的cookie 字典结构
        meta': {}, # 请求时携带的上下文信息，通常与本次请求无关
        proxy': str
        allow_redirect': bool, # 下载是否需要重定向
        timeout: int /s
        task_info': {
            name': '', # 任务信息
            task_sign': '', # 一个任务中一个链接中每一次请求的唯一标识
        }
        :param param: dict 下载参数
        :return:
        """
        # sc 在每次请求都要关闭，所以使用上下文管理器进行管理
        temp_timeout = aiohttp.ClientTimeout(connect=req.timeout)
        async with aiohttp.ClientSession() as session:
            async with session.request(
                    method=req.method,
                    url=req.url,
                    headers=req.headers,
                    # post 参数，get时为 None
                    data=req.data,
                    cookies=req.cookies,
                    # 是否允许重定向
                    allow_redirects=req.allow_redirect,
                    timeout=temp_timeout,
                    proxy=None if not isinstance(req.proxy, dict) else req.proxy.get('proxy'),
                    # ssl验证
                    ssl=req.verify_ssl,
            ) as resp:
                # 挂起等待下载结果
                return await self.__assemble_response(resp, req)


if __name__ == '__main__':
    bd = Test()

    req = Request(
        url='https://www.baidu.com/',
        method='GET',
        timeout=10,
        proxy= get_proxy()
    )

    loop = asyncio.get_event_loop()
    tasks = [asyncio.ensure_future(bd.do(req))]

    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
