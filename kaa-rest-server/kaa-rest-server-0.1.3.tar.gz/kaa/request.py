class Request():

    def __init__(self, env):
        self.env = env
        self.method = self.env['REQUEST_METHOD']
        self.path = self.env['PATH_INFO']
        self.remote_addr = self.env['REMOTE_ADDR']
        self.query = self.__get_query()
        self.headers = self.__get_headers()

    def __get_query(self):
        query_params = {}
        query_string = self.env['QUERY_STRING']
        if not query_string:
            return query_params
        for item in query_string.split('&'):
            values = item.split('=')
            if len(values) == 2:
                self.__set_query_value(values[0], values[1], query_params)
        return query_params

    def __set_query_value(self, key, value, query_params):
        if key in query_params:
            if type(query_params[key]) == list:
                query_params[key].append(value)
            else:
                query_params[key] = [query_params[key], value]
        else:
            query_params[key] = value

    def __get_headers(self):
        headers = {}
        for item in self.env:
            if item[:5] == 'HTTP_':
                headers[item[5:]] = self.env[item]
        return headers

    def get_header(self, key):
        if key in self.headers:
            return self.headers[key]
        return None

    def get_query_param(self, key):
        if key in self.query:
            return self.query[key]
        return None

    def get_dict(self):
        return {
            'method': self.method,
            'path': self.path,
            'remoteAddr': self.remote_addr,
            'query': self.query,
            'headers': self.headers
        }
