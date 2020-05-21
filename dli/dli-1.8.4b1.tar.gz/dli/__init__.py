import os
import warnings

warnings.filterwarnings(
    'always', module="dli"
)

__version__ = '1.8.4b1'
__product__ = "ihsm-datalake"


def connect(api_key=None,
            root_url="https://catalogue.datalake.ihsmarkit.com/__api",
            host=None,
            debug=None,
            strict=None,
            use_keyring=True):

    from dli.client.session import start_session

    return start_session(
        api_key,
        root_url=root_url,
        host=host,
        debug=debug,
        strict=strict,
        use_keyring=use_keyring
    )

