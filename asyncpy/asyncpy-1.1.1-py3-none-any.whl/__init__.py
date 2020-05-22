# -*- coding: utf-8 -*-

"""Asyncpy
Usage:
  asyncpy genspider <name>
  asyncpy (-h | --help | --version)
  asyncpy lx
Options:
  --version        Show version.
"""


from asyncpy.middleware import Middleware
from asyncpy.request import Request
from asyncpy.response import Response
from asyncpy.spider import Spider
from asyncpy.exceptions import IgnoreThisItem
from pathlib import Path
from docopt import docopt

__all__ = ["Middleware","Request","Response","Spider","IgnoreThisItem"]


VERSION = '1.1.1'

DEFAULT_ENCODING = 'utf-8'
'https://aweme-hl.snssdk.com/aweme/v1/user/follower/list/?user_id=59473716351&sec_user_id=MS4wLjABAAAA3518Z2y29JzKNc5Ts8zO_xKBDwKL_ZZzpBhmxuBt7dE&max_time=1590106628&count=20&offset=0&source_type=1&address_book_access=1&gps_access=1&os_api=23&device_type=MI%205s&device_platform=android&ssmix=a&iid=4230556658973179&manifest_version_code=981&dpi=320&uuid=008796763985702&version_code=981&app_name=aweme&cdid=46423769-97c1-4fae-a612-44f5ccf4b778&version_name=9.8.1&ts=1590110215&openudid=c055533a0591b2dc&device_id=69918538596&resolution=810*1440&os_version=6.0.1&language=zh&device_brand=Xiaomi&app_type=normal&ac=wifi&update_version_code=9802&aid=1128&channel=tengxun_new&_rticket=1590110215836'
'https://aweme-hl.snssdk.com/aweme/v1/user/follower/list/?user_id=59473716351&sec_user_id=MS4wLjABAAAA3518Z2y29JzKNc5Ts8zO_xKBDwKL_ZZzpBhmxuBt7dE&max_time=1590105767&count=20&offset=0&source_type=1&address_book_access=1&gps_access=1&os_api=23&device_type=MI%205s&device_platform=android&ssmix=a&iid=4230556658973179&manifest_version_code=981&dpi=320&uuid=008796763985702&version_code=981&app_name=aweme&cdid=46423769-97c1-4fae-a612-44f5ccf4b778&version_name=9.8.1&ts=1590110235&openudid=c055533a0591b2dc&device_id=69918538596&resolution=810*1440&os_version=6.0.1&language=zh&device_brand=Xiaomi&app_type=normal&ac=wifi&update_version_code=9802&aid=1128&channel=tengxun_new&_rticket=1590110235062'

import os
import shutil
def create_base(name):
    template = 'templates'
    template_path = Path(__file__).parent / template
    project_path = os.path.join(os.getcwd(), name)
    if not os.path.exists(project_path):
        shutil.copytree(template_path, project_path)
        os.rename(project_path,project_path)
        spider_path = os.path.join(project_path, 'spiders/templates.py')
        new_spider_path = os.path.join(project_path, 'spiders/{}.py'.format(name))
        os.rename(spider_path,new_spider_path)
        print(new_spider_path)
        with open(file=new_spider_path,mode='r',encoding='utf-8')as f:
            doc = f.read()
            doc = doc.replace('templates',name).replace('Demo',name.capitalize())
            with open(file=new_spider_path,mode='w',encoding='utf-8')as f1:
                f1.write(doc)
                print("创建成功")
    else:
        print("文件已存在")





def cli():
    """
    Commandline for Asyncpy :d
    """
    argv = docopt(__doc__, version=VERSION)
    if argv.get('genspider'):
        name = argv['<name>']
        create_base(name=name)

    if argv.get('lx'):
        print("For the welfare of the people all over the world is one of my lifelong wishes -- lx")
