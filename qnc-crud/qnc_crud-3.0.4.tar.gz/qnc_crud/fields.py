from django import forms
from django.utils.translation import gettext as _

class TrueFalseWidgetMixin:
    '''
        A widget mixin for use with TrueFalseField and TrueFalseRadioField

        Allows you to pass True/False as initial value, as well as 'true'/'false'.
    '''
    def format_value(self, value):
        try:
            return {
                True: ['true'], 
                'true': ['true'], 
                False: ['false'],
                'false': ['false'],
            }[value]
        except KeyError:
            return ['']
class TrueFalseSelectWidget(TrueFalseWidgetMixin, forms.Select):
    pass
class TrueFalseRadioWidget(TrueFalseWidgetMixin, forms.RadioSelect):
    pass

class TrueFalseField(forms.TypedChoiceField):
    '''
        A choice field that renders a select list of empty/yes/no choices, which coerce to None, True, False
    '''
    @staticmethod
    def coerce(value):
        return dict(true=True,false=False).get(value)

    def __init__(self, true=_('Yes'), false=_('No'), **kwargs):
        kwargs['choices'] = [
            ('', kwargs.pop('empty_label', '---')),
            ('true', true),
            ('false', false),
        ]
        kwargs.setdefault('widget', TrueFalseSelectWidget)
        return super().__init__(coerce=TrueFalseField.coerce, empty_value=None, **kwargs)

class TrueFalseRadioField(forms.TypedChoiceField):
    '''
        A choice field that renders yes/no radio buttons, with value coerced to None/True/False
    '''
    @staticmethod
    def coerce(value):
        return dict(true=True,false=False).get(value)

    def __init__(self, true=_('Yes'), false=_('No'), **kwargs):
        # Allow initializing with string values or actual True/False
        if kwargs.get('initial') == True :
            kwargs['initial'] = 'true'
        if kwargs.get('initial') == False :
            kwargs['initial'] = 'false'

        kwargs['choices'] = [
            ('true', true),
            ('false', false),
        ]
        kwargs.setdefault('widget', TrueFalseRadioWidget)
        return super().__init__(coerce=TrueFalseRadioField.coerce, empty_value=None, **kwargs)

