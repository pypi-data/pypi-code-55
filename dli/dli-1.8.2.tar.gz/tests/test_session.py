import json
import os
import time
from urllib.parse import urlencode

import keyring
from keyring.errors import NoKeyringError
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
import pytest
import unittest
import jwt
from unittest.mock import MagicMock, patch
import httpretty

from dli import __version__, __product__
from dli.client.dli_client import Session, DliClient
from dli.client.environments import _Environment
from dli.client.listener import _Listener
from dli.client.session import start_session
from dli.client import session
from dli.client.exceptions import (
    DatalakeException,
    InsufficientPrivilegesException,
    UnAuthorisedAccessException
)
from dli.siren import PatchedSirenBuilder

environ = MagicMock(catalogue='http://catalogue.local',
                    accounts='')
valid_token = jwt.encode({"exp": 9999999999}, 'secret')
expired_token = jwt.encode({"exp": 1111111111}, 'secret')


class SessionTestCase(unittest.TestCase):

    def test_can_decode_valid_jwt_token(self):
        ctx = Session(
            None,
            "key",
            environ,
            None,
            valid_token
        )

        self.assertFalse(ctx.has_expired)

    def test_can_detect_token_is_expired(self):
        ctx = Session(
            None,
            "key",
            environ,
            None,
            expired_token
        )
        self.assertTrue(ctx.has_expired)


