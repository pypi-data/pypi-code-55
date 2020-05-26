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

from wpx.setwp import SetWallpaperOptions
import logging
import os
import subprocess
import shlex

logger = logging.getLogger(__name__)


def set_wallpaper(options: SetWallpaperOptions):
  logger.info('Setting the Wallpaper on OSX is only partially supported. Most likely this will '
              'only have updated your current desktop(s) but not other workspaces. Please check '
              'out https://git.niklasrosenstein.com/NiklasRosenstein/wpx/wiki/Automatic-Wallpaper-updates-on-OSX '
              'for troubleshooting.')

  if options.desktop:
    # 1) Use osascript to update all wallpapers.
    command = 'tell application "System Events" to set picture of every desktop to "{}"'\
              .format(os.path.abspath(options.path))
    subprocess.check_call(['osascript', '-e', command])

    # 2) Update the default background image.
    payload = '{default = {ImageFilePath="%s"; };}' % (os.path.abspath(options.path),)
    subprocess.check_call(['defaults', 'write', 'com.apple.desktop', 'Background', payload])
    subprocess.check_call(['killall', 'Dock'])
