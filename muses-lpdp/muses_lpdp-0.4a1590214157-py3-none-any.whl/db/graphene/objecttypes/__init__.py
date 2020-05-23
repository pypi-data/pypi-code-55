import graphene
from graphene import ObjectType
from graphene_django import DjangoObjectType

from db.graphene.enums import LanguagesEnum
from db.models import SiteParam


class SpellCheckType(ObjectType):
    word = graphene.String(required=True)
    language = graphene.Field(LanguagesEnum)


class SiteParamType(DjangoObjectType):
    class Meta:
        model = SiteParam
