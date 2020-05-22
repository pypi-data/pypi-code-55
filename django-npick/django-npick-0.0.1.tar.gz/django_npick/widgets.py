from django import forms


class IconWidget(forms.TextInput):
    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs=extra_attrs)
        attrs.setdefault('class', 'use-material-icon-picker form-contol')
        return attrs

    class Media:
        css = {
            "icon": (
                # "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css",
                "https://fonts.googleapis.com/icon?family=Material+Icons",
                "css/icon-picker.css",
                "css/unicons-icon-picker.css",)
        }
        # js = (
        # "https://code.jquery.com/jquery-3.4.1.min.js",
        # "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js",
        # "https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js",
        # "js/icon-picker.js",
        # "js/unicons-icon-picker.js",)
