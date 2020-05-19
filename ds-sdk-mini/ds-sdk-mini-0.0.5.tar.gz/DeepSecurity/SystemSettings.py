#  Copyright (c) 2020. Brendan Johnson. All Rights Reserved.

#import connect
#import config

class SystemSettings:
    def __init__(self, config, connection):
        self._config=config
        self._connection = connection
    ##SystemSettings
    def list(self):
        return self._connection.get(url='/systemsettings')
    def modify(self, settingName, payload):
        return self._connection.post(url='/systemsettings/' + str(settingName), data=payload)
    def describe(self, settingName):
        return self._connection.get(url='/systemsettings/' + str(settingName))
    def modify(self, payload):
        return self._connection.post(url='/systemsettings', data=payload)
    def delete(self, settingName):
        return self._connection.delete(url='/systemsettings/' + str(settingName))