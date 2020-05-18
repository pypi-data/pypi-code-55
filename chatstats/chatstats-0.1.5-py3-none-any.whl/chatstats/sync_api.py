import logging
import uuid

from requests import Session, Request, Response
from requests.exceptions import RequestException

logger = logging.getLogger(__name__)


class SyncChatStats:
    __slots__ = ('url', 'version', 'session', 'token')

    ALLOWED_REQUEST_TYPES = ('POST', 'GET')
    URL = 'https://api.chat-stats.ru'
    ACTUAL_VERSION = 'v1'
    VERSIONS = ('v1',)

    def __init__(self, token: str, url: str = None, version: str = None):
        self.token = token
        self.url = url or self.URL
        self.session = Session()
        self.version = version or self.ACTUAL_VERSION
        if self.version not in self.VERSIONS:
            raise KeyError(
                'version doesn\'t exists. Versions: %s' % list(self.VERSIONS)
            )

    def __make_request(self,
                       request_type: str,
                       url: str,
                       payload: dict = None,
                       params: dict = None
                       ) -> Response:
        if request_type.upper() not in self.ALLOWED_REQUEST_TYPES:
            raise KeyError(
                'unsupported request type. Types: %s' % list(self.ALLOWED_REQUEST_TYPES)
            )

        request_params = {
            'url': url,
            'json': payload,
            'params': params,
            'method': request_type.upper()
        }
        rid = str(uuid.uuid4())
        request_params.update({
            'headers': {
                'X-REQUEST-ID': rid
            }
        })

        req = Request(**request_params)
        prepared_request = self.session.prepare_request(req)

        response = Response()
        try:
            response = self.session.send(
                prepared_request,
                timeout=5
            )
            logger.debug(
                'Sent request to %s. Response code: %s' %
                (prepared_request.url, response.status_code)
            )
        except RequestException as e:
            logger.exception(e, extra={
                'request_id': rid,
                'url': prepared_request.url
            })
            response.status_code = 500
        return response

    def new_event(self,
                  event_name: str,
                  user_id: int,
                  user_first_name: str = None,
                  is_bot: bool = None,
                  user_language_code: str = None,
                  user_last_name: str = None,
                  user_username: str = None
                  ) -> Response:
        """
    Args:
        event_name (:obj:`str`): Name of an event
        user_id (:obj:`int`): Id of a user
        user_first_name (:obj:`str`, optional): First name of a user. Used in sex stats.
        user_last_name (:obj:`bytes`, optional): Last name of a user. Used in sex stats.
        user_language_code (:obj:`str`, optional): Language code of a user.
        user_username (:obj:`str`, optional): Username of a user. Used in common stats
        is_bot (:obj:`bool`, optional): Is user a bot
    """
        return self.__make_request(
            request_type='POST',
            url='/'.join([self.url, self.version, 'event']),
            params={
                'token': self.token
            },
            payload={
                'name': event_name,
                'user': {
                    'id': user_id,
                    'first_name': user_first_name,
                    'is_bot': is_bot,
                    'language_code': user_language_code,
                    'last_name': user_last_name,
                    'username': user_username,
                }
            }
        )
