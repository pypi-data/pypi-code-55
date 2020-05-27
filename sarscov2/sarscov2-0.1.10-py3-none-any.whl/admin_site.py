from django.contrib.admin import AdminSite as DjangoAdminSite
from django.contrib.sites.shortcuts import get_current_site
from django.apps import apps as django_apps
from django.conf import settings

title = getattr(
    settings,
    "SARSCOV2_TITLE",
    django_apps.get_app_config(settings.APP_NAME).verbose_name,
)


class AdminSite(DjangoAdminSite):

    site_title = title
    site_header = title
    index_title = title
    site_url = "/administration/"

    def each_context(self, request):
        context = super().each_context(request)
        context.update(global_site=get_current_site(request))
        context.update(site_title=title, site_header=title, index_title=title)
        return context


sarscov2_admin = AdminSite(name="sarscov2_admin")
sarscov2_admin.disable_action("delete_selected")
