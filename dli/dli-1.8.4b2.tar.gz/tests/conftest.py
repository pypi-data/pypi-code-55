import pytest
import keyring

class TestKeyring(keyring.backend.KeyringBackend):
    """A test keyring which always outputs same password
    """
    priority = 1
    servicedict = {}

    def set_password(self, servicename, username, password):
        TestKeyring.servicedict[servicename+username] = password

    def get_password(self, servicename, username):
        return TestKeyring.servicedict.get(servicename+username)

    def delete_password(self, servicename, username):
        try:
            del TestKeyring.servicedict[servicename+username]
        finally:
            pass

# set the keyring for keyring lib
keyring.set_keyring(TestKeyring())


def pytest_collection_modifyitems(config, items):
    skip_integration = config.getoption("--skip-integration")
    mark_skip_integration = pytest.mark.skip(reason="skipping integration test")
    for item in items:
        if skip_integration and "integration" in item.keywords:
            item.add_marker(mark_skip_integration)

def pytest_addoption(parser):
    parser.addoption(
        "--skip-integration", action="store_true", default=False,
        help="Skip integration tests."
    )
