#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#################################################################################
#                                                                               #
#   OpenPost - Opens a POST request from the command line in a browser window   #
#   Copyright (C) 2020 Bob Swift                                                #
#                                                                               #
#   Permission is hereby granted, free of charge, to any person obtaining a     #
#   copy of this software and associated documentation files (the "Software"),  #
#   to deal in the Software without restriction, including without limitation   #
#   the rights to use, copy, modify, merge, publish, distribute, sublicense,    #
#   and/or sell copies of the Software, and to permit persons to whom the       #
#   Software is furnished to do so, subject to the following conditions:        #
#                                                                               #
#   The above copyright notice and this permission notice shall be included     #
#   in all copies or substantial portions of the Software.                      #
#                                                                               #
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS     #
#   OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF                  #
#   MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.      #
#   IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY        #
#   CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,        #
#   TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE           #
#   SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.                      #
#                                                                               #
#################################################################################

# pylint: disable=R0902, R0913

"""Creates an html POST request file and allows opening in a browser window."""




import os
# import html
# import re
import time
import webbrowser

__version__ = "0.3"


class OpenPost():
    """Creates an html POST request file and allows opening in a browser window."""

    HTML_TEMPLATE = """\
<!DOCTYPE html>
<html>
  <head>
  <title>OpenPost Redirector</title>
{0}
  </head>
  <body onLoad="javascript: document.getElementById('postform').submit();">
    <form method="post" name="postform" id="postform" action="{1}">
{2}
    </form>
{3}
  </body>
</html>
"""

    def __init__(self, url=None, file_name=None, keep_file=False, time_to_live=5, form_data=None, headers=None, body=None, new_tab=True):
        """Creates an html POST request file and allows opening in a browser window.

        Keyword Arguments:
            url {str} -- The url for the action in the POST (default: None)
            file_name {str} -- Path and name of the output html file (default: 'OpenPost.html')
            keep_file {bool} -- Keep the output html file after opening in browser (default: False)
            time_to_live {float} -- Number of seconds to delay before removing the output html file (0-60) (default: 5)
            form_data {dict} -- The key:value data to include in the POST request (default: {})
            headers {str|list} -- Lines to include in the <head> section of the html file (default: None)
            body {str} -- Additional lines to include in the <body> section of the html file (default: None)
            new_tab {bool} -- Open the html file in a new browser tab (default: True)
        """
        self.form_data = self._validate_data(form_data)
        self.url = url
        self.keep_file = keep_file
        self.file_name = self._make_filename(file_name)
        self.time_to_live = time_to_live
        self.headers = headers
        self.body = body
        self.new_tab = new_tab
        self.written = False    # Depricated as of v0.3

    @staticmethod
    def version():
        """Returns the version number of the module.

        Returns:
            {str} -- The version number
        """
        return __version__

    @staticmethod
    def _validate_ttl(ttl):
        """Validates the time-to-live value for the output html file after sending the POST request.

        Arguments:
            ttl {float} -- Number of seconds to delay before removing the output html file

        Raises:
            ValueError: Time to live out of range (0-60)

        Returns:
            {float} -- Valid time-to-live value
        """
        temp = float(ttl)
        if 0 <= temp <= 60:
            return temp
        raise ValueError('Time to live out of range (0-60)')

    @staticmethod
    def _validate_data(form_data):
        """Validate the data to be used in the form

        Arguments:
            form_data {dict} -- Dictionary of key:value data to include in the POST request

        Raises:
            ValueError: Form_data not a dictionary

        Returns:
            {dict} -- The key:value data to include in the POST request
        """
        if not form_data:
            return {}
        if isinstance(form_data, dict):
            return form_data
        raise ValueError('Form_data not a dictionary')

    @staticmethod
    def _validate_url(url):
        """Very basic validation of the submitted url.

        Arguments:
            url {str} -- URL to validate

        Raises:
            ValueError: Invalid url.

        Returns:
            {str} -- Validated url
        """
        if url and isinstance(url, str):
            temp = url.strip()
            # r'^(ftp|https?)://[^\s"]+$'
            if temp and ' ' not in temp:
                return temp
        raise ValueError('Invalid url.')

    @staticmethod
    def _make_string(text):
        if text:
            if isinstance(text, list):
                return ('\n'.join(text)).strip()
            return text.strip()
        return ''

    @staticmethod
    def _make_filename(name):
        """Validate the output file name for the POST html file.

        Arguments:
            name {str} -- Path and file name

        Returns:
            {str} -- Validated file path and name
        """
        if name:
            temp = name.strip()
            if temp:
                if not temp.endswith('.html'):
                    temp += '.html'
                return temp
        return 'OpenPost.html'

    def clear_data(self):
        """Clears the data used for the POST request form.
        """
        self.form_data = {}

    def add_key(self, key, value):
        """Add or update a data key used for the POST request form.

        Arguments:
            key {str} -- Key used in the form
            value {str} -- Value for the specified key
        """
        self.form_data[key] = str(value)

    def delete_key(self, key):
        """Remove a data key used for the POST request form.

        Arguments:
            key {str} -- Key to be removed from the form
        """
        self.form_data.pop(key, None)

    def make_html(self):
        """Make the content of the output html file.

        Returns:
            {str} -- The content of the html file, or '' if an error
        """
        url = self._validate_url(self.url)
        headers = self._make_string(self.headers)
        body = self._make_string(self.body)
        data = self._validate_data(self.form_data)
        if not data:
            return ''
        form_content = ''
        for key in data.keys():
            form_content += "<textarea name='{0}' id='{0}' form='postform' style='display: none;'>{1}</textarea>\n".format(key, str(data[key]).strip())
        return self.HTML_TEMPLATE.format(headers, url, form_content, body)

    def write_html(self):
        """Prepare and write the output html file.

        Returns:
            {bool} -- True if the file was successfully written, otherwise false
        """
        filename = self._make_filename(self.file_name)
        html = self.make_html()
        if not html:
            return False
        with open(filename, 'w', encoding='utf-8') as output_file:
            output_file.write(html)
        return True

    def send_post(self):
        """Open the output POST html file in the default web browser, automatically writing the
        output html file if it has not already been written.  Automatically removes the output
        file after the specified time delay unless the keep_file flag has been set.

        Returns:
            {bool} -- True if the file was successfully opened, otherwise false
        """
        filename = self._make_filename(self.file_name)
        if not self.write_html():
            return False
        if self.new_tab:
            webbrowser.open_new_tab(filename)
        else:
            webbrowser.open(filename)

        #   Remove temporary HTML file
        if not self.keep_file:
            time.sleep(self.time_to_live)
            if os.path.exists(filename):
                os.remove(filename)

        return True
