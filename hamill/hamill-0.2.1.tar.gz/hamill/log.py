# -----------------------------------------------------------
# MIT Licence (Expat License Wording)
# -----------------------------------------------------------
# Copyright © 2020, Damien Gouteux
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# For more information about the Hamill lightweight markup language see:
# https://xitog.github.io/dgx/informatique/hamill.html

#-------------------------------------------------------------------------------
# Import
#-------------------------------------------------------------------------------

import sys

#-------------------------------------------------------------------------------
# Logging
#-------------------------------------------------------------------------------

try:
    out = sys.stdout.shell
    IDLE = True
except AttributeError:
    out = sys.stdout
    IDLE = False

def success(*msg, sep=' '):
    msg = sep.join(msg)
    if IDLE:
        out.write('[SUCCESS] ' + msg + '\n', 'STRING')
    else:
        out.write(msg + '\n')

def fail(*msg, sep=' '):
    msg = sep.join(msg)
    if IDLE:
        out.write('[FAIL] ' + msg + '\n', 'COMMENT')
    else:
        out.write(msg + '\n')

def info(*msg, sep=' '):
    msg = sep.join(msg)
    if IDLE:
        out.write('[INFO] ' + msg + '\n', 'DEFINITION')
    else:
        out.write(msg + '\n')

def warn(*msg, sep=' '):
    msg = sep.join(msg)
    if IDLE:
        out.write('[WARN] ' + msg + '\n', 'KEYWORD')
    else:
        out.write(msg + '\n')

def error(*msg, sep=' '):
    msg = sep.join(msg)
    if IDLE:
        out.write('[ERROR] ' + msg + '\n', 'COMMENT')
    else:
        out.write(msg + '\n')
