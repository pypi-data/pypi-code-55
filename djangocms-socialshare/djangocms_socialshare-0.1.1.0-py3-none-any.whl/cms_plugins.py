from adminsortable2.admin import SortableInlineAdminMixin
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.contrib.admin import TabularInline
from djangocms_socialshare.models import SocialLink
from djangocms_socialshare.models import SocialLinksPluginModel
from djangocms_socialshare.models import SocialShareButton
from djangocms_socialshare.models import SocialSharePluginModel


class ShareButtonInline(SortableInlineAdminMixin, TabularInline):
    model = SocialShareButton
    extra = 0


@plugin_pool.register_plugin
class SocialSharePlugin(CMSPluginBase):
    model = SocialSharePluginModel
    render_template = 'djangocms_socialshare/socialshare-plugin.html'
    inlines = [
        ShareButtonInline,
    ]


class ShareLinkInline(SortableInlineAdminMixin, TabularInline):
    model = SocialLink
    extra = 0


@plugin_pool.register_plugin
class SocialLinksPlugin(CMSPluginBase):
    model = SocialLinksPluginModel
    render_template = 'djangocms_socialshare/socialshare-plugin.html'
    inlines = [
        ShareLinkInline,
    ]
