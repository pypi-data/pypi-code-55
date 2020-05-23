from copy import copy
from ..reconstructor import RawReconstructor
from .search_attribute import (
    SearchAttribute,
    DictAttribute,
    QueryExpressionAttribute)

# TODO: break this into classes. Update shouldnt need filter
# and Query should need return_values
class SearchRequest(object):
    def __init__(self, client, tablename="", search_attributes={}, reconstructor=None):
        self.search_attributes = copy(search_attributes)
        self.client = client
        self.reconstructor = reconstructor or RawReconstructor()
        if tablename:
            self.add_attribute(SearchAttribute, 'TableName', tablename)

    def __str__(self):
        return self.build().__str__()

    def add_attribute(self, attr_class, name, value):
        """add a search attribute to a duplicated instance
        @param attr_class - a SearchAttribute class
        @param name - the name of the attribute
        @param value - the value that will be added to the SearchAttribute
        """
        search_attribute = self.search_attributes.get(name, attr_class(name))
        search_attribute.add(value)
        self.search_attributes[name] = search_attribute


    def return_values(self, value):
        self.add_attribute(SearchAttribute,
                           'ReturnValues',
                           value)
        return self

    def filter(self, *expressions):
        """return a new SearchInterface setup with filter attributes
        FilterExpression, ExpressionAttributeNames, ExpressionAttributeValues
        are all required to filter properly
        """
        for expression in expressions:
            names = {}
            names[expression.expression_attribute_name] = expression.datatype.column_name
            self.add_attribute(QueryExpressionAttribute,
                              'FilterExpression',
                              expression)
            self.add_attribute(DictAttribute,
                              'ExpressionAttributeNames',
                              names)
            self.add_attribute(DictAttribute,
                              'ExpressionAttributeValues',
                              expression.value_dict())
        return self

    def build(self):
        """build the dict used by dynamodb"""
        return dict((k, v.build()) for k,v in self.search_attributes.items())

