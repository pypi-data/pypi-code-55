from uuid import uuid4

from flask.sessions import SessionMixin, SessionInterface
from werkzeug.datastructures import CallbackDict

from flask_session_azure.storage_account import StorageAccount


class StorageAccountSession(CallbackDict, SessionMixin):
    def __init__(self, sid: str, initial=None):
        def on_update(self):
            self.modified = True

        CallbackDict.__init__(self, initial, on_update)

        self.sid = sid
        self.modified = False


class StorageAccountSessionInterface(SessionInterface):
    """
    Replacement session interface for flask that uses Azure-Storage account tables as storage backend
    Data is encrypted and tagged for manipulation using AES encryption
    """
    session_class = StorageAccountSession

    def __init__(self, connection_str: str, table_name="flasksession", partition_key="default_session",
                 create_table_if_not_exists: bool = True):
        """
        :param connection_str: the connection string to the azure table storage (or cosmos db)
        :param table_name: the table name. Default is "flasksession". When overwriting this, follow the table name rules
        https://docs.microsoft.com/en-us/rest/api/storageservices/Understanding-the-Table-Service-Data-Model#table-names
        :param partition_key: the partition key within the table. Use a unique partition_key if applications share a table
        """
        self.storage = StorageAccount(connection_str, table_name, partition_key, create_table_if_not_exists)

    @staticmethod
    def get_encryption_key_from_app_secret(app):
        """
        Checks if the app secret_key is set, and if it is long enough to use it as AES encryption key.
        Returns the key truncated to a length of multiples of 8, to use it as AES encryption key
        """
        if app.secret_key is None:
            raise RuntimeError(
                "The session is unavailable because no secret key was set. "
                "Set the secret_key on the application to something unique and secret.")
        if len(app.secret_key) < 16:
            raise RuntimeError(
                "The session is unavailable because the secret is too short. "
                f"The secret must be 16 characters or longer, but is only {len(app.secret_key)} character(s).")

        # only use multiples of 8 from the secret_key tu use it as AES encryption_key
        characters = len(app.secret_key)
        characters = characters - characters % 8
        return app.secret_key[:characters]

    def open_session(self, app, request):
        """
        Reads the session data from table storage, decrypts the data and returns the session object
        """
        sid = request.cookies.get(app.session_cookie_name)
        if not sid:
            sid = str(uuid4())
            return self.session_class(sid=sid)
        encryption_key = self.get_encryption_key_from_app_secret(app)
        data = self.storage.read(sid, encryption_key)
        if data is not None:
            return self.session_class(sid=sid, initial=data)
        return self.session_class(sid=sid)

    def save_session(self, app, session, response):
        """
        Serializes the data to JSON, encrypts the data using AES
        and stores the encrypted data along with a verification tag to azure storage.
        Only stores the UUID of the table entry inside the session_cookie
        """

        domain = self.get_cookie_domain(app)
        path = self.get_cookie_path(app)
        if not session:
            if session.modified:
                self.storage.delete(session.sid)
            response.delete_cookie(app.session_cookie_name, domain=domain, path=path)
            return

        if session.modified:
            encryption_key = self.get_encryption_key_from_app_secret(app)
            self.storage.write(session.sid, dict(session), encryption_key)

        httponly = self.get_cookie_httponly(app)
        secure = self.get_cookie_secure(app)
        expires = self.get_expiration_time(app, session)
        response.set_cookie(app.session_cookie_name, session.sid, expires=expires, httponly=httponly, domain=domain,
                            path=path, secure=secure)
