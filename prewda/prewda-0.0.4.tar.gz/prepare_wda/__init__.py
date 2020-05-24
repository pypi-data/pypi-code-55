#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__PROJECT_NAME__ = r"prewda"
__AUTHOR__ = r"ssfanli"
__AUTHOR_EMAIL__ = r"freedomlidi@163.com"
__LICENSE__ = r"MIT"
__URL__ = r"https://github.com/ssfanli/prepare-wda.git"
__VERSION__ = r"0.0.4"
__DESCRIPTION__ = r"a python wrapper for WebDriverAgent prepare"

import os
import functools
from loguru import logger
import prepare_wda


def prepare(xcodebuild: str, wda_fp: str, udid: str):
    """prepare wda

    xcodebuild: specified a xcodebuild, such as the default of MacOS xcodebuild
        or 'xxx/Xcode10.3.app/Contents/Developer/usr/bin/xcodebuild'
    wda_fp: WebDriverAgent path
    udid: ios device udid

    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            wda_shell = os.path.join(
                os.path.dirname(prepare_wda.__file__),
                'wda.sh')
            logger.info(
                f'\nwda_shell: {wda_shell}'
                f'\nxcodebuild: {xcodebuild}'
                f'\nwda_fp: {wda_fp}'
                f'\nudid: {udid}'
            )
            try:
                error_code = os.system(f'{wda_shell} {xcodebuild} {wda_fp} {udid}')
                assert not error_code, f'wda.sh error_code: {error_code}'
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(e)
            finally:
                os.system("ps -ef | grep WebDriverAgentRunner | grep -v grep | awk '{print $2}' | xargs kill")
        return wrapper
    return decorator
