from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.contrib.admin.options import csrf_protect_m
from django.contrib.admin.options import TO_FIELD_VAR
from django.contrib.admin.options import unquote

class Button(object):

    def __init__(self, href, title, target="", klass="", icon="", help_text=""):
        self.href = href
        self.title = title
        self.target = target
        self.klass = klass
        self.icon = icon
        self.help_text = help_text

    @classmethod
    def from_dict(cls, data):
        item = cls(**data)
        return item


class DjangoObjectToolbarAdmin(admin.ModelAdmin):

    @csrf_protect_m
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        if object_id:
            to_field = request.POST.get(TO_FIELD_VAR, request.GET.get(TO_FIELD_VAR))
            obj = self.get_object(request, unquote(object_id), to_field)
            extra_context["django_object_toolbar_changeform_buttons"] = self.get_django_object_toolbar_buttons("django_object_toolbar_changeform_buttons", obj)
        return super().changeform_view(request, object_id, form_url, extra_context)

    def django_object_toolbar(self, obj):
        return self.get_django_object_toolbar("django_object_toolbar_buttons", obj)
    django_object_toolbar.short_description = _("Django Object Toolbar")

    def get_django_object_toolbar(self, buttons_property, obj):
        buttons = self.get_django_object_toolbar_buttons(buttons_property, obj)
        return render_to_string("django-object-toolbar-admin/object-toolbar.html", {
            "buttons": buttons,
        })

    def get_django_object_toolbar_buttons(self, buttons_property, obj):
        buttons = []
        object_toolbar_buttons = getattr(self, buttons_property, [])
        for button in object_toolbar_buttons:
            buttons.append(self.make_django_object_toolbar_button(button, obj))
        return buttons

    def make_django_object_toolbar_button(self, button, obj):
        if isinstance(button, Button):
            return button
        if isinstance(button, str):
            button_function = getattr(self, button, None)
            if button_function:
                button = button_function(obj)
            else:
                button_function = getattr(obj, button, None)
                if button_function:
                    button = button_function()
                else:
                    raise RuntimeError("make_django_object_toolbar_button failed: {0}".format(button))
        if isinstance(button, dict):
            return Button.from_dict(**button)
        if isinstance(button, str):
            href = button
            title = getattr(button_function, "title", href)
            target = getattr(button_function, "target", "")
            klass = getattr(button_function, "klass", "")
            icon = getattr(button_function, "icon", "")
            help_text = getattr(button_function, "help_text", "")
            return Button(href, title, target, klass, icon, help_text)
        if isinstance(result, Button):
            return button
        else:
            raise RuntimeError("make_django_object_toolbar_button failed: {0}".format(button))

    class Media:
        css = {
            "all": [
                "fontawesome/css/all.min.css",
            ]
        }
