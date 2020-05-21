#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from cpt.packager import ConanMultiPackager
from cpt.builds_generator import BuildGenerator, get_mingw_builds, get_visual_builds, get_linux_clang_builds, get_linux_gcc_builds, get_osx_apple_clang_builds

def _get_builds(self, pure_c, shared_option_name, dll_with_static_runtime, reference=None, build_all_options_values=None):
  ref = reference or self._reference
  if self._os_name in ["Android", "Emscripten"]:
    return get_linux_clang_builds(self._clang_versions, self._archs, shared_option_name,
                                  pure_c, self._build_types, self._cppstds, self._options, ref)
  else:
    raise Exception("Unknown operating system: %s" % self._os_name)

def get_builder():
  platform_info = None
  build_for = os.getenv('SESAME_BUILD_FOR', '')
  if build_for == 'android':
    BuildGenerator.get_builds = _get_builds
    class AndroidPlatformInfo(object):
      @staticmethod
      def system():
        return 'Android'
    platform_info = AndroidPlatformInfo()
  elif build_for == 'emscripten':
    BuildGenerator.get_builds = _get_builds
    class EmscriptenPlatformInfo(object):
      @staticmethod
      def system():
        return 'Emscripten'
    platform_info = EmscriptenPlatformInfo()

  builder = ConanMultiPackager(platform_info=platform_info)
  return builder
