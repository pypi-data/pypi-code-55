import os
from . import Singleton

class Config(metaclass=Singleton):
    FIELD_VALUE = 0
    FIELD_DESCRIPTION = 1

    def __init__(self, configFileName):
        self.configFileName = configFileName
        self.configs = self.__load()

    def __load(self):
        configs = {}
        if os.path.exists(self.configFileName):
            with open(self.configFileName, 'r') as f:
                data = f.read().split('\n')
            for d in data:
                description = ''
                if '#' in d:
                    _d = d.split('#')
                    description = _d[1]
                    d = _d[0]
                d = d.split('=')
                key = d[0].replace(' ', '')
                value = d[1].strip()
                configs[key] = (value, description)
        return configs       

    def getValue(self, key):
        try:
            return self.getValueAndDescription(key)[0]
        except Exception as e:
            raise e

    def getDescription(self, key):
        try:
            return self.getValueAndDescription(key)[1]
        except Exception as e:
            raise e

    def getValueAndDescription(self, key):
        if key in list(self.configs.keys()):
            return self.configs[key]
        raise Exception('No Config Key')

if __name__ == '__main__':
    config = Config()
    print (config.getValue('StockDailyDataPath'))
    print (config.getDescription('StockDailyDataPath'))