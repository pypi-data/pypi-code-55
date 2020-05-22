from conML.controller import get_settings
from conML.controller import knowledge_searcher
from conML.controller import load_settings
from conML.controller import load_knowledge
from conML.controller import construction
from conML.controller import feature_selection
from conML.controller import reconstruction
from conML.controller import deconstruction


def _load_default_settings():
    from os.path import join, expanduser, exists
    path = join(expanduser('~'), ".conML", "settings.ini")
    if exists(path): load_settings(path)


def _setup_loggers():
    from logging import addLevelName, Logger, config
    from os.path import join, abspath
    from inspect import getsourcefile

    protocol_level = 55
    addLevelName(protocol_level, "PROTOCOL")

    def protocol(self, message, *args, **kwargs):
        if self.isEnabledFor(protocol_level):
            self._log(protocol_level, message, args, **kwargs)
    Logger.protocol = protocol
    logging_config = join(abspath(getsourcefile(lambda: None))[:-11],
                          "static/logging.ini")
    config.fileConfig(logging_config)


_load_default_settings()
_setup_loggers()
