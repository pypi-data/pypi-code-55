# -*- coding: utf-8 -*-
# @author: leesoar
# @email: secure@tom.com
# @email2: employ@aliyun.com

import argparse

from crack.setting import __version__


parser = argparse.ArgumentParser(description=f"Fake everything.", prog="anole", add_help=False)
parser.add_argument('-v', '--version', action='version', version=__version__, help='Get version of anole')
parser.add_argument('-h', '--help', action='help', help='Show help message')


def run():
    return "Powered by leesoar.com"
