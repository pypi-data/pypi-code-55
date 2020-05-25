from django import template
from django.conf import settings
from django.templatetags import static
from django.utils.safestring import mark_safe

from django_handy.url import simple_urljoin


register = template.Library()


@register.simple_tag
def mailto(address, text=None):
    return mark_safe(
        f'<a href="mailto:{address}">{text or address}</a>'
    )


if getattr(settings, 'HOST', None):
    class FullStaticNode(static.StaticNode):
        def url(self, context):
            relative_url = super().url(context)
            return simple_urljoin(settings.HOST, relative_url)


    @register.tag('fullstatic')
    def do_static(parser, token):
        return FullStaticNode.handle_token(parser, token)
