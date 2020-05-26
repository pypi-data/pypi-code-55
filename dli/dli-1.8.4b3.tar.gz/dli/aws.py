from datetime import timezone

from botocore.credentials import RefreshableCredentials
from botocore.session import get_session

from boto3 import Session


def create_refreshing_session(
    dli_client, **kwargs
):
    session = Session()

    def refresh():
        return dict(
            access_key=dli_client.session.auth_key,
            secret_key='noop',
            token='noop',
            expiry_time=dli_client.session.token_expires_on.replace(
                tzinfo=timezone.utc
            ).isoformat()
        )


    _refresh_meta = refresh()

    session_credentials = RefreshableCredentials.create_from_metadata(
        metadata=_refresh_meta,
        refresh_using=refresh,
        method='noop'
    )

    session = get_session()
    session._credentials = session_credentials
    return Session(
        botocore_session=session,
        **kwargs
    )
