# -*-coding:utf-8-*-

import os
import argparse
import shutil
import json
from .gui import (color, gui)
from .util import *
from .build import Build


# build function
def exec_build(args):
    args_dict = vars(args)
    m_dir = args_dict['dir']
    out = args_dict['out']
    biz = args_dict['biz']

    build_worker = Build()
    build_worker.buildTask(m_dir, out, biz)


def exec_env(args):
    args_dict = vars(args)
    build_worker = Build()
    build_worker.envCheck()


def main():
    print('\r\n')

    cui.i('*************** AntCardSDK CLI Tools ***************')
    root_dir = os.getcwd()
    cui.i('current workspace : ' + root_dir)

    # entry
    parser = argparse.ArgumentParser()

    sub_parser = parser.add_subparsers(title='',
                                       description='',
                                       help='')

    # build command 
    build_parser = sub_parser.add_parser('build', help='build vue template')
    build_parser.add_argument('--dir', required=True, help='path to vue template project workspace')
    build_parser.add_argument('--biz', required=True, help='template biz code')
    build_parser.add_argument('--out', required=False, help='path to build template output')
    build_parser.set_defaults(func=exec_build)
    # env check 
    build_parser = sub_parser.add_parser('env', help='upgrade build tools')
    build_parser.set_defaults(func=exec_env)
    #
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
