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

import readline

import marcel.core


SUMMARY = '''
Generate a stream containing the history of commands executed.
'''


DETAILS = '''
The history command itself will not show up in the command history.
'''


def history():
    return History()


class HistoryArgParser(marcel.core.ArgParser):

    def __init__(self, env):
        super().__init__('history', env, None, SUMMARY, DETAILS)


class History(marcel.core.Op):

    def __init__(self):
        super().__init__()

    def __repr__(self):
        return 'history()'

    # BaseOp

    def setup_1(self):
        pass

    def receive(self, _):
        # Remove the run command from history
        readline.remove_history_item(readline.get_current_history_length() - 1)
        history = self.env().reader.history()
        for i in range(len(history)):
            self.send((i, history[i]))

    # Op

    def must_be_first_in_pipeline(self):
        return True

    def run_in_main_process(self):
        return True
