import servicemock as sm


class ServiceBackend:
    url = 'http://myservice.com'


class CreateUser(sm.Request):
    default_expected_request_body = sm.JSONRequestBody({
        'username': 'smithy',
        'first_name': 'John',
        'last_name': 'Smith'
    })

    def __init__(self):
        # TODO: update body
        super().__init__('POST', '/v1/users', body=self.default_expected_request_body)


class UserCreated(sm.Response):
    default_response = {
        'id': 'deadbeef',
        'username': 'smithy',
        'first_name': 'John',
        'last_name': 'Smith'
    }

    def __init__(self):
        # TODO: Rename JSON to JSONResponseBody
        super().__init__('201 Created', body=sm.JSON(self.default_response))
