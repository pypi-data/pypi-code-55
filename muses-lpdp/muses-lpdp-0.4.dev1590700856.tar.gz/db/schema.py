import graphene

from db.graphene.objecttypes import SiteParamType, SpellCheckType
from db.models import SiteParam


class Query(graphene.ObjectType):
    site_params = graphene.List(SiteParamType)
    spell_checks = graphene.List(SpellCheckType)

    def resolve_site_params(self, info, **kwargs):
        if not info.context.user.is_authenticated:
            return SiteParam.objects.none()
        else:
            return SiteParam.objects.all()

    def resolve_spell_checks(self, info, **kwargs):
        if not info.context.user.is_authenticated:
            return None
        else:
            return None
