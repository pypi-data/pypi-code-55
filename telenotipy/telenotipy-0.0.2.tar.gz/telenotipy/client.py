from requests import get, post, delete
from requests.compat import quote_plus

DEFAULT_API_URL = 'https://telenoti.vinrobot.net/api/v1'

class TelegramNotificationClient:
    """
    This object is a helper to access and use the Telegram Notification service.

    :param str token: The application token to access the API.
    :param str api_url: The API base URL. (Default to 'https://telenoti.vinrobot.net/api/v1')
    :param bool raise_for_status: Whether or not to raise an Exception if the HTTP response
                                  code is between 400 and 600. (Default to True)
    """

    def __init__(self,
                 token,
                 api_url=DEFAULT_API_URL,
                 raise_for_status=True):
        self.api_url = api_url or DEFAULT_API_URL
        self.raise_for_status = raise_for_status
        self.headers = {
            'Authorization': 'Token {}'.format(token),
        }

    def _parse_response(self, response):
        """Parse a response and return the JSON data.

        :param response: The subscription ID/Token.
        :return: The JSON response.
        :rtype: object
        :raises HTTPError: if the HTTP code is between 400 and 600
                           and self.raise_for_status is True.
        :raises ValueError: if the server response is not a valid json.
        """
        if self.raise_for_status:
            response.raise_for_status()
        return response.json()

    def send_notification(self, to, message, title=None):
        """Send a notification to a list of recipients as the current application.

        Send an API request to send a Telegram message to the
        list of recipients.

        :param str[] to: The list of recipients.

        :return: The list of recipients to whom the message was sent
                 and the list of those to whom it was not sent.
        :rtype: object
        :raises HTTPError: if the HTTP code is between 400 and 600
                           and self.raise_for_status is True.
        :raises ValueError: if the server response is not a valid json.
        """

        to = [str(user) for user in to]
        title = str(title or '')
        message = str(message)

        url = '{}/notification/send'.format(self.api_url)
        form_data = {'to': to, 'title': title, 'message': message}
        response = post(url, data=form_data, headers=self.headers)
        return self._parse_response(response)

    def broadcast_notification(self, message, title=None):
        """Send a notification to all the subscribers of the application.

        Send an API request to send a Telegram message to all the
        registered users.

        :return: The list of recipients to whom the message was sent
                 and the list of those to whom it was not sent.
        :rtype: object
        :raises HTTPError: if the HTTP code is between 400 and 600
                           and self.raise_for_status is True.
        :raises ValueError: if the server response is not a valid json.
        """

        return self.send_notification(['*'], message, title)

    def create_subscription(self):
        """Create a subsription owned by the API Token application.

        Send an API request to create a new subscription for
        the current application API token.

        :return: The new subscription information.
        :rtype: object
        :raises HTTPError: if the HTTP code is between 400 and 600
                           and self.raise_for_status is True.
        :raises ValueError: if the server response is not a valid json.
        """

        url = '{}/subscriptions/'.format(self.api_url)
        response = post(url, headers=self.headers)
        return self._parse_response(response)

    def list_subscriptions(self, page=1):
        """List the subsriptions owned by the API Token application.

        Send an API request to list the subscriptions owned by
        the current application API token.

        :param int page: The page in the list. (Default to 1)
        :return: The list of subscriptions.
        :rtype: object
        :raises HTTPError: if the HTTP code is between 400 and 600
                           and self.raise_for_status is True.
        :raises ValueError: if the server response is not a valid json.
        """

        page = int(page)

        url = '{}/subscriptions/?page={}'.format(self.api_url, page)
        response = get(url, headers=self.headers)
        return self._parse_response(response)

    def get_subscription(self, token):
        """Retrieve a subsription owned by the API Token application.

        Send an API request to retrieve the information of a subscription
        owned by the current application API token and described by it's token.

        :param str token: The subscription ID/Token.
        :return: The subscription information.
        :rtype: object
        :raises HTTPError: if the HTTP code is between 400 and 600
                           and self.raise_for_status is True.
        :raises ValueError: if the server response is not a valid json.
        """

        url = '{}/subscriptions/{}'.format(self.api_url, quote_plus(token))
        response = get(url, headers=self.headers)
        return self._parse_response(response)

    def delete_subscription(self, token):
        """Delete a subsription owned by the API Token application.

        Send an API request to delete a subscription owned by
        the current application API token and described by it's token.

        :param str token: The subscription ID/Token.
        :return: The deleted subscription information.
        :rtype: object
        :raises HTTPError: if the HTTP code is between 400 and 600
                           and self.raise_for_status is True.
        :raises ValueError: if the server response is not a valid json.
        """

        url = '{}/subscriptions/{}'.format(self.api_url, quote_plus(token))
        response = delete(url, headers=self.headers)
        return self._parse_response(response)
