

import uuid
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash

from cerberus.mappers.UserMapper import UserMapper
from cerberus.model.KsmUserModel import KsmUserModel
from cerberus.exceptions.exceptions import UserAlreadyExistException, NotFoundRoleException, InternalErrorException, NotFoundUserException
from cerberus.dtos.AuthenticationType import AuthenticationType
from cerberus.dtos.SecurityHash import SecurityHash
from cerberus.services.SecurityHashService import SecurityHashService
from cerberus.services.FirebaseService import FirebaseService
from cerberus.services.AbstractService import AbstractService

class UserService(AbstractService):

    def __init__(self, url):
        super(ConnectionService, self).__init__(url)

    def createUser(self, username, token, authenticationTypeId, roleId):
        ksmUser = None
        kuat = KsmUserModel(self.urlEngine).getUserAuthenticationType(username, authenticationTypeId)

        if not kuat is None:
            raise UserAlreadyExistException()

        kuat = KsmUserModel(self.urlEngine).getUserAuthenticationTypeByUsername(username)
        if not kuat is None:
            ksmUser =  KsmUserModel(self.urlEngine).getUserById(kuat.getUserId())

        ksmRole = KsmUserModel(self.urlEngine).getRoleById(roleId)
        if ksmRole is None:
            raise NotFoundRoleException()

        if authenticationTypeId == AuthenticationType.GOOGLE:
            decoded_token = FirebaseService().getDecoded_token(token)

            res_uid = decoded_token['uid']
            if res_uid != username:
                print("Error:")
                print(res_uid)
                print(username)
                raise InvalidUserCredentialsException()

        try:
            createdAt = datetime.now()

            #Create Ksm User
            if ksmUser is None:
                ksmUser = KsmUserModel(self.urlEngine).addUser(str(uuid.uuid4()), createdAt, createdAt)

            #Create Ksm User Authentication Type
            UserService.createKsmUserAuthenticationType(ksmUser.getId(), username, token, authenticationTypeId)
            if authenticationTypeId == AuthenticationType.GOOGLE:
                email = decoded_token['email']
                UserService.createKsmUserAuthenticationType(ksmUser.getId(), email, token, AuthenticationType.TOKEN)

            #Add Role to User
            ksmRoleUser = KsmUserModel(self.urlEngine).addUser(ksmUser.getId(), roleId, createdAt, createdAt)

        except Exception as ex:
            print(ex)
            raise InternalErrorException("Error creating user")

        return UserMapper.mapToUser(ksmUser)

    def createKsmUserAuthenticationType(self, userId, username, token, authenticationTypeId):
        createdAt = datetime.now()
        if authenticationTypeId == AuthenticationType.LOCAL:
            token = generate_password_hash(userId + token)

        ksmUserAuthenticationType = KsmUserModel(self.urlEngine).addUserAuthenticationType(authenticationTypeId, userId, username, token, createdAt, createdAt)
        return ksmUserAuthenticationType

    def createUserAccessToken(self, email):
        ksmUserAuthenticationType = KsmUserModel(self.urlEngine).getUserAuthenticationTypeByUsername(email)
        if ksmUserAuthenticationType is None:
            raise NotFoundUserException()

        ksmUser =  KsmUserModel(self.urlEngine).getUserById(ksmUserAuthenticationType.getUserId())
        securityHash = SecurityHashService.createHash(SecurityHash.AUTH_TOKEN)

        createdAt = datetime.now()
        ksmUserAuthenticationType = KsmUserModel(self.urlEngine).getUserAuthenticationTypeByUserId(ksmUserAuthenticationType.getUserId(), AuthenticationType.TOKEN)
        if ksmUserAuthenticationType is None:
            token = generate_password_hash(securityHash.getToken())
            ksmUserAuthenticationType = KsmUserModel(self.urlEngine).addUserAuthenticationType(AuthenticationType.TOKEN, ksmUser.getId(), username, token, createdAt, createdAt)
        else:
            ksmUserAuthenticationType.setToken(generate_password_hash(securityHash.getToken()))
            ksmUserAuthenticationType.setUpdatedAt(createdAt)
            KsmUserModel(self.urlEngine).update(ksmUserAuthenticationType)

        return securityHash
