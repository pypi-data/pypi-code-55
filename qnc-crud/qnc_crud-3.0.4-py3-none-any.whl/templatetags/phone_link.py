import re

from django import template
from django.utils.html import format_html

register = template.Library()

def international_format(possible_phone_number, default_area_code='306'):
    # If they included an extenstion, strip it off
    possible_phone_number = possible_phone_number.lower().split('x')[0]

    digits = re.sub(r'\D', '', possible_phone_number)
    if len(digits) == 7 :
        digits = default_area_code + digits
    if len(digits) == 10 :
        digits = '1' + digits

    if len(digits) != 11 :
        return None

    return '+' + digits

@register.filter
def possible_phone_href(possible_phone_number):
    '''
        Suggested Usage:
            <a {{some_number|possible_phone_href}}>{{possible_phone_number}}</a>

        You always have the wrapping <a>, even if we can't parse the number.
        If we can't parse the number, no href is printed (which is valid html, a tag will NOT match :link)
    '''
    n = international_format(possible_phone_number)
    if not n :
        return ''

    return format_html(' href="tel:{}"', n)