import sys
import signal
import logging
from time import sleep
from snowctl.utils import *
from snowctl.config import Config
from snowctl.arguments import arg_parser
from snowctl.logger import logger_options
from snowctl.connect import snowflake_connect


LOG = logging.getLogger(__name__)

BANNER = """\
    --..,_                     _,.--.
       `'.'.                .'`__ o  `;__.
          '.'.            .'.'`  '---'`  `
            '.`'--....--'`.'
              `'--....--'`
"""

def print_usage():
    print('\nsnowctl usage:')
    print('\tuse <database|schema|warehouse> <name>')
    print('\tcopy views - copy view(s) in currect context to other schemas as is')
    print('\tcopy views filter - copy view(s) in currect context to other schemas and choose columns to filter')
    print('\tshow views')
    print('\tsql <query> - execute sql query')
    print('\texit|ctrl+C\n')


class Controller:
    def __init__(self, conn, safe):
        self.conn = conn
        self.cursor = conn.cursor()
        self.safe_mode = safe
        self.run = True
        self.prompt = 'snowctl> '
        self.curr_db = None

    def run_console(self):
        self.listen_signals()
        print_usage()
        try:
            while self.run:
                self.get_prompt()
                print(self.prompt, end='', flush=True)
                user_input = sys.stdin.readline()
                cmd = parser(user_input)
                if cmd is not None:
                    self.operation(cmd)
                else:
                    print('command not found')
        except Exception as e:
            LOG.error(e)
        finally:
            self.exit_console()

    def operation(self, cmd: list):
        try:
            if cmd[0] == 'help':
                print_usage()
            elif cmd[0] == 'copy':
                if len(cmd) == 2:
                    self.copy_views()
                else:
                    self.copy_views(True)
            elif cmd[0] == 'show':
                self.show_views()
            elif cmd[0] == 'use':
                self.use(cmd)
            elif cmd[0] == 'sql':
                self.user_query(cmd)
            elif cmd[0] == 'exit':
                self.exit_console()
        except Exception as e:
            print(f'Error. {e}')

    def use(self, cmd: list):
        self.cursor.execute(f"use {cmd[1]} {cmd[2]}")
        response = self.cursor.fetchone()
        print(response[0])        

    def user_query(self, cmd: list):
        cmd.pop(0)
        query = ' '.join(cmd)
        response = self.execute_query(query)
        for row in response:
            print(row)

    def show_views(self):
        rows = self.execute_query('show views')
        for i, row in enumerate(rows):
            print(f'{i} - {row[1]}')

    def copy_views(self, filter_cols=False):
        from snowctl.copy import Copycat
        cp = Copycat(self.conn, self.safe_mode)
        cp.copy_views(self.curr_db, filter_cols)

    def ask_confirmation(self, query):
        print(f'\n{query}')
        print(f'Confirm? (y/n): ', end='', flush=True)
        user_input = sys.stdin.readline().replace('\n', '').strip()
        if user_input == 'y':
            return True
        else:
            return False

    def execute_query(self, query):
        LOG.debug(f'executing:\n{query}')
        self.cursor.execute(query)
        results = []
        while True:
            row = self.cursor.fetchone()
            if not row:
                break
            results.append(row)
        return results

    def get_prompt(self):
        prompt = ''
        response = self.execute_query('select current_warehouse(), current_database(), current_schema()')
        wh = response[0][0]
        db = response[0][1]
        schema = response[0][2]
        if wh is not None:
            prompt += f'{wh}:'
        if db is not None:
            prompt += f'{db}:'
            self.curr_db = db
        if schema is not None:
            prompt += f'{schema}:'
        if not len(prompt):
            self.prompt = 'snowctl> '
        else:
            prompt = prompt[:-1]
            self.prompt = f'{prompt}> '.lower()

    def exit_console(self):
        print('closing connections...')
        try:
            self.cursor.close()
            self.conn.close()
        finally:
            sys.exit('exit')

    def listen_signals(self):
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def signal_handler(self, signum, frame):
        if signum == signal.SIGINT or signum == signal.SIGTERM:
            self.exit_console()


def main():
    print(BANNER)
    args = arg_parser()
    conf = Config()
    if args.echo:
        conf.echo_config()
    else:
        conf.write_config(args.configuration)
        logger_options(args.debug)
        conn = snowflake_connect(conf.read_config())
        c = Controller(conn, args.safe)
        c.run_console()


if __name__ == '__main__':
    main()
