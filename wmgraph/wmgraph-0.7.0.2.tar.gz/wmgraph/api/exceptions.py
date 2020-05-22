
class MgraphApiError(Exception):
    code = None
    graph_message = None
    inner_error = None

    def __init__(self, graph_data=None, message=None):
        super(MgraphApiError, self).__init__(graph_data)
        self.graph_data = graph_data or {}
        self.message = message
        # see https://docs.microsoft.com/en-us/graph/errors
        error = self.graph_data.get('error')
        if error:
            self.code = error.get('code', 'unknown')
            self.graph_message = error.get('message', '?')
            self.inner_error = error.get('innerError')

    def __str__(self):
        if self.code:
            return f'''{self.code}: {self.graph_message}
    Inner error: {self.inner_error}
    Message: {self.message}'''
        return super(MgraphApiError, self).__str__()


class MgraphConnectionError(Exception):
    def __init__(self, graph_data=None, message=None):
        super(MgraphConnectionError, self).__init__(graph_data)
        self.graph_data = graph_data or {}
        self.message = message
        # see https://docs.microsoft.com/en-us/graph/errors
        self.error = self.graph_data.get('error')
        self.error_description = self.graph_data.get('error_description', '?')

    def __str__(self):
        if self.graph_data:
            return f'''{self.error}
    {self.error_description}'''
        return super(MgraphConnectionError, self).__str__()
