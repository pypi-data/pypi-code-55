#
# Copyright (c) 2020-present, wobe-systems GmbH
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#

""" utility functions """

import logging

log = logging.getLogger(__name__)


def print_pretty_bytes(value):
    chunk_size = 16
    chunks = (value[i : i + chunk_size] for i in range(0, len(value), chunk_size))

    for chunk in chunks:
        hex_values = ""
        char_values = ""

        for val in chunk:
            hex_values += f"{val:02x} "
            char_values += "." if val < 32 else chr(val)

        log.debug(hex_values + char_values)
