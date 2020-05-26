
import requests
from google.oauth2.service_account import Credentials
import google.oauth2.credentials
import google.auth.iam
from google.auth.transport.requests import Request




def gcf_authenticated_request(gcf_url, method='GET', credentials=None, IAM_SCOPE=None, **kwargs):
    """Makes authenticated request to google cloud functions
    code is copy-pasted and modified code from here:
    https://cloud.google.com/iap/docs/authentication-howto#authenticating_from_a_service_account

    Arguments:
        gcf_url {str} -- target google cloud function url e.g. https://us-central1-custom-ground-236517.cloudfunctions.net/hello_protected

    Keyword Arguments:
        method {str} -- request method e.g POST, GET (default: {'GET'})
        credentials {google.oauth2.service_account.Credentails } -- service account that has function.invoker permission on target url (default: {None})
        IAM_SCOPE {list} -- list of google iam scope (default: ['https://www.googleapis.com/auth/iam'])
        **kwargs -- arguemnts for requests.request method

    Returns:
        requests.response -- response object

    Example:
    gcf_url = 'https://us-central1-custom-ground-236517.cloudfunctions.net/hello_protected'
    resp = gcf_authenticated_request(gcf_url) # GET request

    # put request with **kwargs
    gcf_url = 'https://us-central1-custom-ground-236517.cloudfunctions.net/hello_protected'
    body ={"message":"this is a protected function, safe from crona virus "}
    headers = {'Content-Type':'application/json'}
    resp = gcf_authenticated_request(gcf_url,method='POST',headers=headers, data=json.dumps(body))
    """


    token_url = f'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=\\'
    metadata_server_token_url = 'http://metadata/computeMetadata/v1/instance/service-accounts/default/identity?audience='
    OAUTH_TOKEN_URI = 'https://www.googleapis.com/oauth2/v4/token'

    def get_google_open_id_connect_token(service_account_credentials):
        """Get an OpenID Connect token issued by Google for the service account.

        This function:

          1. Generates a JWT signed with the service account's private key
             containing a special "target_audience" claim.

          2. Sends it to the OAUTH_TOKEN_URI endpoint. Because the JWT in #1
             has a target_audience claim, that endpoint will respond with
             an OpenID Connect token for the service account -- in other words,
             a JWT signed by *Google*. The aud claim in this JWT will be
             set to the value from the target_audience claim in #1.

        For more information, see
        https://developers.google.com/identity/protocols/OAuth2ServiceAccount .
        The HTTP/REST example on that page describes the JWT structure and
        demonstrates how to call the token endpoint. (The example on that page
        shows how to get an OAuth2 access token; this code is using a
        modified version of it to get an OpenID Connect token.)
        """

        service_account_jwt = (
            service_account_credentials._make_authorization_grant_assertion())
        request = google.auth.transport.requests.Request()
        body = {
            'assertion': service_account_jwt,
            'grant_type': google.oauth2._client._JWT_GRANT_TYPE,
        }
        token_response = google.oauth2._client._token_endpoint_request(
            request, OAUTH_TOKEN_URI, body)
        return token_response['id_token']

    token_request_url = metadata_server_token_url + gcf_url
    token_request_headers = {'Metadata-Flavor': 'Google'}

    if not IAM_SCOPE:
        IAM_SCOPE = ['https://www.googleapis.com/auth/iam']

    if credentials:
        bootstrap_credentials = credentials
        bootstrap_credentials.has_scopes = IAM_SCOPE
    else:
        bootstrap_credentials, _ = google.auth.default(
            scopes=IAM_SCOPE)

    bootstrap_credentials.refresh(Request())
    signer = bootstrap_credentials.signer
    signer_email = bootstrap_credentials.service_account_email

    service_account_credentials = Credentials(
        signer, signer_email, token_uri=OAUTH_TOKEN_URI, additional_claims={
            'target_audience': gcf_url
        })
    headers = {}
    if 'headers' in kwargs.keys():
        for key in list(kwargs.keys()):
            if key == 'headers':
                headers = kwargs[key]
                del kwargs[key]

    google_open_id_connect_token = get_google_open_id_connect_token(
        service_account_credentials)

    headers['Authorization'] = f'Bearer {google_open_id_connect_token}'
    try:
        response = requests.request(method, gcf_url, headers=headers, **kwargs)
        return response
    except requests.exceptions.ReadTimeout:
        return print(f"triggered next gcf {gcf_url} but didn't wait for response")
    except:
        if response.status_code == 403:
            raise Exception(f'Service account {signer_email} does not have permission to '
                            'access the IAP-protected application.')
        elif response.status_code != 200:
            raise Exception(
                f'Bad response from application at {response.url}: {response.status_code} / {response.headers} / {response.text}')
        else:
            return response