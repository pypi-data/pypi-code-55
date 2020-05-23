from django.forms.widgets import TextInput as Ti, PasswordInput as Pi, NumberInput as Ni, EmailInput as Ei, \
    SelectDateWidget as Sdw, URLInput as Ui, HiddenInput as Hi, MultipleHiddenInput as Mhi, FileInput as Fi, \
    Textarea as T, ClearableFileInput as Cfi, DateInput as Di, DateTimeInput as Dti, TimeInput as Tmi, \
    CheckboxInput as Ci, NullBooleanSelect as Nbs


class TextInput(Ti):
    template_name = "web/forms/widgets/text.html"

    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.attrs.update({'class': 'input'})


class PasswordInput(Pi):
    template_name = "web/forms/widgets/password.html"

    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.attrs.update({'class': 'input'})


class NumberInput(Ni):
    template_name = "web/forms/widgets/number.html"

    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.attrs.update({'class': 'input'})


class EmailInput(Ei):
    template_name = "web/forms/widgets/email.html"

    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.attrs.update({'class': 'input'})


class URLInput(Ui):
    template_name = "web/forms/widgets/url.html"

    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.attrs.update({'class': 'input'})


class HiddenInput(Hi):
    template_name = "web/forms/widgets/hidden.html"

    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.attrs.update({'class': 'input'})


class MultipleHiddenInput(Mhi):
    template_name = "web/forms/widgets/multiple_hidden.html"

    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.attrs.update({'class': 'input'})


class FileInput(Fi):
    template_name = "web/forms/widgets/file.html"

    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.attrs.update({'class': 'input'})


class ClearableFileInput(Cfi):
    template_name = "web/forms/widgets/clearable_file_input.html"

    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.attrs.update({'class': 'input'})


class Textarea(T):
    template_name = "web/forms/widgets/textarea.html"

    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.attrs.update({'class': 'textarea'})


class DateInput(Di):
    def __init__(self, attrs=None, format=None):
        super().__init__(attrs, format)
        self.attrs.update({'class': 'input'})


class DateTimeInput(Dti):
    def __init__(self, attrs=None, format=None):
        super().__init__(attrs, format)
        self.attrs.update({'class': 'input'})


class TimeInput(Tmi):
    def __init__(self, attrs=None, format=None):
        super().__init__(attrs, format)
        self.attrs.update({'class': 'input'})


class CheckboxInput(Ci):
    template_name = "web/forms/widgets/checkbox.html"

    def __init__(self, attrs=None, check_test=None):
        super().__init__(attrs, check_test)
        self.attrs.update({'class': 'checkbox'})


class NullBooleanSelect(Nbs):
    template_name = "web/forms/widgets/select.html"

    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.attrs.update({'class': 'select'})


class SelectDateWidget(Sdw):
    def __init__(self, attrs=None, years=None, months=None, empty_label=None):
        super().__init__(attrs, years, months, empty_label)
        self.attrs.update({'class': 'select'})
