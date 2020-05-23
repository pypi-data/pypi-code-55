from .base_expression import BaseExpression

class RawExpression(BaseExpression):
    def __str__(self):
        attr_name = self.expression_attribute_name
        if hasattr(self.datatype, '_index'):
            attr_name = "{}[{}]".format(attr_name, self.datatype._index)
        return "{attr_name} {expression} {value}".format(
                attr_name=attr_name,
                expression=self.expression,
                value=self.value)

    def value_dict(self):
        """return an empty dict because there should be no ExpressionAttributeValues"""
        return {}

