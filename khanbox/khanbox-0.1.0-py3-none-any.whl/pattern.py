from typing import Pattern
import re

#2020-03-25 13:56:40,848
DATETIME = re.compile(r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2}) (?P<hour>\d{2}):(?P<minute>\d{2})")