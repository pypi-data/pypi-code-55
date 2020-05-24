from logging import Logger
from typing import Any

from vortex.DeferUtil import deferToThreadWrapWithLogger

from peek_plugin_base.storage.DbConnection import DbSessionCreator


def runPyInPg(logger: Logger,
              dbSessionCreator: DbSessionCreator,
              classMethodToRun: Any,
              *args,
              **kwargs) -> Any:
    return deferToThreadWrapWithLogger(logger) \
        (runPyInPgBlocking) \
        (dbSessionCreator, classMethodToRun, *args, **kwargs)


def runPyInPgBlocking(dbSessionCreator: DbSessionCreator,
                      classMethodToRun: Any,
                      *args,
                      **kwargs) -> Any:
    from peek_storage.plpython.RunPyInPg import runPyInPgBlocking
    return runPyInPgBlocking(dbSessionCreator,
                             classMethodToRun,
                             *args,
                             **kwargs)
