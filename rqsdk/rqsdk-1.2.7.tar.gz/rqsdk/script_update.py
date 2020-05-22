# -*- coding: utf-8 -*-
#
# Copyright 2016 Ricequant, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import subprocess
import sys

import click

from rqsdk.const import BASH_FILE, EXTRA_INDEX_URL


def pip_install(full_name, index_url):
    command = "install -U -i {} {} {}".format(index_url, EXTRA_INDEX_URL, full_name)
    if sys.platform.startswith("win"):
        script_update = os.path.join(os.path.dirname(os.path.abspath(__file__)), "script_update.py")
        python_path = sys.executable
        subprocess.Popen("{} {} {}".format(python_path, script_update, command), shell=True)
        sys.exit(1)
    else:
        update_processing(command.split())


def update_processing(args):
    """启动子进程更新rqsdk"""
    try:
        from pip import main
    except ImportError:
        from pip._internal import main
    main(list(args))
    if sys.platform.startswith("win"):
        click.echo("请输入Enter继续...")
    return


def update_bash_file(rqdatac_uri):
    for _file in BASH_FILE:
        _path = os.path.join(os.path.expanduser("~"), _file)
        if not os.path.exists(_path):
            continue
        lines = open(_path, "r", encoding="utf8").readlines()
        flag = False
        for line in lines:
            if "export RQDATAC2_CONF=" in line:
                lines[lines.index(line)] = "export RQDATAC2_CONF={} \n".format(rqdatac_uri)
                flag = True

        if flag is False:
            lines.append("export RQDATAC2_CONF={} \n".format(rqdatac_uri))

        with open(_path, "w", encoding="utf8")as f:
            f.writelines(lines)


if __name__ == '__main__':
    update_processing(sys.argv[1:])
