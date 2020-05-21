from . import __version__ as corgy_erp_version

from django import template

register = template.Library()

@register.simple_tag()
def current_version():
    return corgy_erp_version