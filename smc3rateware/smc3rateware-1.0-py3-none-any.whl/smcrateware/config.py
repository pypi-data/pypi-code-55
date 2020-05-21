import os
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)

class SMC3RatewareConfig:
    ENDPOINT = 'http://demo.smc3.com/AdminManager/services/RateWareXL'

class TestingConfig:
    root_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'tests')
    logging.debug('testing root_dir: %s' % root_dir)