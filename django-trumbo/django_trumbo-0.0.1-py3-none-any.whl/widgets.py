# coding=utf-8

from django.forms.widgets import Textarea
from django.templatetags.static import static
from django.utils.safestring import mark_safe


class TrumbowygWidget(Textarea):
    class Media:
        css = {
            'all': (
                'trumbowyg/ui/trumbowyg.css',
                'trumbowyg/ui/trumbowyg_reset.css',
            )
        }
        js = (
            'trumbowyg/jquery.min.js',
            'trumbowyg/trumbowyg.min.js',
            'trumbowyg/langs/ru.js',
        )

    def render(self, name, value, attrs=None, renderer=None):
        output = super(TrumbowygWidget, self).render(name, value, attrs, renderer)
        script = u'''
            <script>
                $("#id_%s").trumbowyg({
                svgPath: '%s',
                btns: [
                    ['viewHTML'],
                    ['formatting'],
                    ['strong', 'em', 'del'],
                    ['superscript', 'subscript'],
                    ['link'],
                    ['insertImage'],
                    ['justifyLeft', 'justifyCenter', 'justifyRight', 'justifyFull'],
                    ['unorderedList', 'orderedList'],
                    ['horizontalRule'],
                    ['removeformat'],
                    ['fullscreen']
                ],
                autogrow: true
            });
            </script>
        ''' % (name, static('trumbowyg/ui/icons.svg'))
        output += mark_safe(script)
        return output
