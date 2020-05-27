import spb

from .utils import *
from .query import Query


class Manager(object):  # pylint: disable=R0205
    ''' Data mapper interface (generic repository) for models '''

    def __init__(self, model, type_check=True):
        self.model = model
        self.type_check = type_check
        self.session = spb._get_default_session()

    def _get_model_object(self, options):
        if isinstance(options, self.model):
            return options
        else:
            return self.model(options)

    def query(self, options, optional):
        '''Convert model to graphql query string'''
        model = self._get_model_object(options)
        query = Query.get(model, optional)
        result = self.session.execute(self.model, query)
        return result

    def mutation(self, options, optional):
        '''Convert model to graphql mutation string'''
        query = None
        model = self._get_model_object(options)
        result = None
        query = Query.mutation(model, optional)
        result = self.session.execute(self.model, query)
        return result

    def delete(self, options):
        model = self._get_model_object(options)
        query = Query.delete(model)
        result = self.session.execute(self.model, query)
        return result
