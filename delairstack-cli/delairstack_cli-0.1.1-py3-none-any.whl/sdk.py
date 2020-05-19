from pathlib import Path

from delairstack import DelairStackSDK

from delairstack_cli import config


def delairstack_sdk(credential_path: Path = config.DEFAULT_CREDENTIAL_PATH, *,
                    profile: str = config.DEFAULT_PROFILE):
    credentials = config.get_credentials(
        credential_path=credential_path,
        profile=profile
    )
    if not credentials:
        credentials = config.setup(credential_path=credential_path)

    return DelairStackSDK(
            user=credentials.username,
            password=credentials.password,
            url=credentials.url,
            proxy_url=credentials.proxy_url,
        )
