import configparser
import os
from requests import Session

from . import models
from .auth import ApiTokenAuth
from .config import Config
from .exceptions import InitializationError
from .models.utils import CachedProperty
from .requestor import Requestor, urljoin
from .serializer import Serializer


User = models.User
Bot = models.Bot
RedditApp = models.RedditApp
RefreshToken = models.RefreshToken
UserVerification = models.UserVerification
SentryToken = models.SentryToken
DatabaseCredential = models.DatabaseCredential

class CredentialManager(object):
    '''The CredentialManager class provides convenient access to CredentialManager's API.

    Instances of this class are the gateway to interacting with CredentialManager's API
    through CredentialManager. The canonical way to obtain an instance of this class is via:


    .. code-block:: python

        import CredentialManager
        credentialManager = CredentialManager.client(apiToken='LIqbGjAeep3Ws5DH3LOEQPmw8UZ6ek')


    '''
    _default = None
    _endpoint = '/api/v1'

    def __init__(self, configName=None, sessionClass=None, sessionKwargs=None, **kwargs):
        '''Initialize a CredentialManager instance.

        :param str configName: The name of a section in your ``.credmgr.ini`` file that credmgr will load its configuration
            is loaded from. If ``configName`` is ``None``, then it will look for it in the environment variable ``credmgr_configName``.
            If it is not found there, the ``default`` section is used.
        :param Session sessionClass: A Session class that will be used to create a requestor. If not set, use ``requests.Session`` (default: None).
        :param dict sessionKwargs: Dictionary with additional keyword arguments used to initialize the session (default: None).

        Additional keyword arguments will be used to initialize the
        :class:`.Config` object. This can be used to specify configuration
        settings during instantiation of the :class:`.CredentialManager` instance. For
        more details please see :ref:`configuration`.

        Required settings are:

        - apiToken
        OR
        - username
        - password

        .. warning::
             Using an API Token instead of a username/password is strongly recommended!

        The ``sessionClass`` and ``sessionKwargs`` allow for
        customization of the session :class:`.CredentialManager` will use. This allows,
        e.g., easily adding behavior to the requestor or wrapping its
        |Session|_ in a caching layer. Example usage:

        .. |Session| replace:: ``Session``
        .. _Session: https://2.python-requests.org/en/master/api/#requests.Session

        .. code-block:: python

           import json, betamax, requests

           class JSONDebugRequestor(Requestor):
               def request(self, *args, **kwargs):
                   response = super().request(*args, **kwargs)
                   print(json.dumps(response.json(), indent=4))
                   return response

           mySession = betamax.Betamax(requests.Session())
           credentialManager = CredentialManager(..., sessionClass=JSONDebugRequestor, sessionKwargs={'session': mySession})
        '''
        if sessionKwargs is None:
            sessionKwargs = {}
        configSection = None
        try:
            configSection = configName or os.getenv('credmgr_configName') or 'DEFAULT'
            self.config = Config(configSection, **kwargs)
        except configparser.NoSectionError as exc:
            if configSection is not None:
                exc.message += "\nYou provided the name of a .credmgr.ini section that doesn't exist."
            raise

        self._server = urljoin(getattr(self.config, 'server'), getattr(self.config, 'endpoint'))
        apiToken = getattr(self.config, 'apiToken')
        username = getattr(self.config, 'username')
        password = getattr(self.config, 'password')

        initErrorMessage = "Required settings are missing. Either 'apiToken' OR 'username' and 'password' must be specified, These settings can be provided in a .credmgr.ini file, as a keyword argument during the initialization of the `CredentialManager` class, or as an environment variable."
        if all([apiToken, username, password]):
            raise InitializationError(initErrorMessage)
        if apiToken:
            self._auth = ApiTokenAuth(apiToken)
        elif username and password:
            self._auth = (username, password)
        else:
            raise InitializationError('API Token or an username/password pair must be set.')

        self._requestor = Requestor(self._server, self._auth, sessionClass, **sessionKwargs)
        self.serializer = Serializer(self)
        self._currentUser = None
        self._userDefaults = None
        self.getUserDefault = lambda key, default: self.userDefaults.get(key, default)
        self.user = models.UserHelper(self)
        '''An instance of :class:`.UserHelper`.

        Provides the interface for interacting with :class:`.User`.
        For example to get a ``user`` with ``id`` of ``1`` do:
        
        .. code-block:: python
            user = credmgr.user(1)
            print(user.id)
        
        To create a ``user`` do:
        
        ..code-block:: python
            user = credmgr.user.create(**userKwargs)
        
        See :meth:`~.UserHelper.create` for the required params.
        '''
        self.bot = models.BotHelper(self)
        '''An instance of :class:`.BotHelper`.

        Provides the interface for interacting with :class:`.Bot`.
        For example to get a ``bot`` with ``id`` of ``1`` do:
        
        .. code-block:: python
            bot = credmgr.bot(1)
            print(bot.id)
        
        To create a ``bot`` do:
        
        ..code-block:: python
            bot = credmgr.bot.create(**botKwargs)
        
        See :meth:`~.BotHelper.create` for the required params.
        '''

        self.redditApp = models.RedditAppHelper(self)
        '''An instance of :class:`.CredentialManagerAppHelper`.

        Provides the interface for interacting with :class:`.CredentialManagerApp`.
        For example to get a ``redditApp`` with ``id`` of ``1`` do:
        
        .. code-block:: python
            redditApp = credmgr.redditApp(1)
            print(redditApp.id)
        
        To create a ``redditApp`` do:
        
        ..code-block:: python
            redditApp = credmgr.redditApp.create(**redditAppKwargs)
        
        See :meth:`~.RedditAppHelper.create` for the required params.
        '''

        self.refreshToken = models.RefreshTokenHelper(self)
        '''An instance of :class:`.RefreshTokenHelper`.

        Provides the interface for interacting with :class:`.RefreshToken`.
        For example to get a ``refreshToken`` with ``id`` of ``1`` do:
        
        .. code-block:: python
            refreshToken = credmgr.refreshToken(1)
            print(refreshToken.id)
        
        .. note::
            Refresh tokens cannot be manually created.
        '''

        self.userVerification = models.UserVerificationHelper(self)
        '''An instance of :class:`.UserVerificationHelper`.

        Provides the interface for interacting with :class:`.UserVerification`.
        For example to get a ``userVerification`` with ``id`` of ``1`` do:
        
        .. code-block:: python
            userVerification = credmgr.userVerification(1)
            print(userVerification.id)
        
        To create a ``userVerification`` do:
        
        ..code-block:: python
            userVerification = credmgr.userVerification.create(**userVerificationKwargs)
        
        See :meth:`~.UserVerificationHelper.create` for the required params.
        '''

        self.sentryToken = models.SentryTokenHelper(self)
        '''An instance of :class:`.SentryTokenHelper`.

        Provides the interface for interacting with :class:`.SentryToken`.
        For example to get a ``sentryToken`` with ``id`` of ``1`` do:
        
        .. code-block:: python
            sentryToken = credmgr.sentryToken(1)
            print(sentryToken.id)
        
        To create a ``sentryToken`` do:
        
        ..code-block:: python
            sentryToken = credmgr.sentryToken.create(**sentryTokenKwargs)
        
        See :meth:`~.SentryTokenHelper.create` for the required params.
        '''

        self.databaseCredential = models.DatabaseCredentialHelper(self)
        '''An instance of :class:`.DatabaseCredentialHelper`.

        Provides the interface for interacting with :class:`.DatabaseCredential`.
        For example to get a ``databaseCredential`` with ``id`` of ``1`` do:
        
        .. code-block:: python
            databaseCredential = credmgr.databaseCredential(1)
            print(databaseCredential.id)
        
        To create a ``databaseCredential`` do:
        
        ..code-block:: python
            databaseCredential = credmgr.databaseCredential.create(**databaseCredentialKwargs)
        
        See :meth:`~.DatabaseCredentialHelper.create` for the required params.
        '''

    def users(self, batchSize=10, limit=None):
        return User(self).listItems(batchSize=batchSize, limit=limit)

    def bots(self, batchSize=20, limit=None, owner=None):
        return Bot(self).listItems(batchSize=batchSize, limit=limit, owner=owner)

    def redditApps(self, batchSize=20, limit=None, owner=None):
        return RedditApp(self).listItems(batchSize=batchSize, limit=limit, owner=owner)

    def refreshTokens(self, batchSize=20, limit=None, owner=None):
        return RefreshToken(self).listItems(batchSize=batchSize, limit=limit, owner=owner)

    def userVerifications(self, batchSize=20, limit=None, owner=None):
        return UserVerification(self).listItems(batchSize=batchSize, limit=limit, owner=owner)

    def sentryTokens(self, batchSize=20, limit=None, owner=None):
        return SentryToken(self).listItems(batchSize=batchSize, limit=limit, owner=owner)

    def databaseCredentials(self, batchSize=20, limit=None, owner=None):
        return DatabaseCredential(self).listItems(batchSize=batchSize, limit=limit, owner=owner)

    @CachedProperty
    def currentUser(self) -> User:
        if not self._currentUser:
            self._currentUser = self.get('/users/me')
        return self._currentUser

    @CachedProperty
    def userDefaults(self):
        if not self._userDefaults:
            self._userDefaults = self.currentUser.defaultSettings
        return self._userDefaults

    def get(self, path, params=None):
        return self.serializer.deserialize(self._requestor.request(path, 'GET', params=params))

    def post(self, path, data):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        return self.serializer.deserialize(self._requestor.request(path, 'POST', data=data, headers=headers))

    def patch(self, path, data):
        return self.serializer.deserialize(self._requestor.request(path, 'PATCH', json=data))

    def delete(self, path):
        return self._requestor.request(path, 'DELETE')