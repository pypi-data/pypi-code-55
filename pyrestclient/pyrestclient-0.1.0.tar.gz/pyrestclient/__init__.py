import json
import re
from http import HTTPStatus
from urllib.parse import urljoin, urlencode

import requests
from urllib3 import disable_warnings, exceptions

from .logger import logger

disable_warnings(exceptions.InsecureRequestWarning)


def json_data(data):
    return json.dumps(data)


def get_header_default(user_agent='ide', content_type='application/json-patch+json', accept='application/json'):
    return {
        'User-Agent': user_agent,
        'Content-Type': content_type,
        'Accept': accept,
        # 'UserAgentInternal': 'webfrontend/1.0'
    }


class RESTClient:
    """ Main class for RestAPI """

    def __init__(self,
                 protocol: str = '',
                 host: str = '',
                 port: int = 0,
                 username: str = None,
                 password: str = None,
                 header: dict = None,
                 auth_basic: bool = False,
                 auth_uri: str = '',
                 auth_payload: dict = None,
                 logger_enabled: bool = False):

        # Enable/disable logger
        logger.disabled = not logger_enabled

        # Credentials and settings for api url
        self.username = username
        self.password = password
        self.protocol = protocol  # HTTP or HTTPS
        self.host = host
        self.port = port
        self.auth_uri = auth_uri
        self.auth_payload = auth_payload
        self.auth_basic = auth_basic

        # Default header
        self.header = header or get_header_default()

        # Create auth header
        if self.auth_payload:
            try:
                self.token = AuthToken(self).token
                self.header['Authorization'] = self.token
            except KeyError as err:
                logger.error(f'Cannot get token. {err}')

        # Set basic Authorization if enabled
        elif self.auth_basic:
            self.auth_basic = (self.username, self.password)
            self.header = {}

    def __str__(self):

        return f'Username: {self.username}\n' \
               f'Password: {self.password}\n' \
               f'Base URL: {self.base_url}\n'

    @property
    def base_url(self):
        """Create tested URL"""

        return f'{self.protocol}://{self.host}:{self.port}' if self.port else f'{self.protocol}://{self.host}'

    def _requested_url(self, url):
        """ Return full URL if link specified contains 'http' """

        if 'http' in url:
            return url
        elif self._validate_url(self.base_url):
            return urljoin(self.base_url, url)
        raise SyntaxError(f'URL does not specified. Used: "{url}" only. Specify full URL or use constructor')

    @staticmethod
    def _validate_url(url):
        return re.match(r'http[s]?://[\w/.]+', url)

    def send_request(self,
                     method: str,
                     url: str,
                     query_params=None,
                     data=None,
                     files=None,
                     verify=False,
                     custom_header=None,
                     cookies=None,
                     request_timeout=None):

        """
        Send common request

        To upload file use:

        with open(files, 'rb') as f:
             files = {'licenseFile': (License.name, f)}

        :param cookies:
        :param method: GET, POST, DELETE
        :param url: unified identificator, self.url (BASE) + url
        :param query_params: = Query parameters in the url
        :param data: json data
        :param files: "files: {'licenseFile': (License.name, f)}"
        :param verify: Bool
        :param custom_header: Use specified header
        :param request_timeout: Time in sec.
        :return: requests.request('POST', url=url, headers=HEADER, files=files, verify=False)

        """

        # Make full url to use in request
        link = self._requested_url(url)

        # Add params to requested link
        if query_params:
            link += '?' + urlencode(query_params)

        method = method.upper()

        assert method in ['GET', 'HEAD', 'DELETE', 'POST', 'PUT', 'PATCH', 'OPTIONS'], \
            'Specified methods is not compatible.'

        if data and files:
            logger.error('Data parameter cannot be used with files parameter simultaneously.')
            raise ValueError('Data parameter cannot be used with files parameter simultaneously.')

        # Extend header
        if 'Content-Type' not in self.header:
            self.header['Content-Type'] = 'application/json'

        response = 'Invalid requests. Check parameters'

        try:
            # For 'POST', 'PUT', 'PATCH', 'OPTIONS', 'DELETE'
            if method in ['POST', 'PUT', 'PATCH', 'OPTIONS', 'DELETE']:
                if data and not files:

                    response = requests.request(method=method,
                                                url=link,
                                                auth=self.auth_basic,
                                                headers=self.header,
                                                json=data,
                                                cookies=cookies,
                                                verify=verify,
                                                timeout=request_timeout)

                    logger.info(f'{method} ' + link)
                    logger.info('PAYLOAD:\n' + json.dumps(data, indent=4))

                elif files:
                    files_header = self.header.copy()
                    del files_header['Content-Type']
                    if custom_header:
                        files_header = custom_header

                    response = requests.request(method=method,
                                                url=link,
                                                auth=self.auth_basic,
                                                headers=files_header,
                                                cookies=cookies,
                                                files=files,
                                                verify=verify,
                                                timeout=request_timeout)

                    logger.info(f'{method} ' + link)
                    logger.info('PAYLOAD:\n' + json.dumps(data, indent=4))

                elif not files and not data:
                    response = requests.request(method=method,
                                                url=link,
                                                auth=self.auth_basic,
                                                headers=self.header,
                                                cookies=cookies,
                                                verify=verify,
                                                timeout=request_timeout)

                    logger.info(f'{method} ' + link)
                    logger.info('PAYLOAD:\n' + json.dumps(data, indent=4))

            # For 'GET', 'HEAD' request
            else:

                # For usual 'GET' without query params
                header = self.header
                if custom_header:
                    header = custom_header

                logger.info(f'{method} ' + link)
                response = requests.request(method=method,
                                            url=link,
                                            auth=self.auth_basic,
                                            cookies=cookies,
                                            headers=header,
                                            verify=verify,
                                            timeout=request_timeout)

        except BaseException as err:
            logger.error(err)
            raise err

        return response

    @property
    def is_service_available(self):
        """Check base url availability within 30 sec."""

        try:
            response = requests.get(self.base_url, timeout=10, verify=False)
            if response.status_code == 200:
                return True
        except requests.exceptions.Timeout:
            return False
        except requests.exceptions.ConnectionError:
            return False

    def download(self, url, dst):
        """Download file.

        :param url: Full url to file
        :param dst: path to store
        :return:
        """

        response = self.send_request('GET', url)
        try:
            if response.ok:
                with open(dst, 'wb') as f:
                    f.write(response.content)
                    return True
            else:
                return False
        except (ConnectionError, ConnectionRefusedError) as err:
            logger.error(f'Download failed. {err}')
            return err

    # noinspection PyPep8Naming
    def GET(self,
            url='',
            query_params=None,
            extend_header=False,
            cookies=None,
            request_timeout=None):

        return self.send_request('GET',
                                 url=url,
                                 query_params=query_params,
                                 cookies=cookies,
                                 request_timeout=request_timeout)

    # noinspection PyPep8Naming
    def POST(self,
             url='',
             query_params=None,
             data=None,
             file=None,
             extend_header=False,
             cookies=None,
             request_timeout=None):

        return self.send_request('POST',
                                 url=url,
                                 query_params=query_params,
                                 data=data,
                                 files=file,
                                 cookies=cookies,
                                 request_timeout=request_timeout)

    # noinspection PyPep8Naming
    def PUT(self,
            url='',
            extend_header=False,
            custom_header=None,
            data='',
            files='',
            request_timeout=None,
            verify=False):

        header = self.header.copy()

        if files:
            del header['Content-Type']

        if custom_header:
            header = custom_header
        elif extend_header:
            header = extend_header

        return requests.request(method='PUT',
                                url=url,
                                auth=self.auth_basic,
                                headers=header,
                                data=data,
                                files=files,
                                verify=verify,
                                timeout=request_timeout)

    def DELETE(self,
               url='',
               data='',
               query_params=None,
               extend_header=False,
               cookies=None,
               request_timeout=None):

        return self.send_request('DELETE',
                                 url=url,
                                 query_params=query_params,
                                 data=data,
                                 cookies=cookies,
                                 request_timeout=request_timeout)


