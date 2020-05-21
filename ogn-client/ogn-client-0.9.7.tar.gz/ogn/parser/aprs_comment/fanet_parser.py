import re

from ogn.parser.utils import FPM_TO_MS
from ogn.parser.pattern import PATTERN_FANET_POSITION_COMMENT, PATTERN_FANET_STATUS_COMMENT

from .base import BaseParser


class FanetParser(BaseParser):
    def __init__(self):
        self.beacon_type = 'fanet'
        self.position_parser = PATTERN_FANET_POSITION_COMMENT
        self.status_parser = PATTERN_FANET_STATUS_COMMENT

    def parse_position(self, aprs_comment):
        ac_match = self.position_parser.match(aprs_comment)
        return {'address_type': int(ac_match.group('details'), 16) & 0b00000011 if ac_match.group('details') else None,
                'aircraft_type': (int(ac_match.group('details'), 16) & 0b01111100) >> 2 if ac_match.group('details') else None,
                'stealth': (int(ac_match.group('details'), 16) & 0b10000000) >> 7 == 1 if ac_match.group('details') else None,
                'address': ac_match.group('address') if ac_match.group('address') else None,
                'climb_rate': int(ac_match.group('climb_rate')) * FPM_TO_MS if ac_match.group('climb_rate') else None}

    def parse_status(self, aprs_comment):
        match = self.status_parser.match(aprs_comment)
        return {'user_name': match.group('user_name') if match.group('user_name') else None,
                'signal_quality': float(match.group('signal_quality')) if match.group('signal_quality') else None,
                'frequency_offset': float(match.group('frequency_offset')) if match.group('frequency_offset') else None,
                'error_count': int(match.group('error_count')) if match.group('error_count') else None}
