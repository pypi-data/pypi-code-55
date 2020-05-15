# This file is part of Marcel.
# 
# Marcel is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or at your
# option) any later version.
# 
# Marcel is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Marcel.  If not, see <https://www.gnu.org/licenses/>.

import marcel.core


SUMMARY = '''
The input stream is output in reverse order.
'''


DETAILS = None


def reverse():
    return Reverse()


class ReverseArgParser(marcel.core.ArgParser):

    def __init__(self, env):
        super().__init__('reverse', env, None, SUMMARY, DETAILS)


class Reverse(marcel.core.Op):

    def __init__(self):
        super().__init__()
        self.contents = []

    # BaseOp
    
    def setup_1(self):
        pass
    
    def receive(self, x):
        self.contents.append(x)
    
    def receive_complete(self):
        self.contents.reverse()
        for x in self.contents:
            self.send(x)
        self.send_complete()
