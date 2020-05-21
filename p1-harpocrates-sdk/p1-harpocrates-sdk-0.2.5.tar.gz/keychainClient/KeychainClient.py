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
import struct
from datetime import datetime
from cacheout import Cache
from rest.RestCurd import RestCurd
from keychainClient.protobuf import keychain_pb2
from keychainClient.model import KeySpec
from keychainClient.crypto import KeychainEncryptor
from keychainClient.exception import KeychainNotExistException
from rest.exception import RestRequestException

class KeychainClient:

    SERVICE_ENTRY = "/api/v1/service/"
    CONSENT_ENTRY = "/api/v1/consents/"
    RESTRICTIONS_ENTRY = "/api/v1/restrictions/"
    DELETIONS_ENTRY = "/api/v1/deletions/"
    CONSENT_KEY_ENTRY = "/api/v1/keys/"
    CONSENT_CATEGORY_ENTRY = "/api/v1/consentcategory/"
    USER_ENTRY = "/api/v1/users/"
    CRYPTO_ENTRY = "/api/v1/crypto/"

    SERVICE_REFRESH_ENDPOINT = "refreshtoken"
    CONSENT_KEY_ENDPOINT = "key"
    USER_COUNT_ENDPOINT = "count"
    USER_CREATE_ENDPOINT = "user"
    USER_SOFT_DELETE_ENDPOINT = "user/soft"
    USER_HARD_DELETE_ENDPOINT = "user/hard"
    CRYPTO_ENCRYPT_ENDPOINT = "encrypt"
    CRYPTO_DECRYPT_ENDPOINT = "decrypt"

    CONSTANT_USERID_NAME = "userId"
    CONSTANT_HEADER_AUTHORIZATION = "authorization"
    CONSTANT_HEADER_USER_ID = "user-id"
    CONSTANT_BEARER_NAME = "Bearer"
    CONSTANT_PAGE_NUMBER = "pageNumber"
    CONSTANT_PAGE_SIZE = "pageSize"

    def __init__(self, keychainHost, keychainPort, authHost, authPort, accountName, accountPassword,
                 serviceKey, cacheSize=None, expireInSeconds=None):
        """
        Constructor.
        :param keychainHost: keychain host address
        :param keychainPort: keychain host port
        :param authHost: authentication host address
        :param authPort: authentication host port
        :param accountName: the registered backend micro-service account name
        :param accountPassword: the registered backend micro-service account password
        :param serviceKey: the service key for keychain key derivation
        :param cacheSize: consent key cache size
        :param expireInSeconds: consent key cache expiration in seconds
        """
        self.keychainHost = keychainHost
        self.keychainPort = keychainPort
        self.restCurd = RestCurd(authHost, authPort, accountName, accountPassword)
        self.serviceKey = serviceKey
        self.keyCache = Cache(maxsize=cacheSize, ttl=expireInSeconds)
        self.encryptor = KeychainEncryptor()


    def cacheDecorateGetKey():
        def cacheDecorator(func):
            def cacheWrapper(*args):
                cachekey = args[1]
                cacheVal = args[0].keyCache.get(cachekey)
                if cacheVal is None:
                    cacheVal = func(*args)
                    args[0].keyCache.set(cachekey, cacheVal)
                return cacheVal
            return cacheWrapper
        return cacheDecorator

    def authenticate(self):
        """
        First you need to register a service account into Cerberus system for your backend micro-service
        that needs access to keychain for personal data pseudonymisation. If you have multiple services
        that need access to keychain, it is recommended to register multiple accounts for keychain access.

        This method should be called before any other APIs.
        :return: None
        :exception RestRequestException
        """
        self.restCurd.authenticate()

    def getCategories(self):
        url = self.__buildGetCategoriesUrl()
        try:
            return self.restCurd.get(url=url)
        except RestRequestException as ex:
            print("getCategoryPages failed. ", str(ex))
            raise RestRequestException(
                "get category pages failed. " + str(ex))


    @cacheDecorateGetKey()
    def getUserConsentKeys(self, userId):
        """
        get the user consent keys.
        :param userId: user id
        :return: ConsentKeyResponse
        """
        keyUrl = self.__buildGetConsentKeyUrl()
        headers = {'Content-Type': 'application/x-protobuf'}

        consentKeyRequest = keychain_pb2.ConsentKeyRequest()
        consentKeyRequest.user_id = userId
        consentKeyRequest.service_key = self.serviceKey.encode("utf-8")
        requestBytes = consentKeyRequest.SerializeToString()
        try:
            response = self.restCurd.post(url=keyUrl, headers=headers, data=requestBytes)
            consentKeys = keychain_pb2.ConsentKeyResponse()
            consentKeys.ParseFromString(response.content)
            return consentKeys
        except RestRequestException as ex:
            print("getConsentKey {} failed {}. ".format(userId, str(ex)))
            raise RestRequestException(
                "get user consent key failed. " + str(ex))

    def getConsentCategoryKey(self, userId, category):
        consentKey = self.getUserConsentKeys(userId)
        keys = consentKey.keys
        keySpec = None
        for k in keys:
            if k.key_category == category:
                keySpec = KeySpec(k.key_generation, k.key_category, k.key)
                break
        if not keySpec:
            print("Key not found for %s" % category)
            raise KeychainNotExistException("Key does not exist")
        return keySpec

    def getConsent(self, userId):
        """
        Get the user consents.
        :param userId: string. user id.
        :return: Json object contains all user consents. format is
        {
          "userId": "string",
          "consents": [
            {
              "categoryTitle": "location",
              "granted": true
            },
            {
              "categoryTitle": "image",
              "granted": false
            }
          ],
        }
        """
        consentUrl = self.__buildGetConsentUrl()
        headers = {self.CONSTANT_HEADER_USER_ID: userId}
        try:
            return self.restCurd.get(url=consentUrl, headers=headers)
        except RestRequestException as ex:
            print("getConsent {} failed {}. ".format(userId, str(ex)))
            raise RestRequestException(
                "get user consent failed. " + str(ex))


    def setConsents(self, consent):
        """
        Set user consent on specified categories. Multiple categories can be set at same time.
        :param consent: JSON object. The format is
        {
          "userId": "string",
          "consents": [
            {
              "categoryTitle": "location",
              "granted": true
            },
            {
              "categoryTitle": "image",
              "granted": false
            }
          ],
        }
        :return: None
        :exception: RestRequestException if request failed.
        """
        consentUrl = self.__buildConsentUrl()
        headers = {self.CONSTANT_HEADER_USER_ID: consent["userId"]}
        consentBody = {"consents": consent["consents"]}
        try:
            self.restCurd.post(url=consentUrl, headers=headers, json=consentBody)
            self.keyCache.delete(consent["userId"])
        except RestRequestException as ex:
            print("setConsents {} failed {}. ".format(consent["userId"], str(ex)))
            raise RestRequestException(
                    "set user consent failed. " + str(ex))

    def setConsent(self, userId, categoryTitle, granted):
        """
        Set user consent on specified category.
        :param userId: string. user id.
        :param categoryTitle: string. consent category
        :param granted: boolean. True to grant permission. False to revoke the permission
        :return: None
        :exception RestRequestException
        """
        consent = {}
        consent["userId"] = userId
        consent["consents"] = []
        consent["consents"].append({"categoryTitle": categoryTitle, "granted": granted})
        return self.setConsents(consent)

    def getRestrictions(self, userId):
        """
        Get the user's restriction of consents
        :param userId:
        :return: Json object contains all restricted consents of user. format is
        {
          "userId": "string",
          "restrictions": [
            {
              "categoryTitle": "location",
              "restricted": true
            },
            {
              "categoryTitle": "image",
              "restricted": false
            }
          ]
        }
        :exception: RestRequestException
        """
        url = self.__buildGetRestrictionUrl()
        headers = {self.CONSTANT_HEADER_USER_ID: userId}
        try:
            return self.restCurd.get(url=url, headers=headers)
        except RestRequestException as ex:
            print("get user {} retrication failed {}.".format(userId, str(ex)))
            raise RestRequestException(
                "get user restriction failed." + str(ex))

    def setRestrictions(self, restriction):
        """
        set the restriction of consent. Multiple categories can be restricted at same time
        :param restriction: Json object. The format is
        {
          "userId": "string",
          "restrictions": [
            {
              "categoryTitle": "location",
              "restricted": true
            },
            {
              "categoryTitle": "image",
              "restricted": false
            }
          ]
        }
        :return: None
        :exception: RestRequestException when request failed.
        """
        url = self.__buildRestrictionUrl()
        headers = {self.CONSTANT_HEADER_USER_ID: restriction["userId"]}
        restrictionBody = {"restrictions": restriction["restrictions"]}
        try:
            self.restCurd.post(url=url, headers=headers, json=restrictionBody)
            self.keyCache.delete(restriction["userId"])
        except RestRequestException as ex:
            print("set user {} restriction failed {}.".format(restriction["userId"], str(ex)))
            raise RestRequestException(
                    "set user restriction failed. " + str(ex))

    def setRestriction(self, userId, categoryTitle, restricted):
        """
        set the restriction of consent on specified category
        :param userId: string. user Id
        :param categoryTitle: string. consent category
        :param restricted: boolean. True to restrict the consent. false otherwish
        :return: None
        :exception RestRequestException
        """
        restriction = {}
        restriction["userId"] = userId
        restriction["restrictions"] = []
        restriction["restrictions"].append({"categoryTitle": categoryTitle, "restricted": restricted})
        return self.setRestrictions(restriction)

    def setDeletions(self, deletions):
        """
        set the deletion of user consent
        :param deletions: Json object. format is
        {
          "userId": "string",
          "deletionModel": [
            "location",
            "image"
          ]
        }
        :return: None
        """
        url = self.__buildDeletionUrl()
        headers = {self.CONSTANT_HEADER_USER_ID: deletions["userId"]}
        try:
            self.restCurd.delete(url=url, headers=headers, json=deletions["deletionModel"])
            self.keyCache.delete(deletions["userId"])
        except RestRequestException as ex:
            print("set user {} deletion failed {}.".format(deletions["userId"], str(ex)))
            raise RestRequestException(
                "set user deletion failed. " + str(ex))


    def createUser(self, userId):
        url = self.__buildCreateUserUrl()
        headers = {self.CONSTANT_HEADER_USER_ID: userId}
        try:
            self.restCurd.post(url=url, headers=headers)
        except RestRequestException as ex:
            print("create user {} failed {}. ".format(userId, str(ex)))
            raise RestRequestException(
                    "Create user" + userId + "failed. " + str(ex))

    def deleteUser(self, userId, trueDelete=False):
        url = self.__buildDeleteUserUrl(trueDelete)
        headers = {self.CONSTANT_HEADER_USER_ID: userId}
        try:
            self.restCurd.delete(url=url, headers=headers)
        except RestRequestException as ex:
            print("Delete user {} failed {}.".format(userId, str(ex)))
            raise RestRequestException(
                    "Delete user" + userId + "failed. " + str(ex))

    def encryptBytes(self, userId, category, plainTextBytes):
        """
        Encrypt byte arrays.
        :param userId: string. user id.
        :param category: string. consent category
        :param plainTextBytes: byte arrays need encryption
        :return: encrypted byte arrays
        """
        keySpec = self.getConsentCategoryKey(userId, category)
        return self.encryptor.encrypt(keySpec, plainTextBytes)

    def decryptToBytes(self, userId, category, encryptTextBytes):
        """
        Decrypt encryped byte arrays
        :param userId: string. user id
        :param category: string. consent category.
        :param encryptTextBytes: encrypted byte arrays need decryption.
        :return: plain byte arrays.
        """
        keySpec = self.getConsentCategoryKey(userId, category)
        return self.encryptor.decrypt(keySpec, encryptTextBytes)

    def encryptString(self, userId, category, plainString):
        """
        Encrypt plain string.
        :param userId: string. user if
        :param category: consent category
        :param plainString: plain string need encryption
        :return: encrypted byte arrays
        """
        keySpec = self.getConsentCategoryKey(userId, category)
        return self.encryptor.encrypt(keySpec, plainString.encode("utf-8"))

    def decryptToString(self, userId, category, encryptStringBytes):
        """
        Decrypt encrypted byte arrays to string
        :param userId: string. user id
        :param category: string. consent category
        :param encryptStringBytes: encrypted byte arrays
        :return: plain string
        """
        keySpec = self.getConsentCategoryKey(userId, category)
        plainStringBytes = self.encryptor.decrypt(keySpec, encryptStringBytes)
        return plainStringBytes.decode("utf-8")


    def encryptInt(self, userId, category, integer):
        """
        Encrypt integer number.
        :param userId: string. user id.
        :param category: string. consent category
        :param integer: input integer number
        :return: encrypted byte arrays.
        """
        keySpec = self.getConsentCategoryKey(userId, category)
        intBytes = struct.pack("<q", integer)
        return self.encryptor.encrypt(keySpec, intBytes)

    def decryptToInt(self, userId, category, encryptIntBytes):
        """
        decrypt encrypted byte arrays to integer number
        :param userId: string. user id
        :param category: string. consent category.
        :param encryptIntBytes: encrypted byte arrays
        :return: int number
        """
        keySpec = self.getConsentCategoryKey(userId, category)
        intBytes = self.encryptor.decrypt(keySpec, encryptIntBytes)
        return struct.unpack("<q", intBytes)[0]

    def encryptFloat(self, userId, category, floatValue):
        keySpec = self.getConsentCategoryKey(userId, category)
        floatBytes = struct.pack("<d", floatValue)
        return self.encryptor.encrypt(keySpec, floatBytes)

    def decryptToFloat(self, userId, category, encryptFloatBytes):
        keySpec = self.getConsentCategoryKey(userId, category)
        floatBytes = self.encryptor.decrypt(keySpec, encryptFloatBytes)
        return struct.unpack("<d", floatBytes)[0]

    def encrypteDateTime(self, userId, category, dateTime):
        """
        Encrypt datetime. Input data time must be UTC. precision is milliseconds.
        :param userId: user id
        :param category: consent category
        :param dateTime: datetime need encryption. must be UTC
        :return: byte array
        """
        dateTimeValueInt = int(dateTime.timestamp() * 1000)
        return self.encryptInt(userId, category, dateTimeValueInt)

    def decryptToDateTime(self, userId, category, encryptDateTimeBytes):
        """
        decrypt input bytes to datetime in UTC. precision is milliseconds.
        :param userId: user id
        :param category: consent category
        :param encryptDateTimeBytes:
        :return: UTC datetime
        """
        dateTimeValueInt = self.decryptToInt(userId, category, encryptDateTimeBytes)
        return datetime.utcfromtimestamp(dateTimeValueInt / 1000)

    def encryptBytesFromService(self, userId, category, plainTextBytes):
        """
        Encrypt byte arrays by calling backend keychain service
        :param userId: string. user id
        :param category: string. consent category
        :param plainTextBytes: byte arrays need encryption
        :return: encrypted byte arrays
        """
        encryptUrl = self.__buildCryptoEncryptUrl()
        headers = {'Content-Type': 'application/x-protobuf'}
        requestMessage = keychain_pb2.CryptoRequest()
        requestMessage.user_id = userId
        requestMessage.service_key = self.serviceKey.encode("utf-8")
        requestMessage.consent_category = category
        requestMessage.data = plainTextBytes
        messageBytes = requestMessage.SerializeToString()
        try:
            response = self.restCurd.post(url=encryptUrl, headers=headers, data=messageBytes)
            responseMessage = keychain_pb2.CryptoResponse()
            responseMessage.ParseFromString(response.content)
            return responseMessage.data
        except RestRequestException as ex:
            print("encryptBytesFromService failed.", str(ex))
            raise RestRequestException(
                "encryptBytesFromService failed. " + str(ex))

    def decryptBytesFromService(self, userId, category, encryptedTextBytes):
        """
        Decrypt encrypted byte arrays by calling backend keychain service
        :param userId: string. user id
        :param category: string. consent category
        :param encryptedTextBytes:  encrypted byte arrays need decryption
        :return: plain byte arrays
        """
        encryptUrl = self.__buildCryptoDecryptUrl()
        headers = {'Content-Type': 'application/x-protobuf'}
        requestMessage = keychain_pb2.CryptoRequest()
        requestMessage.user_id = userId
        requestMessage.service_key = self.serviceKey.encode("utf-8")
        requestMessage.consent_category = category
        requestMessage.data = encryptedTextBytes
        messageBytes = requestMessage.SerializeToString()
        try:
            response = self.restCurd.post(url=encryptUrl, headers=headers, data=messageBytes)
            responseMessage = keychain_pb2.CryptoResponse()
            responseMessage.ParseFromString(response.content)
            return responseMessage.data
        except RestRequestException as ex:
            print("decryptBytesFromService failed.", str(ex))
            raise RestRequestException(
                "decryptBytesFromService failed. " + str(ex))

    def encryptStringFromService(self, userId, category, plainString):
        """
        Encrypt plain string by calling backend keychain service
        :param userId: string. user id
        :param category: string. consent category
        :param plainString:
        :return: encrypted byte arrays.
        """
        return self.encryptBytesFromService(userId, category, plainString.encode("utf-8"))

    def decryptStringFromService(self, userId, category, encryptStringByte):
        """
        decrypt encrypted byte arrays to string by calling backend keychain service
        :param userId: string. user id
        :param category: string. consent category
        :param encryptStringByte: encrypted byte arrays
        :return: plain string.
        """
        return self.decryptBytesFromService(userId, category, encryptStringByte).decode("utf-8")

    def encryptIntFromService(self, userId, category, integer):
        intBytes = struct.pack("<q", integer)
        return self.encryptBytesFromService(userId, category, intBytes)

    def decryptIntFromService(self, userId, category, encryptedIntBytes):
        intBytes = self.decryptBytesFromService(userId, category, encryptedIntBytes)
        return struct.unpack("<q", intBytes)[0]

    def encryptFloatFromService(self, userId, category, floatValue):
        floatBytes = struct.pack("<d", floatValue)
        return self.encryptBytesFromService(userId, category, floatBytes)

    def decryptFloatFromService(self, userId, category, encryptedFloatBytes):
        floatBytes = self.decryptBytesFromService(userId, category, encryptedFloatBytes)
        return struct.unpack("<d", floatBytes)[0]

    def encryptDateTimeFromService(self, userId, category, dateTime):
        dateTimeValueInt = int(dateTime.timestamp() * 1000)
        return self.encryptIntFromService(userId, category, dateTimeValueInt)

    def decryptDateTimeFromService(self, userId, category, encryptedDateTimeBytes):
        dateTimeValueInt = self.decryptIntFromService(userId, category, encryptedDateTimeBytes)
        return datetime.utcfromtimestamp(dateTimeValueInt / 1000)

    def __buildAuthenticateUrl(self):

        url = "http://" + self.cerberusHost + ":" + str(self.cerberusPort) + self.AUTHENTICATION_ENDPOINT
        return url


    def __buildGetConsentUrl(self):
        return self.__buildConsentUrl()

    def __buildGetRestrictionUrl(self):
        return self.__buildRestrictionUrl()

    def __buildConsentUrl(self):
        return "http://" + self.keychainHost + ":" + str(self.keychainPort) + \
              self.CONSENT_ENTRY

    def __buildRestrictionUrl(self):
        return "http://" + self.keychainHost + ":" + str(self.keychainPort) + \
            self.RESTRICTIONS_ENTRY

    def __buildDeletionUrl(self):
        return "http://" + self.keychainHost + ":" + str(self.keychainPort) + \
            self.DELETIONS_ENTRY

    def __buildGetConsentKeyUrl(self):
        url = "http://" + self.keychainHost + ":" + str(self.keychainPort) + \
              self.CONSENT_KEY_ENTRY + self.CONSENT_KEY_ENDPOINT
        return url

    def __buildGetCategoriesUrl(self):
        url = "http://" + self.keychainHost + ":" + str(self.keychainPort) + self.CONSENT_CATEGORY_ENTRY
        return url

    def __buildCryptoEncryptUrl(self):
        return "http://" + self.keychainHost + ":" + str(self.keychainPort) + \
            self.CRYPTO_ENTRY + self.CRYPTO_ENCRYPT_ENDPOINT

    def __buildCryptoDecryptUrl(self):
        return "http://" + self.keychainHost + ":" + str(self.keychainPort) + \
            self.CRYPTO_ENTRY + self.CRYPTO_DECRYPT_ENDPOINT

    def __buildCreateUserUrl(self):
        return "http://" + self.keychainHost + ":" + str(self.keychainPort) + \
            self.USER_ENTRY + self.USER_CREATE_ENDPOINT

    def __buildDeleteUserUrl(self, trueDelete):
        url = "http://" + self.keychainHost + ":" + str(self.keychainPort) + \
            self.USER_ENTRY
        if trueDelete:
            url += self.USER_HARD_DELETE_ENDPOINT
        else:
            url += self.USER_SOFT_DELETE_ENDPOINT
        return url
