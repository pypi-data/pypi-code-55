# Copyright 2014-2019 The Meson development team

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import typing as T
import xml.etree.ElementTree as ET

from .vs2010backend import Vs2010Backend
from ..interpreter import Interpreter
from ..build import Build


class Vs2019Backend(Vs2010Backend):
    def __init__(self, build: T.Optional[Build], interpreter: T.Optional[Interpreter]):
        super().__init__(build, interpreter)
        self.name = 'vs2019'
        if self.environment is not None:
            comps = self.environment.coredata.compilers.host
            if comps and all(c.id == 'clang-cl' for c in comps.values()):
                self.platform_toolset = 'llvm'
            elif comps and all(c.id == 'intel-cl' for c in comps.values()):
                c = list(comps.values())[0]
                if c.version.startswith('19'):
                    self.platform_toolset = 'Intel C++ Compiler 19.0'
                # We don't have support for versions older than 2019 right now.
            if not self.platform_toolset:
                self.platform_toolset = 'v142'
            self.vs_version = '2019'
        # WindowsSDKVersion should be set by command prompt.
        sdk_version = os.environ.get('WindowsSDKVersion', None)
        if sdk_version:
            self.windows_target_platform_version = sdk_version.rstrip('\\')

    def generate_debug_information(self, link):
        # valid values for vs2019 is 'false', 'true', 'DebugFastLink', 'DebugFull'
        ET.SubElement(link, 'GenerateDebugInformation').text = 'DebugFull'
