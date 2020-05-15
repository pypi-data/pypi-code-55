import sys
import logging

# to support logging output in tests:
logging.basicConfig(
    handlers=[logging.StreamHandler(sys.stdout)],
    level=logging.INFO
)
