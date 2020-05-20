#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import platform
from sesame import build_shared

def get_builder():
    builder = build_shared.get_builder()

    # These are needed for test_packages. Just build for the active platform...
    settings = {}
    os_build = {
        'Windows': 'Windows',
        'Darwin': 'Macos',
        'Linux': 'Linux'}.get(platform.system())

    settings['arch_build'] = 'x86_64'
    settings['os_build'] = os_build

    if os_build == 'Windows':
      settings['compiler.version'] = os.getenv('CONAN_VISUAL_VERSIONS', '16').split(',')[0]
      settings['arch'] = os.getenv('CONAN_ARCHS', 'x86_64').split(',')[0]
    elif os_build == 'Macos':
      settings['compiler.version'] = os.getenv('CONAN_APPLE_CLANG_VERSIONS', '11.0').split(',')[0]
      settings['arch'] = os.getenv('CONAN_ARCHS', 'x86_64').split(',')[0]
    elif os_build == 'Linux':
      settings['compiler.version'] = os.getenv('CONAN_CLANG_VERSIONS', '10').split(',')[0]
      settings['arch'] = os.getenv('CONAN_ARCHS', 'x86_64').split(',')[0]

    builder.add(settings=settings)
    return builder
