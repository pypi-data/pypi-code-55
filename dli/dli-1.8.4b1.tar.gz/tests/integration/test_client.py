import pytest
import freezegun
import datetime

@pytest.mark.integration
def test_client_refresh(client, empty_dataset):
    client.get_dataset(empty_dataset.id)
    
    with freezegun.freeze_time(
        client.session.token_expires_on + datetime.timedelta(days=10)
    ):
        client.get_dataset(empty_dataset.id)
