from django import forms
from django.forms.utils import flatatt
from django.utils.safestring import mark_safe


class IconPickerWidget(forms.TextInput):
    class Media:
        css = {'all': (
            "https://cdn.jsdelivr.net/npm/uikit@3.4.0/dist/css/uikit.min.css",
            'https://fonts.googleapis.com/icon?family=Material+Icons',
            'icon_picker_widget/css/style.css',)}
        js = ("https://code.jquery.com/jquery-3.4.1.min.js",
              'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js',
              'https://cdn.jsdelivr.net/npm/uikit@3.4.0/dist/js/uikit.min.js',
              'https://cdn.jsdelivr.net/npm/uikit@3.4.0/dist/js/uikit-icons.min.js',
              'icon_picker_widget/js/npick.js')

    def render(self, name, value, attrs=None, **kwargs):
        super().render(name, value, attrs)
        flat_attrs = flatatt(attrs)
        atr_id = attrs['id']
        html = f'  <input  {flat_attrs} value="{value}" type="text" class="form-contol use-material-icon-picker" id="{atr_id}" name="{name}"> '
        return mark_safe(html)
