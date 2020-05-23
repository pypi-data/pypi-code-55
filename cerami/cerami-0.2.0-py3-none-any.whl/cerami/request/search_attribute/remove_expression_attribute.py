from .search_attribute import SearchAttribute

class RemoveExpressionAttribute(SearchAttribute):
    def __init__(self, name, value=None):
        value = value or []
        super(RemoveAttribute, self).__init__(name, value)

    def add(self, expression):
        self.value.append(expression)

    def build(self):
        return "REMOVE " + ', '.join(str(expr) for expr in self.value)



