import json
import time

from django import template
from django.conf import settings
from django.shortcuts import resolve_url
from django.utils.html import format_html
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def millisecond_timestamp():
    return str(int(round(time.time()*1000)))

def get_errormessage_id(bound_field):
    return f'error-{bound_field.form.prefix}-{bound_field.name}'

@register.filter
def add_aria_errormessage(bound_field):
    # You can call this as many times as you like
    if hasattr(bound_field, 'aria_errormessage_id') :
        return

    error_message_id = get_errormessage_id(bound_field)
    bound_field.aria_errormessage_id = error_message_id
    
    _as_widget = bound_field.as_widget
    def as_widget(widget=None, attrs=None, only_initial=False):
        attrs = attrs or {}
        attrs['aria-errormessage'] = error_message_id
        return _as_widget(widget=widget, attrs=attrs, only_initial=only_initial)

    bound_field.as_widget = as_widget

    return ''

@register.filter
def with_error_message_container(bound_field):
    add_aria_errormessage(bound_field)
    return format_html('''
        {field}
        <div class="error" aria-live="polite" id="{error_message_id}"></div>
    ''', field=bound_field, error_message_id=bound_field.aria_errormessage_id)


@register.filter
def with_widget_attr(bound_field, attr):
    # Note - this MUTATES the bound_field
    # You can call this as many times as you like, with different attributes
    name, value = attr.split(',', 1)

    _as_widget = bound_field.as_widget
    def as_widget(widget=None, attrs=None, only_initial=False):
        attrs = attrs or {}
        attrs[name] = value
        return _as_widget(widget=widget, attrs=attrs, only_initial=only_initial)

    bound_field.as_widget = as_widget
    return bound_field