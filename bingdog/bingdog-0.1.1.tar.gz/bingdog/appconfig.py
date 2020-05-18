import yaml
from bingdog.util import ifNone, NullPointerException

class Configurator(object):
    __configurator = None
    
    def __init__(self, confPath = "bingdog.conf"):
        self._config = None
        self.__flowDiagramPath = None
        with open(confPath, "r", "utf-8") as f:
            self._config = yaml.load(f)
    
    def initialize(confClass, *args, **kwargs):
        if issubclass(confClass, Configurator) or confClass is Configurator:
            if __configurator == None:
                __configurator = confClass(*args, **kwargs)
        else:
            raise ConfiguratorException(confClass)
    
    def getConfigurator():
        return ifNone(__configurator)
    
    @property
    def flowDiagramPath(self):
        if self.__flowDiagramPath is None:
            application = self._config.get("application")
            task = ifNone(application).get("task")
            self.__flowDiagramPath = ifNone(task).get("flow_file_path")
        return self.__flowDiagramPath
        
    @flowDiagramPath.setter    
    def flowDiagramPath(self, path):
        self.__flowDiagramPath = path
    
    def getLoggingLevel(self):
        try:
            application = self._config.get("application")
            logger = ifNone(application).get("logger")
            return ifNone(logger).get("level")
        except NullPointerException as e:
            return "info"
    
    def getLoggingFormat(self):
        try:
            application = self._config.get("application")
            logger = ifNone(application).get("logger")
            return ifNone(logger).get("format")
        except NullPointerException as e:
            return "%(levelname)s:%(asctime)s:%(message)s"
            
    def getLoggingFilePath(self):
        try:
            application = self._config.get("application")
            logger = ifNone(application).get("logger")
            return IfNone(logger).get("log_file_path")
        except NullPointerException as e:
            return "bingdog.log"
            
class ConfiguratorException(Exception):
    def __init__(self, confClass):
        super().__init__(confClass, " is not a class of Configurator.")
        
    