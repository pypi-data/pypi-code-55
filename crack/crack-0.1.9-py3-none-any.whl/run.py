# -*- coding: utf-8 -*-
# @author: leesoar
# @email: secure@tom.com
# @email2: employ@aliyun.com

import argparse

from crack import __version__

optional_title = 'optional arguments'


class CapitalisedHelpFormatter(argparse.HelpFormatter):
    def __init__(self, prog):
        super(CapitalisedHelpFormatter, self).__init__(prog,
                                                       indent_increment=2,
                                                       max_help_position=30,
                                                       width=200)
        self._action_max_length = 20

    def add_usage(self, usage, actions, groups, prefix=None):
        if prefix is None:
            prefix = 'Usage: '
        return super(CapitalisedHelpFormatter, self).add_usage(
            usage, actions, groups, prefix)

    class _Section(object):

        def __init__(self, formatter, parent, heading=None):
            self.formatter = formatter
            self.parent = parent
            self.heading = heading
            self.items = []

        def format_help(self):
            # format the indented section
            if self.parent is not None:
                self.formatter._indent()
            join = self.formatter._join_parts
            item_help = join([func(*args) for func, args in self.items])
            if self.parent is not None:
                self.formatter._dedent()

            # return nothing if the section was empty
            if not item_help:  return ''

            # add the heading if the section was non-empty
            if self.heading is not argparse.SUPPRESS and self.heading is not None:
                current_indent = self.formatter._current_indent
                if self.heading == optional_title:
                    heading = '%*s\n%s:\n' % (current_indent, '', self.heading.title())
                else:
                    heading = '%*s%s:' % (current_indent, '', self.heading.title())
            else:
                heading = ''

            return join(['\n', heading, item_help])


parser = argparse.ArgumentParser(description=f"Crack everything.", prog="crack",
                                 formatter_class=CapitalisedHelpFormatter, add_help=False)
parser.add_argument('-v', '--version', action='version', version=__version__, help='Get version of anole')
parser.add_argument('-h', '--help', action='help', help='Show help message')


def run():
    return "Powered by leesoar.com"