class SessionRequestFactoryTestCase(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def session(self):
        self.session = Session(None, None, environ, None, valid_token)

    @httpretty.activate
    def test_response_403_raises_InsufficientPrivilegesException(self):
        response_text = 'Insufficient Privileges'
        httpretty.register_uri(
            httpretty.GET, 'http://catalogue.local/test',
            status=403, body=response_text
        )

        with self.assertRaises(InsufficientPrivilegesException):
            self.session.get('/test')

    @httpretty.activate
    def test_response_401_raises_UnAuthorisedAccessException(self):
        response_text = 'UnAuthorised Access'
        httpretty.register_uri(
            httpretty.GET, 'http://catalogue.local/test',
            status=401, body=response_text
        )


        with self.assertRaises(UnAuthorisedAccessException):
            self.session.get('/test')

    @httpretty.activate
    def test_response_500_raises_DatalakeException(self):
        response_text = 'Datalake server error'
        httpretty.register_uri(
            httpretty.GET, 'http://catalogue.local/test',
            status=500, body=response_text
        )

        with self.assertRaises(DatalakeException):
            self.session.get('/test')

    @httpretty.activate
    def test_sdk_version_is_included_in_header(self):
        httpretty.register_uri(
            httpretty.GET, 'http://catalogue.local/__api/',
            status=200, body="response"
        )
        # issue a request
        self.session.get('/__api/')

        request = httpretty.last_request()
        self.assertTrue("X-Data-Lake-SDK-Version" in request.headers)
        self.assertEqual(request.headers["X-Data-Lake-SDK-Version"], str(__version__))


class TestEnv:

    def __init__(self):
        self.sam = "http://sam.local"
        self.catalogue = "http://catalogue.local"
        self.accounts = "http://catalogue.local"
        self.consumption = "http://consumption.local"
        self.sam_client = "CLIENT_ID"


class TestSessionMock(Session):

    def __init__(self, id, pasw):
        self._get_SAM_auth_key = MagicMock()
        self._get_auth_key = MagicMock()
        self._get_decoded_token = MagicMock()
        self._get_expiration_date = MagicMock()
        self._set_mount_adapters = MagicMock()
        super().__init__(id, pasw, TestEnv(), "Test")


class TestClientMock(DliClient):

    def __init__(self, api_root, host=None, debug=None, strict=True,
                 access_id=None, secret_key=None, use_keyring=True):
        super().__init__("Test", access_id=access_id, secret_key=secret_key, use_keyring=use_keyring)

    def _new_session(self):
        return TestSessionMock("Test", "Test")


class TestSessionMockWithAuth(Session):

    def __init__(self, id, pasw):
        self._set_mount_adapters = MagicMock()
        self.access_id = id
        self.secret_key = pasw
        self.auth_key = None
        self._environment = TestEnv()
        self.host = None
        self.use_keyring = True
        self.siren_builder = PatchedSirenBuilder()


class TestClientMockWithAuth(TestClientMock):

    def _new_session(self):
        return TestSessionMockWithAuth(self.access_id, self.secret_key)


class TestSessionMockNoPrompt(Session):

    # required to prevent the web popup that we want to
    # launch ourselves / use selenium
    def __init__(self, id, pasw, env):
        super().__init__(id, pasw, env, "Test", auth_prompt=False)


class TestClientMockNoPrompt(DliClient):

    def _new_session(self):
        return TestSessionMockNoPrompt(None, None, self._environment)


@pytest.fixture
def clear_keyring(monkeypatch):
    monkeypatch.setattr(keyring, 'get_password', lambda _, app: None)
    monkeypatch.setattr(keyring, 'set_password', lambda _, app, val: None)

@pytest.fixture
def mock_session(clear_keyring):
    yield TestSessionMock

@pytest.fixture
def mock_del_env_user(monkeypatch):
    monkeypatch.delenv("DLI_ACCESS_KEY_ID", raising=False)
    monkeypatch.delenv("DLI_SECRET_ACCESS_KEY", raising=False)

@pytest.fixture
def real_client(request):
    # This is the S3 address used for the QA environment.
    api_root = os.environ[f'{request.param[0]}_API_URL']
    accessid = os.environ[f'{request.param[0]}_ACCESS_ID']
    secretkey = os.environ[f'{request.param[0]}_SECRET_ACCESS_KEY']
    client = None

    if request.param[1] == "Credentials":
        client = DliClient(
            api_root=api_root,
            access_id=accessid,
            secret_key=secretkey
        )
    elif request.param == 'API':
        pass
    else:
        pass

    yield client


@pytest.fixture
def mock_create_env_user(monkeypatch):
    monkeypatch.setenv("DLI_ACCESS_KEY_ID", "TestingUser")
    monkeypatch.setenv("DLI_SECRET_ACCESS_KEY", "TestingPass")


def test_credentials_no_api_key(monkeypatch, mock_create_env_user, recwarn):
    # test flow when u/p set and no api key set
    monkeypatch.setattr(DliClient, '_new_session', lambda x: x)
    dl = start_session()
    assert(issubclass(type(dl), DliClient))
    assert(dl.secret_key is not None and dl.access_id is not None)


def test_credentials_session(mock_create_env_user, mock_session):
    # test flow when u/p set and no api key set

    sesh = mock_session(os.environ["DLI_ACCESS_KEY_ID"],
                        os.environ["DLI_SECRET_ACCESS_KEY"])
    assert sesh._get_SAM_auth_key.call_count == 1


def test_api_key_deprecation_warning(recwarn, monkeypatch):
    # test flow when u/p set and api key set
    # api key should override
    monkeypatch.setattr(DliClient, '_new_session', MagicMock())
    dl = start_session(api_key="Test")
    assert(issubclass(type(dl), DliClient))
    assert "`api_key` will be deprecated in the future" \
           in ",".join([str(x.message) for x in recwarn.list])
    assert(dl.secret_key is not None and dl.access_id is None)


def test_credentials_and_api_key(mock_create_env_user, monkeypatch):
    # test flow when u/p set and api key set
    # api key should override
    monkeypatch.setattr(DliClient, '_new_session',  MagicMock())
    dl = start_session(api_key="Test")
    assert (dl.secret_key is not None and dl.access_id is None)


def test_api_session(mock_create_env_user, mock_session):
    # test flow when u/p set and no api key set
    # (there will be no acces id set)
    sesh = mock_session(None, "Test")
    assert sesh._get_auth_key.call_count == 1


def test_credentials_and_no_api_key(mock_create_env_user, monkeypatch, caplog):
    # test flow when no credentials and api key set
    monkeypatch.setattr(session, "get_client", lambda: TestClientMock)
    dl = start_session()
    for x in caplog.records:
        assert("old" not in x.message)


def test_no_credentials_and_api_key(mock_del_env_user, monkeypatch, caplog):
    # test flow when no credentials and api key set
    monkeypatch.setattr(session, "get_client", lambda: TestClientMock)
    dl = start_session(api_key="Test")
    assert (dl.secret_key is not None and dl.access_id is None)
    for x in caplog.records:
        assert("new" not in x.message)


def test_api_key_auth(mock_del_env_user, monkeypatch):
    # test old auth process (_get_auth_key())
    api_response = valid_token
    monkeypatch.setattr(session, "get_client", lambda: TestClientMockWithAuth)
    dl = start_session(api_key="API")
    dl._session.post = MagicMock()
    dl._session.post.return_value.text = api_response

    dl._session._auth_init()
    assert(dl and dl._session.auth_key is not None)


def test_credentials_auth(mock_create_env_user, monkeypatch):
    # test new auth process (_get_SAM_auth_key())
    sam_response = {
        "access_token": valid_token,
        "token_type": "Bearer", "expires_in": 3599}
    catalogue_response = {
        "access_token": valid_token,
        "token_type": "Bearer", "expires_in": 3599}

    monkeypatch.setattr(session, "get_client", lambda: TestClientMockWithAuth)
    dl = start_session()
    dl._session.post = MagicMock()
    dl._session.post.return_value.json.side_effect = [
        sam_response, catalogue_response
    ]

    dl._session._auth_init()
    assert(dl and dl._session.auth_key is not None)



def real_drive(port, postbox, env):
    chrome_options = Options()
    # chrome_options.add_argument("--headless")

    user = "dl_manual_test_2@ihsmarkit.com"
    pw = "-0o_p}i-Uz%*PQy_"

    driver = webdriver.Chrome(executable_path='./chromedriver',
                              options=chrome_options)
    driver.get(f"{_Listener.LOCALHOST}:{port}/login?postbox={postbox}&{urlencode(env.__dict__)}")

    WebDriverWait(driver, 120).until(
        ec.visibility_of_element_located((By.ID, "emailAddress"))
    ).send_keys(user)

    driver.find_element(By.ID, "continueButton").click()

    WebDriverWait(driver, 10).until(
        ec.visibility_of_element_located((By.ID, "i0116"))
    ).send_keys(user)

    driver.find_element(By.ID, "idSIButton9").click()

    WebDriverWait(driver, 10).until(
        ec.visibility_of_element_located((By.ID, "passwordInput"))
    ).send_keys(pw)

    driver.find_element(By.ID, "submitButton").click()

    driver.find_element(By.ID, "idSIButton9").click()
    # need to add some time, else the client quits before we
    # complete localhost activity.
    time.sleep(2)
    driver.quit()


def real_drive_off_cliff(port):
    #takes down the Listener

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    user = "dl_manual_test_2@ihsmarkit.com"
    pw = "-0o_p}i-Uz%*PQy_"
    driver = webdriver.Chrome(executable_path='./chromedriver',
                              chrome_options=chrome_options)
    driver.get(f"{_Listener.LOCALHOST}:{port}/shutdown")
    driver.quit()


def real_login_attempt(sesh):
    postbox = _Listener.run(port=8080)
    real_drive(8080, postbox, sesh._environment)
    time.sleep(5)
    assert _Listener.VALUES.get(postbox) is not None
    return postbox


def test_reload_JWT_keyring(monkeypatch):
    monkeypatch.setattr(keyring, 'get_password', lambda _, app: valid_token.decode())

    dl = TestClientMockWithAuth(api_root="Test")
    dl._session._get_web_auth_key = MagicMock()
    dl._session._auth_init()
    assert dl._session._get_web_auth_key.call_count == 0


def test_no_reload_delete_expired_JWT_keyring(monkeypatch):

    dl = TestClientMockWithAuth(api_root="Test")
    # we definitely set it in the first place
    keyring.set_password(
        __product__, dl._session._environment.catalogue, valid_token.decode())
    # later 'expires'
    orig = keyring.get_password
    monkeypatch.setattr(keyring, 'get_password', lambda _, app: expired_token.decode())

    dl._session._get_web_auth_key = MagicMock()
    dl._session._get_web_auth_key.return_value = valid_token
    dl._session._auth_init()
    assert dl._session._get_web_auth_key.call_count == 1
    assert(orig(__product__, dl._session._environment.catalogue) is None)


@pytest.mark.skipif(True or os.environ.get('CI_PYPI_USER') is not None,
                    reason="Not runnable on gitlab - 8080 closed")
def test_set_JWT_keyring_web_auth_key(monkeypatch):
    orig = keyring.get_password
    monkeypatch.setattr(keyring, 'get_password', lambda _, app: None)
    dl = TestClientMockWithAuth(api_root="Test")

    def catch(port, postbox):
        _Listener.VALUES[postbox] = valid_token.decode("utf-8")

    dl._session._get_web_auth_key(callback=catch)
    assert(orig(__product__, dl._session._environment.catalogue)
           == valid_token.decode())


@pytest.mark.skipif(True or os.environ.get('CI_PYPI_USER') is not None,
                    reason="Not runnable on gitlab - 8080 closed")
@pytest.mark.integration
def test_web_session(mock_del_env_user):

    sesh = Session(
        "test", "test", _Environment("https://catalogue-dev.udpmarkit.net"),
        "Test", auth_prompt=False, auth_key=None)

    real_login_attempt(sesh)
    time.sleep(1)

    assert(len(_Listener.VALUES) == len(set(_Listener.VALUES.VALUES())))


@pytest.mark.skipif(True or os.environ.get('CI_PYPI_USER') is not None,
                    reason="Not runnable on gitlab - 8080 closed")
@pytest.mark.integration
def test_web_flow(clear_keyring, mock_del_env_user, monkeypatch):

    monkeypatch.setattr(session, "get_client", lambda: TestClientMockNoPrompt)
    dl = start_session(root_url="https://catalogue-dev.udpmarkit.net")

    # this is what get_web_auth_key is otherwise doing,
    # but we need to unblock to allow selenium to operate.
    # so we register a custom default callback to call selenium
    # rather than the web browser
    def cb(port, postbox):
        real_drive(port, postbox, dl._environment)

    with patch.object(Session._get_web_auth_key, '__defaults__', (cb,)):
        dl._session._auth_init()

    assert dl._session.auth_key is not None

@pytest.mark.skipif(True or os.environ.get('CI_PYPI_USER') is not None,
                    reason="Not runnable on gitlab - 8080 closed")
@pytest.mark.integration
@pytest.mark.parametrize('real_client', [('QA', "Credentials")],
                         indirect=['real_client'])
def test_credentials_on_catalogue(clear_keyring, real_client):
    # test that new auth actually works and returns JWT

    assert(real_client.datasets._get(
        "autotestdatasetItsdeclarationRomanZimmermannandpeople"
    ) is not None)

@pytest.mark.skipif(True or os.environ.get('CI_PYPI_USER') is not None,
                    reason="Not runnable on gitlab - 8080 closed")
@pytest.mark.integration
@pytest.mark.parametrize('real_client', [('QA', "Credentials")],
                         indirect=['real_client'])
def test_webflow_on_catalogue(monkeypatch, real_client):

    monkeypatch.setattr(session, "get_client", lambda: TestClientMockNoPrompt)
    dl = start_session(root_url="https://catalogue-dev.udpmarkit.net")

    # this is what get_web_auth_key is otherwise doing,
    # but we need to unblock to allow selenium to operate.
    # so we register a custom default callback to call selenium
    # rather than the web browser
    def cb(port, postbox):
        real_drive(port, postbox, dl._environment)

    with patch.object(Session._get_web_auth_key, '__defaults__', (cb,)):
        dl._session._auth_init()

    # todo - doesnt work with these u/p sam logins
    assert dl.datasets._get("Sheep") is not None

def test_no_system_keyring_installed(monkeypatch):
    keyring.core.set_keyring(keyring.core.fail.Keyring())
    monkeypatch.setattr("dli.client.dli_client.Session._reload_or_web_flow.__defaults__", (True,))
    with pytest.raises(NoKeyringError):
        dl = start_session(root_url="https://catalogue-dev.udpmarkit.net")

def test_no_system_keyring_ack(monkeypatch, capsys):
    def t(pb):
        _Listener.VALUES[pb] =  valid_token.decode("utf-8")
    keyring.core.set_keyring(keyring.core.fail.Keyring())
    monkeypatch.setattr("dli.client.dli_client.Session._get_web_auth_key.__defaults__", ( (lambda port, pb: t(pb)), ))
    dl = start_session(root_url="https://catalogue-dev.udpmarkit.net")
    captured = capsys.readouterr()
    assert "no keyring manager available" in captured.out