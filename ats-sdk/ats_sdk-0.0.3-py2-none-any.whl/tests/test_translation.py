from shuttlis.time import time_now

from ats_sdk.domain import TranslatableMessages
from ats_sdk.translation import translate, fetch_translatable_strings


def test_fetch_translatable_strings_in_simple_dict():
    class FakeMessages(TranslatableMessages):
        NAME = "cb.name"
        CITY = "cb.city"

    resource = {"name": FakeMessages.NAME, "city": FakeMessages.CITY}

    translatable_strings = set(fetch_translatable_strings(resource))

    assert {"cb.name", "cb.city"} == translatable_strings


def test_fetch_translatable_strings_in_nested_dict():
    class FakeMessages(TranslatableMessages):
        NAME = "cb.name"
        CITY = "cb.city"

    resource = {"name": FakeMessages.NAME, "data": {"city": FakeMessages.CITY}}

    translatable_strings = set(fetch_translatable_strings(resource))

    assert {"cb.name", "cb.city"} == translatable_strings


def test_fetch_translatable_strings_in_nested_dict_with_list():
    class FakeMessages(TranslatableMessages):
        NAME = "cb.name"
        CITY = "cb.city"

    resource = {
        "name": FakeMessages.NAME,
        "data": [{"city": FakeMessages.CITY}, {"name": FakeMessages.NAME}],
    }

    translatable_strings = set(fetch_translatable_strings(resource))

    assert {"cb.name", "cb.city"} == translatable_strings


def test_fetch_translatable_strings_in_nested_dict_with_other_types():
    class FakeMessages(TranslatableMessages):
        NAME = "cb.name"
        CITY = "cb.city"

    resource = {
        "name": FakeMessages.NAME,
        "house": "random",
        "age": 10,
        "dob": time_now().date(),
        "data": [{"city": FakeMessages.CITY}, {"name": FakeMessages.NAME}],
    }

    translatable_strings = set(fetch_translatable_strings(resource))

    assert {"cb.name", "cb.city"} == translatable_strings


def test_translate_with_simple_dict():
    class FakeMessages(TranslatableMessages):
        NAME = "cb.name"
        CITY = "cb.city"

    resource = {"name": FakeMessages.NAME, "city": FakeMessages.CITY}
    translated_strings = {"cb.name": "name in en", "cb.city": "city in en"}

    translated_resource = translate(
        resource=resource, translated_strings=translated_strings
    )

    assert {"name": "name in en", "city": "city in en"} == translated_resource


def test_translate_with_nested_dict():
    class FakeMessages(TranslatableMessages):
        NAME = "cb.name"
        CITY = "cb.city"

    resource = {"name": FakeMessages.NAME, "data": {"city": FakeMessages.CITY}}
    translated_strings = {"cb.name": "name in en", "cb.city": "city in en"}

    translated_resource = translate(
        resource=resource, translated_strings=translated_strings
    )

    assert {"name": "name in en", "data": {"city": "city in en"}} == translated_resource


def test_translate_with_nested_dict_with_list():
    class FakeMessages(TranslatableMessages):
        NAME = "cb.name"
        CITY = "cb.city"

    resource = {
        "name": FakeMessages.NAME,
        "data": [{"city": FakeMessages.CITY}, {"name": FakeMessages.NAME}],
    }
    translated_strings = {"cb.name": "name in en", "cb.city": "city in en"}

    translated_resource = translate(
        resource=resource, translated_strings=translated_strings
    )

    assert {
        "name": "name in en",
        "data": [{"city": "city in en"}, {"name": "name in en"}],
    } == translated_resource


def test_translate_with_nested_dict_with_other_types():
    class FakeMessages(TranslatableMessages):
        NAME = "cb.name"
        CITY = "cb.city"

    resource = {
        "name": FakeMessages.NAME,
        "house": "random",
        "age": 10,
        "dob": time_now().date(),
        "data": [{"city": FakeMessages.CITY}, {"name": FakeMessages.NAME}],
    }

    translated_strings = {"cb.name": "name in en", "cb.city": "city in en"}

    translated_resource = translate(
        resource=resource, translated_strings=translated_strings
    )

    assert {
        "name": "name in en",
        "house": "random",
        "age": 10,
        "dob": time_now().date(),
        "data": [{"city": "city in en"}, {"name": "name in en"}],
    } == translated_resource