class AuthToken:
    """Class to get auth token"""

    def __init__(self, client: RESTClient):
        self.client = client

    @property
    def auth_url(self):
        """Get full authorization URL"""
        return urljoin(self.client.base_url, self.client.auth_uri)

    @property
    def token(self):
        if self.client.is_service_available:
            try:
                response = requests.post(self.auth_url, json=self.client.auth_payload, verify=False, timeout=7)
                return response.json()['token']
            except json.decoder.JSONDecodeError as err:
                logger.error(err)
                return 'Cannot get token property: {}'.format(err)
            except TypeError as err:
                logger.error(err)
                return 'Endpoint is available but "token" key cannot be retrieved.\n' \
                       'Check credentials.\n{}'.format(err)
        else:
            return f'Host {self.client.host} is unreachable. Check service status'


class RESTAssertion:
    """Parse requests response to get status code."""

    @staticmethod
    def should_be_success_response_code(response):
        """200 <= status_code < 400"""
        assert response.ok, 'Response code is not success.'

    @staticmethod
    def should_be_ok_response_code(response):
        """OK, 200. Request fulfilled, document follows"""
        assert response.status_code == HTTPStatus.OK, 'Response code is not 200.'

    @staticmethod
    def should_be_not_found_response_code(response):
        """Nothing matches the given URI"""
        assert response.status_code == HTTPStatus.NOT_FOUND, 'Response code is not 404.'

    @staticmethod
    def should_be_bad_request(response):
        """Bad request syntax or unsupported method"""
        assert response.status_code == HTTPStatus.BAD_REQUEST, 'Response code is not 400.'
