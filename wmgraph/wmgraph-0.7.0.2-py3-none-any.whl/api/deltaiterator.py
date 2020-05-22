
class GenericDeltaIterator:
    def __init__(self, api, url=None, deltalink=None, **kwargs):
        '''
        Delta iterator.
        If deltalink is given, url is not used and the iterator resumes from that state.

        Example:
            url = 'https://graph.microsoft.com/v1.0/users/delta?$select=displayName,userPrincipalName'
            iterator = GenericDeltaIterator(api, url)
            for item in iterator:
                print(item)
            print(f"next iteration: {iterator.get_next_url()}")
        '''
        self.api = api
        self.url = deltalink or url
        self.kwargs = kwargs
        self.deltalink = deltalink

    def __iter__(self):
        return self._generic_iterate()

    def get_next_url(self):
        return self.deltalink

    def _generic_iterate(self):
        '''private
        Support for paged results. See https://docs.microsoft.com/de-de/graph/paging
        Saves deltalink for delta operations
        '''
        graph_data = self.api.get(self.url, **self.kwargs)
        while 'value' in graph_data:
            deltanext = graph_data.get('@odata.nextLink')
            self.deltalink = graph_data.get('@odata.deltaLink')

            for val in graph_data['value']:
                yield val

            if deltanext:
                graph_data = self.api.get(deltanext)
            else:
                break
