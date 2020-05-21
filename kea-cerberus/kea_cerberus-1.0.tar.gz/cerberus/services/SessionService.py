from flask import Flask
import uuid

from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from cerberus.model.KsmUserModel import KsmUserModel
from cerberus.model.KsmSessionModel import KsmSessionModel
from cerberus.dtos.AuthenticationType import AuthenticationType
from cerberus.mappers.SessionMapper import SessionMapper
from cerberus.exceptions.exceptions import InvalidUserSessionException, InvalidUserCredentialsException, NotFoundUserException
from cerberus.services.SecurityHashService import SecurityHashService
from cerberus.services.FirebaseService import FirebaseService
from cerberus.services.AbstractService import AbstractService

class SessionService(AbstractService):

    def __init__(self, url):
        super(ConnectionService, self).__init__(url)

    def createSessionByLocalAuth(self, connection, username, password):

        if username is None:
            raise InvalidUserCredentialsException()

        if password is None:
            raise InvalidUserCredentialsException()

        kuat = KsmUserModel(self.urlEngine).getUserAuthenticationType(username, AuthenticationType.LOCAL)
        if kuat is None:
            raise NotFoundUserException()


        if not check_password_hash(kuat.getToken(), kuat.getUserId() + password):
            raise InvalidUserCredentialsException()

        return SessionService.createSession(connection, kuat)

    def createSessionByGoogleAuth(self, connection, uid, tokenId):

        if uid is None:
            raise InvalidUserCredentialsException()

        if tokenId is None:
            raise InvalidUserCredentialsException()

        decoded_token = FirebaseService().getDecoded_token(tokenId)

        res_uid = decoded_token['uid']
        if res_uid != uid:
            raise InvalidUserCredentialsException()

        kuat = KsmUserModel(self.urlEngine).getUserAuthenticationType(uid, AuthenticationType.GOOGLE)
        if kuat is None:
            user_email = decoded_token['email']
            kuat = KsmUserModel.getUserAuthenticationTypeByUsername(user_email)
            if kuat is None:
                raise InvalidUserCredentialsException()
            else:
                createdAt = datetime.now()
                ksmUserAuthenticationType = KsmUserModel.addUserAuthenticationType(AuthenticationType.GOOGLE, kuat.getUserId(), uid, uid, createdAt, createdAt)
                return SessionService.createSession(connection, ksmUserAuthenticationType)

        return SessionService.createSession(connection, kuat)


    #def createSessionByFacebookAuth(self, connection, token):

    def createSessionByTokenAuth(self, connection, username, token):

        if username is None:
            raise InvalidUserCredentialsException()

        if token is None:
            raise InvalidUserCredentialsException()

        kuat = KsmUserModel(self.urlEngine).getUserAuthenticationType(username, AuthenticationType.TOKEN)

        if kuat is None:
            raise NotFoundUserException()

        SecurityHashService.validateHash(token)

        if not check_password_hash(kuat.getToken(), token):
            raise InvalidUserCredentialsException()

        return SessionService.createSession(connection, kuat)

    def createSession(self, connection, kuat):

        if kuat is None:
            return

        date = datetime.now()
        ksmSession = KsmSessionModel(self.urlEngine).add(str(uuid.uuid4()), True, connection.getToken(), kuat.getUserId(), kuat.getAuthenticationTypeId(), date, date)
        return SessionMapper.mapToSession(ksmSession, connection)

    def getValidSession(self, token):

        if token is None:
            raise NullClientSessionException()

        ksmSession = KsmSessionModel(self.urlEngine).get(token)
        if ksmSession is None:
            raise InvalidUserSessionException()

        if ksmSession.getActive() == False:
            raise ClientSessionExpiredException()

        date = datetime.now()
        ksmSession.setUpdatedAt(date)
        KsmSessionModel(self.urlEngine).update(ksmSession)

        return SessionMapper.mapToSession(ksmSession, None)


    def getConnectionIdBySession(self, token):

        if token is None:
            raise NullClientSessionException()

        ksmSession = KsmSessionModel(self.urlEngine).get(token)
        if ksmSession is None:
            raise InvalidUserSessionException()

        return ksmSession.getConnectionId()
