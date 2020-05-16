import sys
sys.path.insert(0, '/opt/finac')

import finac as f
import finac.api as api

import logging
import os

from pyaltt2.config import load_yaml

from server import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
