from .. import utils
import os

CONFIG = utils.load_config(".pipemaker/config.yaml")
CREDS = utils.load_config(".pipemaker/creds.yaml")

# for testing creds are in environment variables
if CONFIG.server == "cloudamqp" and "cloudamqp_user" in os.environ:
    CREDS.cloudamqp.host = os.environ["cloudamqp_host"]
    CREDS.cloudamqp.user = os.environ["cloudamqp_user"]
    CREDS.cloudamqp.password = os.environ["cloudamqp_password"]
    CREDS.cloudamqp.vhost = os.environ["cloudamqp_vhost"]

if CONFIG.qtype == "qrabbit":
    from ..qrabbit.taskq import Taskq, TaskqP
    from ..qrabbit import loghandler
    from ..qrabbit.workerq import Workerq, WorkerqP
    from ..qrabbit.eventq import Eventq, EventqP
else:
    from ..qpython.taskq import Taskq, TaskqP
    from ..qpython import loghandler
    from ..qpython.workerq import Workerq, WorkerqP
    from ..qpython.eventq import Eventq, EventqP

from .taskdb import TaskDB
