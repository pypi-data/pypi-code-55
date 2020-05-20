#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import platform
from conans.client.conan_api import Conan
from sesame import build_shared

import cpt.builds_generator

def get_builder(pure_c=False):
    os_build = {
        'Windows': 'Windows',
        'Darwin': 'Macos',
        'Linux': 'Linux'}.get(platform.system())

    builder = build_shared.get_builder()
    builder.add_common_builds(pure_c=pure_c)
    builder.remove_build_if(lambda build: 'compiler.libcxx' in build.settings and build.settings['compiler.libcxx'] == 'libstdc++')
    for build_conf in builder.items:
      build_conf.settings['arch_build'] = 'x86_64'
      build_conf.settings['os_build'] = os_build

    return builder
