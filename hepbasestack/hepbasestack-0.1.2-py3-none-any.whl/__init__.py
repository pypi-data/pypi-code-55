"""
Miscellaneous tools
"""

__version__ = '0.1.2'
__all__ = ["visual","itools","logger", "colors", "layout"]

import resource
import concurrent.futures as fut
import tqdm
import time

from . import logger
from . import visual

Logger = logger.Logger


########################################################

def _progbar(runtime):
    """
    Helper function showing a timed progress bar

    Args:
        runtime (int) : max time of the progressbar in seconds
    """

    for k in tqdm.tqdm(range(int(runtime))):
        time.sleep(1)

########################################################

def timed_progressbar(runtime):
    """
    Show a progress bar increasing every second for runtime seconds.
    This runs in its own thread, so the program can continue in the 
    meantime. This can be useful for while loops which run for a certain 
    time for example.

    Args:
        runtime (int) : maxtime of the progress bar in seconds
    """
    ex = fut.ProcessPoolExecutor(max_workers=1)
    ex.submit(_progbar, runtime)
    return ex

########################################################

def timeit(func):
    """
    Use as decorator to get the effective execution time of the decorated function

    Args:
        func (func): Measure the execution time of this function

    Returns:
        func: wrapped func
    """

    from time import time


    def wrapper(*args,**kwargs):
        t1 = time()
        res = func(*args,**kwargs)
        t2 = time()
        seconds = t2 -t1
        mins  = int(seconds)/60
        hours = int(seconds)/3600
        res_seconds  = int(seconds)%3600
        mins         = int(res_seconds)/60
        left_seconds = int(res_seconds)%60
        Logger.info('Execution of {0} took {1} hours, {2} mins and {3} seconds'.format(func.__name__, hours, mins, left_seconds))
        Logger.info('Execution of {0} took {1} seconds'.format(func.__name__,seconds))
        max_mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        Logger.info('Execution might have needed {0} kB in memory (highly uncertain)!'.format(max_mem))
        return res

    return wrapper

#####################################################################

def isnotebook():
    """
    Identify if a session is run in an jupyter notebook

    Taken from https://stackoverflow.com/questions/15411967/how-can-i-check-if-code-is-executed-in-the-ipython-notebook
    """

    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True   # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False      # Probably standard Python interpreter

