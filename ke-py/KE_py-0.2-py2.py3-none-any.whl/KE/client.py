# -*- coding: utf-8 -*-
from __future__ import with_statement, print_function, absolute_import
import requests
from KE.v3.client import KE3
from KE.v4.client import KE4


class KE(object):
    def __new__(cls, host='localhost', port=7070, username='ADMIN', password='KYLIN', version=3,
                debug=False, *args, **kwargs):
        if version == 3:
            return KE3(host, port=port, username=username, password=password,
                       debug=debug, *args, **kwargs)
        elif version == 4:
            return KE4(host, port=port, username=username, password=password,
                       debug=debug,  *args, **kwargs)

    def __repr__(self):
        return "<KE Host: {host} Version: {version}>".format(host=self.host, version=self.version)

