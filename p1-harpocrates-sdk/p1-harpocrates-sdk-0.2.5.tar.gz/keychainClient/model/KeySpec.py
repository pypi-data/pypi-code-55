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

class KeySpec:

    def __init__(self, keyVersion, category, key):
        self.keyVersion = keyVersion
        self.category = category
        self.key = key

    def getKeyVersion(self):
        return self.keyVersion

    def getCategory(self):
        return self.category

    def getKey(self):
        return self.key

