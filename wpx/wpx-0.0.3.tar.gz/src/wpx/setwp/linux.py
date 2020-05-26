# -*- coding: utf8 -*-
# Copyright (c) 2020 Niklas Rosenstein
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

# NOTE: Assumes that the system is running GNOME.

from . import SetWallpaperOptions
from gi.repository import Gio
import os
import logging
import subprocess

SCHEMA = 'org.gnome.desktop.background'
PICTURE_URI = 'picture-uri'


def _ensure_dbus_session_address_var():
  """
  In order to set the wallpaper from a limited set of environment variables, as
  is the case when running wpx from cron, find the DBUS_SESSION_BUS_ADDRESS
  value and set it.

  Thanks to https://askubuntu.com/a/743024 for the solution.
  """

  if not os.getenv('DBUS_SESSION_BUS_ADDRESS'):
    script = (
      'set -e\n'
      'PID=$(pgrep --euid $(id --real --user) gnome-session | head -n1)\n'
      'grep -z DBUS_SESSION_BUS_ADDRESS /proc/$PID/environ|cut -d= -f2-')
    output = subprocess.check_output(['bash', '-c', script]).decode().strip().strip('\x00')
    os.environ['DBUS_SESSION_BUS_ADDRESS'] = output.strip()


def set_wallpaper(options: SetWallpaperOptions):
  _ensure_dbus_session_address_var()
  if options.desktop:
    path = 'file://' + os.path.abspath(options.path)
    settings = Gio.Settings.new(SCHEMA)
    settings.set_string(PICTURE_URI, path)
  if options.login:
    logging.warning('setting the login wallpaper is not supported on linux')
