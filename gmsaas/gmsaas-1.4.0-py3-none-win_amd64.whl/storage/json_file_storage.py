# Copyright 2019 Genymobile
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
"""
File Storage using JSON format
"""

import os
import json

from gmsaas.storage.storage import BaseStorage


class JsonFileStorage(BaseStorage):
    """ Storage implementation that keeps object in a json file """

    def __init__(self, filename, target_version, permission_flags=None):
        self.filename = filename
        self.permission_flags = permission_flags
        BaseStorage.__init__(self, target_version)

    def _load(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as json_file:
                return json.load(json_file)
        except:
            return {}

    def _save(self, data):
        with open(self.filename, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=True)
            if self.permission_flags:
                os.chmod(self.filename, self.permission_flags)
