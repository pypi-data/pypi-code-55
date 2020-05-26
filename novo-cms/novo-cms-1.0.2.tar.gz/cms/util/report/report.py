#!/usr/bin/env python
# -*- encoding: utf8 -*-
"""
    WebReport Export
"""
import os
import re
import sys
import json
import textwrap

import requests

from cms.util import get_logger, User


reload(sys)
sys.setdefaultencoding('utf-8')


BASE_URL = 'http://fr.novogene.com:8080/WebReport/ReportServer'

__author__ = 'suqingdong'
__author_email__ = 'suqingdong@novogene.com'


class WebReport(object):

    def __init__(self, username, password, logger=None):
        self.username = username
        self.password = password
        self.base_url = BASE_URL

        self.logger = logger or get_logger()

        self.session = requests.session()

    def login(self):

        url = self.base_url + '?op=fs_load&cmd=login'

        payload = {
            'fr_username': self.username,
            'fr_password': self.password,
            'fr_remember': 'true',
        }
        resp = self.session.post(url, data=payload).json()

        if resp.get('fail'):
            self.logger.error('[{errorCode}] {errorMsg}'.format(**resp))
            return False

        self.logger.info('Login Successfully!')
        return True

    def get_sessionid(self, payload):
        resp = self.session.get(self.base_url, params=payload)
        sessionid = re.findall(r'sessionID=(\d+)', resp.text)[0]
        return sessionid

    def list_transactiontype(self):
        """
        获取业务线编码，eg. 疾病研究部 1911
        """
        payload = {'reportlet': 'CRM/kf/F009.cpt'}
        sessionid = self.get_sessionid(payload)
        self.logger.info('SessionID: {}'.format(sessionid))

        payload = {
            'op': 'widget',
            'widgetname': 'transactiontype',
            'sessionID': sessionid
        }
        resp = self.session.post(self.base_url, params=payload).json()
        print('#业务线序号\t业务线名称')
        for each in resp:
            print('{value}\t{text}'.format(**each))

    def get_report(self, transactiontype):
        payload = {
            'reportlet': '/CRM/kf/y102.cpt',
            'transactiontype': transactiontype,
            # 'year': '2020',
            # 'month': '5',
        }
        sessionid = self.get_sessionid(payload)
        self.logger.info('SessionID: {}'.format(sessionid))

        # get dialog
        payload = {
            'op': 'fr_dialog',
            'cmd': 'parameters_d',
            'sessionID': sessionid
        }
        formdata = {
            '__parameters__': {
                "LABELPROJECTNUM": "[9879][76ee][7f16][53f7]:",
                "PROJECTNUM": "",
                "LABELCONTRACTNO": "[5408][540c][53f7]:",
                "CONTRACTNO": "",
                "LABELCONFIRMSTATUS": "[786e][8ba4][7c7b][578b]:",
                "CONFIRMTYPE": "",
                "CONFIRMTYPE_TEMP": ""
            }
        }

        # 查询信息存储在cookies中
        resp1 = self.session.post(self.base_url, params=payload, data=formdata)

        # # Table List
        # payload = {
        #     'op': 'page_content',
        #     'sessionID': sessionid,
        #     'pn': '1',
        # }
        # resp2 = self.session.get(self.base_url, params=payload, cookies=resp1.cookies)

        # Excel Export
        payload = {
            'op': 'export',
            'sessionID': sessionid,
            'format': 'excel',
            'extype': 'simple'
        }
        resp2 = self.session.get(self.base_url, params=payload, cookies=resp1.cookies, stream=True)
        return resp2


def main(**args):

    username = args['username']
    password = args['password']
    transactiontype = args['transactiontype']

    logger = get_logger('Report', verbose=args['verbose'])

    user = User(**args)
    username, password = user.get_user_pass()
    wr = WebReport(username, password, logger=logger)
    if wr.login():
        user.save(username, password)
    else:
        exit(1)

    if transactiontype == 'list':
        wr.list_transactiontype()
        exit()

    resp = wr.get_report(transactiontype)
    with open(args['output'], 'wb') as out:
        for chunk in resp.iter_content(chunk_size=1024):
            out.write(chunk)

    logger.info('\033[33msave file: {output}\033[0m'.format(**args))


def parser_add_report(parser):

    parser.description = __doc__

    parser.epilog = textwrap.dedent('''
        examples:
            %(prog)s -tid 1911 -o report.1911.xlsx  # 指定业务线编码
            %(prog)s -tid list                      # 查看所有业务线编码列表
    ''')

    parser.add_argument('-tid', '--transactiontype',
                        help='the number of your transactiontype, use "list" to list all transactiontypes [%(default)s]',
                        default='1911')

    parser.add_argument('-o', '--output',
                        help='the output filename [%(default)s]',
                        default='report.xlsx')

    parser.set_defaults(func=main)
