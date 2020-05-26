import time
import os

import colorama
from colorama import Fore, Back, Style
import cursor

fore_colors_list = [Fore.BLACK, Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE, Fore.RESET]
back_colors_list = [Back.BLACK, Back.RED, Back.GREEN, Back.YELLOW, Back.BLUE, Back.MAGENTA, Back.CYAN, Back.WHITE, Back.RESET]
styles_list = [Style.DIM, Style.NORMAL, Style.BRIGHT, Style.RESET_ALL]
colors_names_list = ['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white', 'reset']
styles_names_list = ['dim', 'normal', 'bright', 'reset']


class Logger:
    def __init__(self, title=None, size=tuple(), hide_cursor=True, debug_mode=False):
        colorama.init()
        if title:
            os.system('title {}'.format(title))
        if size:
            os.system('mode {y}, {x}'.format(y=size[0], x=size[1]))
        if hide_cursor:
            cursor.hide()
        else:
            cursor.show()
        self.fore_colors = dict(zip(colors_names_list, fore_colors_list))
        self.back_colors = dict(zip(colors_names_list, back_colors_list))
        self.styles = dict(zip(styles_names_list, styles_list))
        self.cursor_state = hide_cursor
        self.window_title = title
        self.debug_mode = debug_mode

    def printl(self, *text, group='INFO', fore='white', back='reset', style='normal', log_time=None, sep=' ', end='\n', flush=False, file=None):
        fore_color = self.fore_colors[fore]
        back_color = self.back_colors[back] if back else back
        style = self.styles[style]
        group = '[{}]'.format(group).ljust(13)
        log_time = time.strftime('<%H:%M:%S %d/%m/%y>').ljust(23) if not log_time else log_time

        text = sep.join(text)

        print(fore_color + back_color + style + log_time + group + text + self.styles['reset'], end=end, flush=flush, file=file)

    def log(self, *text, sep=' '):
        self.printl(*text, group='LOG', fore='white', sep=sep)

    def info(self, *text, sep=' '):
        self.printl(*text, group='INFO', fore='cyan', sep=sep)

    def warning(self, *text, sep=' '):
        self.printl(*text, group='WARNING', fore='yellow', sep=sep)

    def error(self, *text, sep=' '):
        self.printl(*text, group='ERROR', fore='red', sep=sep)

    def debug(self, *text, sep=' '):
        if self.debug_mode:
            self.printl(*text, group='DEBUG', fore='magenta', sep=sep)

    @staticmethod
    def reset_all():
        print('\033[0m', end='')

    @property
    def cursor_state(self):
        return self.cursor_state

    @cursor_state.setter
    def cursor_state(self, setter):
        if setter:
            cursor.show()
        else:
            cursor.hide()

    @property
    def window_title(self):
        return self.window_title

    @window_title.setter
    def window_title(self, title):
        os.system(f'title {title}')
