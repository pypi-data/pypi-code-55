import operator
import base64
from functools import reduce
from django.conf import settings
from rest_framework import serializers
from cryptography.fernet import Fernet, MultiFernet
from django.db import models


def fernet_base() -> MultiFernet:
    key = settings.KEY_ENCRY
    vector = settings.VECTOR_ENCRY
    key1 = Fernet(key)
    key2 = Fernet(vector)
    fernet = MultiFernet([key1, key2])
    return fernet


def encrypt(texto_plano: str) -> str:
    if not texto_plano:  # pragma: no cover
        return ''
    fernet = fernet_base()
    new_text = fernet.encrypt(str.encode(texto_plano))
    return new_text.decode()


def decrypt(enc: str) -> str:
    if not enc:  # pragma: no cover
        return ''
    fernet = fernet_base()
    decrypted_text = fernet.decrypt(str.encode(enc))
    return decrypted_text.decode()


def search_multiple_fields(queryset, search_fields, parameter):
    def construct_search(field_name):
        if field_name.startswith('^'):
            return "%s__istartswith" % field_name[1:]
        elif field_name.startswith('='):
            return "%s__iexact" % field_name[1:]
        elif field_name.startswith('@'):
            return "%s__search" % field_name[1:]
        else:
            return "%s__icontains" % field_name

    orm_lookups = [construct_search(str(search_field))
                   for search_field in search_fields]
    for bit in parameter.split():
        or_queries = [models.Q(**{orm_lookup: bit})
                      for orm_lookup in orm_lookups]
        queryset = queryset.filter(reduce(operator.or_, or_queries))
    return queryset
