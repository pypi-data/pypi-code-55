"""

Privacy1 AB CONFIDENTIAL
________________________

 [2017] - [2018] Privacy1 AB
 All Rights Reserved.

 NOTICE:  All information contained herein is, and remains the property
 of Privacy1 AB.  The intellectual and technical concepts contained herein
 are proprietary to Privacy1 AB and may be covered by European, U.S. and Foreign
 Patents, patents in process, and are protected by trade secret or copyright law.

 Dissemination of this information or reproduction of this material
 is strictly forbidden.
 """

class ServiceData:

    SERVICE_KEY_TITLE = "key"
    SERVICE_NAME_TITLE = "name"
    SERVICE_ACCESS_TITLE = "requiredAccessLevel"

    def __init__(self, serviceName, serviceKey, accessLevel):
        self.serviceName = serviceName
        self.servicekey = serviceKey
        self.accessLevel = accessLevel
        self.sessionToken = ""
        self.refreshToken = ""

    def getServiceName(self):
        return self.serviceName

    def getServicekey(self):
        return self.servicekey

    def getAccessLevel(self):
        return self.accessLevel

    def setSessionToken(self, sessionToken):
        self.sessionToken = sessionToken

    def getSessionToken(self):
        return self.sessionToken

    def setRefreshToken(self, refreshToken):
        self.refreshToken = refreshToken

    def getRefreshToken(self):
        return self.refreshToken
