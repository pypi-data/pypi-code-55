
from configparser import RawConfigParser
import os.path
import sys

this = sys.modules[__name__]
this.google = {}

home = os.path.expanduser('~')

# If ~/.iox_profile exists, read it
config_file = os.path.join(home, '.ioxrc')
if os.path.exists(config_file):
    # Parse the configuration file
    parser = RawConfigParser()
    parser.read(config_file)

    # Get credentials
    this.google['credentials'] = parser.get('google', 'credentials')






