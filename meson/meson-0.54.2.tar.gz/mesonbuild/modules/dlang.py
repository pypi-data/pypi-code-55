# Copyright 2018 The Meson development team

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This file contains the detection logic for external dependencies that
# are UI-related.

import json
import os

from . import ExtensionModule

from .. import mlog

from ..mesonlib import (
    Popen_safe, MesonException
)

from ..dependencies.base import (
    ExternalProgram, DubDependency
)

from ..interpreter import DependencyHolder

class DlangModule(ExtensionModule):
    class_dubbin = None
    init_dub = False

    def __init__(self, interpreter):
        super().__init__(interpreter)
        self.snippets.add('generate_dub_file')

    def _init_dub(self):
        if DlangModule.class_dubbin is None:
            self.dubbin = DubDependency.class_dubbin
            DlangModule.class_dubbin = self.dubbin
        else:
            self.dubbin = DlangModule.class_dubbin

        if DlangModule.class_dubbin is None:
            self.dubbin = self.check_dub()
            DlangModule.class_dubbin = self.dubbin
        else:
            self.dubbin = DlangModule.class_dubbin

        if not self.dubbin:
            if not self.dubbin:
                raise MesonException('DUB not found.')

    def generate_dub_file(self, interpreter, state, args, kwargs):
        if not DlangModule.init_dub:
            self._init_dub()

        if len(args) < 2:
            raise MesonException('Missing arguments')

        config = {
            'name': args[0]
        }

        config_path = os.path.join(args[1], 'dub.json')
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf8') as ofile:
                try:
                    config = json.load(ofile)
                except ValueError:
                    mlog.warning('Failed to load the data in dub.json')

        warn_publishing = ['description', 'license']
        for arg in warn_publishing:
            if arg not in kwargs and \
               arg not in config:
                mlog.warning('Without', mlog.bold(arg), 'the DUB package can\'t be published')

        for key, value in kwargs.items():
            if key == 'dependencies':
                config[key] = {}
                if isinstance(value, list):
                    for dep in value:
                        if isinstance(dep, DependencyHolder):
                            name = dep.method_call('name', [], [])
                            ret, res = self._call_dubbin(['describe', name])
                            if ret == 0:
                                version = dep.method_call('version', [], [])
                                if version is None:
                                    config[key][name] = ''
                                else:
                                    config[key][name] = version
                elif isinstance(value, DependencyHolder):
                    name = value.method_call('name', [], [])
                    ret, res = self._call_dubbin(['describe', name])
                    if ret == 0:
                        version = value.method_call('version', [], [])
                        if version is None:
                            config[key][name] = ''
                        else:
                            config[key][name] = version
            else:
                config[key] = value

        with open(config_path, 'w', encoding='utf8') as ofile:
            ofile.write(json.dumps(config, indent=4, ensure_ascii=False))

    def _call_dubbin(self, args, env=None):
        p, out = Popen_safe(self.dubbin.get_command() + args, env=env)[0:2]
        return p.returncode, out.strip()

    def check_dub(self):
        dubbin = ExternalProgram('dub', silent=True)
        if dubbin.found():
            try:
                p, out = Popen_safe(dubbin.get_command() + ['--version'])[0:2]
                if p.returncode != 0:
                    mlog.warning('Found dub {!r} but couldn\'t run it'
                                 ''.format(' '.join(dubbin.get_command())))
                    # Set to False instead of None to signify that we've already
                    # searched for it and not found it
                    dubbin = False
            except (FileNotFoundError, PermissionError):
                dubbin = False
        else:
            dubbin = False
        if dubbin:
            mlog.log('Found DUB:', mlog.bold(dubbin.get_path()),
                     '(%s)' % out.strip())
        else:
            mlog.log('Found DUB:', mlog.red('NO'))
        return dubbin

def initialize(*args, **kwargs):
    return DlangModule(*args, **kwargs)
