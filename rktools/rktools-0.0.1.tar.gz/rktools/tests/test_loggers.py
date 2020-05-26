#!/usr/bin/env python
# -*- coding: utf-8 -*-

#####################
## test_loggers.py ##
#####################

# Execute:
# (base) $ source ~/venvs/rklearn-lib/bin/activate 
# (rklearn-lib) (base) $ cd rktools/tests/
# (rklearn-lib) (base) $ python rktools/tests/test_loggers.py --conf=rktools/tests/config/config.yaml   

import os
import sys
import argparse
import yaml
import unittest 
import logging 

from rktools.loggers import init_logger 

#############
## Globals ##
#############

# The logger should always be used globally like this
logger = None

# The cmd line arguments flags
flags = None

#################
## TestLoggers ##
#################

class TestLoggers(unittest.TestCase):

    ##############
    ## setUp()  ##
    ##############

    def setUp(self):
        print("[INFO] In self.setUp()...")
        assert(logger != None)


    ##########################
    ## test_logger_basics() ##
    ##########################

    def test_logger_basics(self):
        print("[INFO] In self.test_logger_basics()...")

        logger.debug("A debug message!")
        logger.info("A info message!")
        logger.warning("A warn message!")
        logger.error("A error message!")
        logger.critical("A critical message!")

    #########################
    ## test_logs_rolling() ##
    #########################

    
    def test_logs_rolling(self):
    
        print("[INFO] In test_logs_rolling()...")

        dummy = "This dummy sentence is repeated again and again..."
        size = 0
        logger.info("Writing 1000 times the dummy sentence...")
        for _ in range(1, 1000):
            logger.debug(dummy)
            size += len(dummy)
            logger.info("Log size > {}".format(size))

        logger.info("Done.")


    def tearDown(self):
        print("[INFO] In self.tearDown()...")

# end TestLoggers 

###################
## parse_args()  ##
###################

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--conf", help="Path to the YAML configuration file", required=True,)
    ns, args = parser.parse_known_args(namespace=unittest)
    return ns, sys.argv[:1] + args

###############                                                                                                                    
## __main__  ##
###############

if __name__ == '__main__':

    flags, argv = parse_args()
    sys.argv[:] = argv

    with open(flags.conf, 'r') as ymlfile:
        config = yaml.load(ymlfile, Loader=yaml.FullLoader)

    logger = init_logger(name="test_loggers", 
                         config = config, 
                         level=logging.getLevelName(config["logger"]["log_level"].upper()))

    unittest.main()

