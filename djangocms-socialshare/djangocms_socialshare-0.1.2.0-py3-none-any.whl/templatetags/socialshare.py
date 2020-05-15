from typing import Union

from django import template
from django.http import HttpRequest
from django.utils import translation
from djangocms_page_meta.utils import get_page_meta
from djangocms_socialshare.models import SocialLink
from djangocms_socialshare.models import SocialShareButton
from djangocms_socialshare.models import Type


register = template.Library()


@register.simple_tag(takes_context=True)
def item_url(context: dict, item: Union[SocialShareButton, SocialLink]):
    if type(item) == SocialLink:
        if item.type == Type.EMAIL:
            return f'mailto:{item.url}'
        else:
            return item.url

    request: HttpRequest = context['request']
    meta = get_page_meta(request.current_page, translation.get_language())
    if item.type == Type.FACEBOOK:
        return f'https://www.linkedin.com/sharing/share-offsite/?url={meta.url}'
    elif item.type == Type.LINKEDIN:
        return (
            f'https://www.linkedin.com/sharing/share-offsite/?url={meta.url}'
        )
    elif item.type == Type.EMAIL:
        return (
            f'mailto:?subject=I wanted you to see this site&amp;'
            f'body=Check out this site {meta.url}.'
        )
