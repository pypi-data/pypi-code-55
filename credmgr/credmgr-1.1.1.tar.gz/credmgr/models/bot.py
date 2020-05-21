from .utils import camelToSnake, resolveUser
from ..mixins import BaseApp


class Bot(BaseApp):
    _attrTypes = {
        **BaseApp._attrTypes, 'reddit_app': 'RedditApp', 'sentry_token': 'SentryToken', 'database_credential': 'DatabaseCredential'
    }
    _editableAttrs = BaseApp._editableAttrs + ['redditAppId', 'sentryTokenId', 'databaseCredentialId']
    _path = '/bots'
    _credmgrCallable = 'bot'
    _canFetchByName = True

    def __init__(self, credmgr, **kwargs):
        '''Initialize a Bot instance

        Bots are used for grouping apps into a single request

        :param credmgr: An instance of :class:`~.CredentialManager`.
        :param id: ID of this Bot.
        :param name: Name of this Bot.
        :param ownerId: ID of the `~.User` that owns this Bot.
        :param redditApp: `~.RedditApp` that will be used with this Bot.
        :param sentryToken: `~.SentryToken` that will be used with this Bot.
        :param databaseCredential: `~.DatabaseCredential` that will be used with this Bot.
        '''
        super().__init__(credmgr, **kwargs)

    @staticmethod
    @resolveUser()
    def _create(_credmgr, name, redditApp, sentryToken, databaseCredential, owner=None):
        '''Create a new Bot

        Bots are used for grouping apps into a single request

        :param str name: Name of the Bot (required)
        :param Union[RedditApp,int] redditApp: Reddit App the bot will use
        :param Union[SentryToken,int] sentryToken: Sentry Token the bot will use
        :param Union[DatabaseCredential,int] databaseCredential: Database Credentials the bot will use
        :param Union[User,int,str] owner: Owner of the bot. Requires Admin to create for other users.
        :return: Bot
        '''

        from . import DatabaseCredential, RedditApp, SentryToken
        additionalParams = {}
        if isinstance(redditApp, RedditApp):
            redditApp = redditApp.id
        if redditApp:
            additionalParams['reddit_app_id'] = redditApp
        if isinstance(sentryToken, SentryToken):
            sentryToken = sentryToken.id
        if sentryToken:
            additionalParams['sentry_token_id'] = sentryToken
        if isinstance(databaseCredential, DatabaseCredential):
            databaseCredential = databaseCredential.id
        if databaseCredential:
            additionalParams['database_credential_id'] = databaseCredential
        if owner:
            additionalParams['owner_id'] = owner
        return _credmgr.post('/bots', data={'app_name': name, **additionalParams})

    def edit(self, **kwargs):
        for key, value in kwargs.items():
            if key in ['redditApp', 'sentryToken', 'databaseCredential']:
                newKey = f'{key}Id'
                kwargs[newKey] = kwargs.pop(key)
        super(Bot, self).edit(**kwargs)