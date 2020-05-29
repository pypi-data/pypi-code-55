from ybc_exception import ParameterTypeError
from ybc_exception import ParameterValueError


class Argument:
    def __init__(self, module_name, method_name, name, value, type, predicates):
        self.module_name = module_name
        self.method_name = method_name
        self.name = name
        self.value = value
        self.type = type
        self.predicates = predicates

    def check_argument(self):
        self._check_type()
        self._check_value()

    def _check_type(self):
        if self.type is not None and not isinstance(self.value, self.type):
            raise ParameterTypeError(self.method_name, self.name)

    def _check_value(self):
        if self.predicates is not None and not self.predicates(self.value):
            raise ParameterValueError(self.method_name, self.name)


class Checker:
    @staticmethod
    def check_arguments(arguments):
        for argument in arguments:
            argument.check_argument()
