# -*- coding: utf-8 -*-
# Authored by: Josh (joshzda@gmail.com)

from __future__ import absolute_import, unicode_literals

import six

from jdu.core.utils import to_binary, to_text


class JDUException(Exception):

    def __init__(self, errcode, errmsg):
        """
        :param errcode: Error code
        :param errmsg: Error message
        """
        self.errcode = errcode
        self.errmsg = errmsg

    def __str__(self):
        _repr = 'Error code: {code}, message: {msg}'.format(
            code=self.errcode,
            msg=self.errmsg
        )

        if six.PY2:
            return to_binary(_repr)
        else:
            return to_text(_repr)

    def __repr__(self):
        _repr = '{klass}({code}, {msg})'.format(
            klass=self.__class__.__name__,
            code=self.errcode,
            msg=self.errmsg
        )
        if six.PY2:
            return to_binary(_repr)
        else:
            return to_text(_repr)


class InvalidSignatureException(JDUException):
    """Invalid signature exception class"""

    def __init__(self, errcode=10001, errmsg='Invalid signature'):
        super(InvalidSignatureException, self).__init__(errcode, errmsg)


class ParamTypeError(JDUException):
    def __init__(self, param_name, param_type):
        errcode = 10002
        errmsg = '%s should be %s' % s(param_name, param_type)
        super(ParamTypeError, self).__init__(errcode, errmsg)


class JDUClientException(JDUException):
    """JD Union API client exception class"""

    def __init__(self, code, message, client=None,
                 request=None, response=None):
        errcode = 20001
        errmsg = '京东联盟错误Code: %s, Message: %s' % (code, message)
        super(JDUClientException, self).__init__(errcode, errmsg)
        self.client = client
        self.request = request
        self.response = response


class JDUClientAccessException(JDUClientException):
    """JD Union 权限错误"""
    pass
