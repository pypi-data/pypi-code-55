#!/usr/bin/env python
# -*- coding: utf-8 -*-

#################
## monitors.py ##
#################

# type = module
# full name = rktools.monitors 

#############
## Imports ##
#############

from tqdm import tqdm


#################
## ProgressBar ##
#################

class ProgressBar: 

    ################
    ## __init__() ##
    ################

    def __init__(self, 
                 max_value, desc='Loading: ', 
                 position = None, 
                 disable = False, 
                 ascii = False, 
                 bar_format = "{l_bar}{bar:100}{r_bar}{bar:-10b}",
                 dynamic_ncols = True):
        """
        Parameters:
        -----------
        * max_value: int
            ...

        * desc: string
            ...

        * position: int
            ...
        
        * disable: boolean
            If true, the progress bar is not displayed.

        * ascii: boolean
            False by default, and the progress bar is plain. True and the bar is like that '...#####3'

        """
        self.max_value = max_value
        self.desc = desc
        self.position = position
        self.disable = disable
        self.ascii = ascii 
        self.bar_format = bar_format
        self.dynamic_ncols = dynamic_ncols

        self.p = self.pbar()

    ############
    ## pbar() ##
    ############

    def pbar(self):
        if self.position is not None:
            return tqdm(
                total = self.max_value,
                desc = self.desc,
                position = self.position,
                disable = self.disable,
                ascii = self.ascii,
                bar_format = self.bar_format,
                dynamic_ncols = self.dynamic_ncols
            )
        else:
            return tqdm(
                total = self.max_value,
                desc = self.desc,
                disable = self.disable,
                ascii = self.ascii,
                bar_format = self.bar_format,
                dynamic_ncols = self.dynamic_ncols
            )

    def update(self, update_value):
        self.p.update(update_value)

    def write(self, msg):
        self.p.write(msg)

    def close(self):
        self.p.close()



