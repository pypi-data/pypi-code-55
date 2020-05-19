from http import HTTPStatus

import pytest
from responses import mock
from shuttlis.time import time_now

from ats_sdk.domain import TranslatableMessages
from ats_sdk.error import ClientError
from ats_sdk.services import AlternateTextService

fake_ats_url = "https://fake_ats_url"


@mock.activate
def test_translate_and_serialize_successful():
    mock.add(
        mock.GET,
        f"{fake_ats_url}/api/v1/translate/static",
        status=HTTPStatus.OK,
        json={"data": {"cb.name": "name in en", "cb.city": "city in en"}},
    )

    class FakeMessages(TranslatableMessages):
        NAME = "cb.name"
        CITY = "cb.city"

    dob = time_now().date()
    resource = {
        "name": FakeMessages.NAME,
        "age": 10,
        "data": {
            "hello": "world",
            "dob": dob,
            "name": FakeMessages.NAME,
            "city": FakeMessages.CITY,
        },
    }

    translated_resource = AlternateTextService(
        url=fake_ats_url
    ).translate_and_serialize(resource=resource, locale="en")

    assert {
        "name": "name in en",
        "age": 10,
        "data": {
            "hello": "world",
            "dob": dob.isoformat(),
            "name": "name in en",
            "city": "city in en",
        },
    } == translated_resource


@mock.activate
def test_translate_and_serialize_raises_client_error_if_translation_fails():
    mock.add(
        mock.GET,
        f"{fake_ats_url}/api/v1/translate/static",
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )

    class FakeMessages(TranslatableMessages):
        NAME = "cb.name"
        CITY = "cb.city"

    dob = time_now().date()
    resource = {
        "name": FakeMessages.NAME,
        "age": 10,
        "data": {
            "hello": "world",
            "dob": dob,
            "name": FakeMessages.NAME,
            "city": FakeMessages.CITY,
        },
    }

    with pytest.raises(ClientError):
        AlternateTextService(url=fake_ats_url).translate_and_serialize(
            resource=resource, locale="en"
        )
