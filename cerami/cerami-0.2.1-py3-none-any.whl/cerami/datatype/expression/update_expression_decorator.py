class UpdateExpressionDecorator(object):
    def __init__(self, action, expression):
        self.action = action
        self.expression = expression

    def __str__(self):
        return "{} {}".format(self.action, self.expression)

    def attribute_map(self):
        return self.expression.attribute_map()

    def value_dict(self):
        return self.expression.value_dict()

    def _generate_variable_name(self, column_name):
        return self.expression._generate_variable_name(self, column_name)


