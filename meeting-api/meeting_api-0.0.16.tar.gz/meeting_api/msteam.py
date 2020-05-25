import requests


class AccessToken:

    def __init__(
            self, code, redirect_uri=None, client_id=None, client_secret=None):
        self.data = {}
        self.data['grant_type'] = 'authorization_code'
        self.data['scope'] = 'user.readwrite'
        self.data['code'] = code
        self.data['redirect_uri'] = redirect_uri
        self.data['client_id'] = client_id
        self.data['client_secret'] = client_secret
        self.url = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'

    def update(self):
        request = requests.post(url=self.url, data=self.data)

        data = request.json()
        if 'error' in data.keys():
            self.token = None
            self.error = data['error_description']
        else:
            self.token = data['access_token']


class User:
    def __init__(self, username, userid, password=None):
        self.username = username
        self.password = password
        self.userid = userid


class Team:
    def __init__(self, code, client_id, client_secret, redirect_uri):
        self.code = code
        self.redirect_uri = redirect_uri
        self.client_id = client_id
        self.client_secret = client_secret

    def update_access_token(self):
        self.access_token = AccessToken(
            self.code, self.redirect_uri, self.client_id, self.client_secret)
        self.access_token.update()

        if not self.access_token.token:
            raise Exception(self.access_token.error)

    def check(self):
        if not hasattr(self, 'access_token'):
            self.update_access_token()

    def create_user(
            self, displayName, mailNickname, userPrincipalName,
            password, **kwargs):
        self.check()

        data = {
            'accountEnabled': True,
            'displayName': displayName,
            'mailNickname': mailNickname,
            'userPrincipalName': userPrincipalName,
            'passwordProfile': {
                'forceChangePasswordNextSignIn': True,
                'password': password}}

        headers = {
            'Authorization': 'Bearer {}'.format(self.access_token.token),
            'content-type': 'application/json'}

        response = requests.post(
            'https://graph.microsoft.com/v1.0/users', json=data,
            headers=headers)
        return_values = response.json()
        if 'error' in return_values.keys():
            self.error = return_values['error']['message']
            return False
        else:
            self.user = User(
                userPrincipalName, userid=return_values['id'],
                password=password)
            return True

    def update_user(self, username, userid, password=None):
        self.user = User(username=username, userid=userid)
        if password is not None:
            self.user.password = password

    def create_meeting(self, start_time, end_time, subject):
        self.check()

        headers = {
            'Authorization': 'Bearer {}'.format(self.access_token.token),
            'content-type': 'application/json'}

        data = {
            'startDateTime': start_time,
            'endDateTime': end_time,
            'subject': subject}
        if hasattr(self, 'user'):
            data.update({
                'participants': {'organizer': {'identity': {'user': {
                    'id': self.user.userid}}}}})

        response = requests.post(
            url='https://graph.microsoft.com/v1.0/me/onlineMeetings',
            headers=headers, json=data)
        return_values = response.json()

        if 'error' in return_values.keys():
            self.error = return_values['error']['message']
            return False
        else:
            self.meeting_url = return_values['joinUrl']
            return True
