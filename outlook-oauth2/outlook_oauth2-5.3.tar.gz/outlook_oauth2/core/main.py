from outlook_oauth2.core.mailbox import Mailbox

__all__ = ['OutlookAccount']


class OutlookAccount(Mailbox):
    """Sets up access to Outlook account for all methods & classes.

    Attributes:
        access_token: A string OAuth token from Outlook allowing access to a user's account
    """

    def __init__(self, access_token):
        Mailbox.__init__(self, self, 'me')
        self.access_token = access_token

    def get_mailbox(self, email_address):
        """Provides access to another inbox attached to this account"""
        return Mailbox(self, email_address)
