# -*- coding:utf-8 -*-

# 如果只是用来判断是否需要使用代理，则无需随机生成header，使用固定的header即可
HEADER = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0',
    'Accept': 'text/html, application/xhtml+xml, application/xml;q = 0.9, image/webp, image/apng, */*;q = 0.8, application/signed-exchange;v = b3',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Encoding': '*',  # 某些网站，及时可以使用br，也需要设置成*，否则返回乱码
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Connection': 'keep-alive'}