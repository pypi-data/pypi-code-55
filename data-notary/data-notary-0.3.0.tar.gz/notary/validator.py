class Validator(object):
    def __init__(self, attrs={}, **kwargs):
        self.errors = {}

        if type(attrs) is dict:
            for attr in attrs:
                setattr(self, attr, attrs[attr])

        for attr in kwargs:
            setattr(self, attr, kwargs[attr])

    def __getattr__(self, name):
        def _missing(*args, **kwargs):
            return None

        return _missing()

    def validate(self):
        raise Exception("You must implement the validate() function in a subclass")

    def is_valid(self):
        self.errors = {}
        self.validate()

        return len(self.errors) == 0

    def assert_present(self, attr, message = "not_present"):
        try:
            att = getattr(self, attr)
        except AttributeError:
            att = None

        if att is None:
            self._add_error(attr, message)
            return False

        return True

    def assert_list(self, attr, message="not_valid"):
        try:
            lst = getattr(self, attr)
        except AttributeError:
            lst = None

        if type(lst) is not list:
            self._add_error(attr, message)

            return False

        return True

    def assert_not_present(self, attr, message="not_allowed"):
        try:
            if getattr(self, attr) is not None:
                self._add_error(attr, message)
                return False
        except AttributeError:
            pass

        return True

    def assert_in(self, lst, attr, message = "{}_not_in_list"):
        val = getattr(self, attr)

        if type(lst) is not list:
            self._add_error(lst, "not_valid")
            return

        if not val in lst:
            self._add_error(attr, message.format(val))

    def _add_error(self, attr, error):
        if self.errors.get(attr) is None:
            self.errors[attr] = []

        self.errors[attr].append(error)

