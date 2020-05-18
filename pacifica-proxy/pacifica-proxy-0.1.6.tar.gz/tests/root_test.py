#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test the main method."""
from json import loads
from cherrypy.test import helper
from pacifica.proxy.rest import Root
from .common_test import CommonCPSetup


class TestRootObject(helper.CPWebCase, CommonCPSetup):
    """Test the uploader policy service."""

    PORT = 8180
    HOST = '127.0.0.1'
    headers = [('Content-Type', 'application/json')]

    def test_root(self):
        """Test the root object."""
        root = Root()
        self.assertFalse(root is None)

    def test_status_url(self):
        """Test the status url on root."""
        self.getPage('/')
        self.assertStatus('200 OK')
        data = loads(self.body)
        self.assertTrue('message' in data, 'Body of status has message key')
        self.assertEqual(data['message'], 'Pacifica Proxy Up and Running', 'content of message is specific')
