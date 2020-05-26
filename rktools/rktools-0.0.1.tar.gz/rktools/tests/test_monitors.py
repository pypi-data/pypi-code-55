#!/usr/bin/env python
# -*- coding: utf-8 -*-

#######################
## test_monitors.py  ##
#######################

# Execute:
# (base) $ source ~/venvs/rklearn-lib/bin/activate 
# (rklearn-lib) (base) $ python rktools/tests/test_monitors.py --conf rktools/tests/config/config.yaml   

import sys
import time
import argparse
import yaml
import unittest 
import logging 

from rktools.loggers import init_logger 
from rktools.monitors import ProgressBar

#############
## Globals ##
#############

LOGGER = None

##################
## TestMonitors ##
##################

class TestMonitors(unittest.TestCase):

    ##############
    ## setUp()  ##
    ##############

    def setUp(self):
        assert(LOGGER != None)
        LOGGER.info("In self.setUp()...")

    ############################
    ## test_simple_progress() ##
    ############################

    def test_simple_progress(self):
        
        assert(LOGGER != None)
        LOGGER.info("In test_simple_progress()...")
        max = 10
        cpt = -1
        self.progress_bar = ProgressBar(max_value = max)

        for i in range(1, max+1):
            time.sleep(1)
            cpt = i
            self.progress_bar.update(1)
        self.progress_bar.close()

        LOGGER.info("At the end, cpt = {}".format(cpt))

    ####################################
    ## test_simple_progress_ascii_1() ##
    ####################################

    def test_simple_progress_ascii_1(self):
        
        assert(LOGGER != None)
        LOGGER.info("In test_simple_progress_ascii_1()...")
        max = 10
        cpt = -1
        self.progress_bar = ProgressBar(max_value = max, ascii = True)

        for i in range(1, max+1):
            time.sleep(1)
            cpt = i
            self.progress_bar.update(1)
        self.progress_bar.close()

        LOGGER.info("At the end, cpt = {}".format(cpt))

    #################################
    ## test_simple_progress_desc() ##
    #################################

    def test_simple_progress_desc(self):
        
        assert(LOGGER != None)
        LOGGER.info("In test_simple_progress_desc()...")
        max = 10
        cpt = -1
        self.progress_bar = ProgressBar(max_value = max)

        for i in range(1, max+1):
            time.sleep(1)
            cpt = i
            self.progress_bar.p.set_description("Bar desc (file %i)" % i)
            self.progress_bar.p.refresh()
            self.progress_bar.update(1)
        self.progress_bar.close()

        LOGGER.info("At the end, cpt = {}".format(cpt))


    ################
    ## tearDown() ##
    ################

    def tearDown(self):
        LOGGER.info("In self.tearDown()...")


# end TestMonitors

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

    FLAGS, argv = parse_args()
    sys.argv[:] = argv

    with open(FLAGS.conf, 'r') as ymlfile:
        config = yaml.load(ymlfile, Loader=yaml.FullLoader)

    LOGGER = init_logger(name="test_monitors", 
                         config = config, 
                         level=logging.getLevelName(config["logger"]["log_level"].upper()))

    unittest.main()







