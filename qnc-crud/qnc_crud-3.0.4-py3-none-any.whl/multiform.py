class MultiForm:
    '''
        A convenience class for working with multiple forms as if they were one single form.

        We aim to implement enough of the Form api that an instance of this class:
            can be rendered via "qnc_crud/form_fields.html" (untested)
            can be passed to js_response.set_form_errors    (tested briefly)

        We may add various other useful properties/methods, as well.
    '''

    def __init__(self, *forms):
        self.forms = forms

    def is_valid(self):
        valid = True
        for form in self.forms :
            if not form.is_valid() :
                valid = False
        return valid

    def __iter__(self):
        for form in self.forms :
            for field in form :
                yield field

    def iter_non_field_errors(self):
        for form in self.forms :
            for error in form.non_field_errors() :
                yield error

    def non_field_errors(self):
        return list(self.iter_non_field_errors())