"""
This is the core file to import into any notebook or program to create a pipeline.
It is only needed for the master not for the workers
"""
from .utils.defaultlog import log

from .master.pipeline import Pipeline

pipeline = Pipeline()
from .filesystem import Filepath, Fpath

# todo include environment in task and worker e.g. conda, python requirements, docker image + files

# todo run multiple threads per worker
#    # other multiprocess methods

# todo enable prioritise, pause, cancel, terminate, timeout. cannot do this for FIFO workerqP. same with celery.
# todo convert pkl to excel
# todo keep selection as well as sort order on refresh
