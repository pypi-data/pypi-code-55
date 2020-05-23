import re


def create_response_parameters(method_config, cors):
    params = {}

    if 'response_headers' in method_config:
        for header in method_config['response_headers'].keys():
            params['method.response.header.' + header] = method_config['response_headers'][header]

    if cors:
        # put CORS headers in method
        params['method.response.header.Access-Control-Allow-Origin'] = '\'*\''

    return params


def create_request_parameters(method_config):
    params = {}

    if 'request_headers' in method_config:
        for header in method_config['request_headers'].keys():
            params['method.request.header.' + header] = method_config['request_headers'][header]

    if 'request_querystrings' in method_config:
        for header in method_config['request_querystrings'].keys():
            params['method.request.querystring.' + header] = method_config['request_querystrings'][header]

    return params


def create_request_template(request_parameters, path_parameters=[], request_body=[]):
    string = '{'

    for param in request_parameters.keys():
        name = param.split('.')[3]
        string += '"{0}" : "$input.params(\'{0}\')",'.format(name)

    for param in path_parameters:
        string += '"{0}" : "$input.params(\'{0}\')",'.format(param)

    for param in request_body:
        string += '"{0}" : $input.json(\'$.{0}\'),'.format(param)

    if string.endswith(','):
        string = string[:-1]

    return string + '}'


def get_path_parameters(path):
    return re.findall(r'{([A-Za-z0-9]*)}', path)


def get_error_response_template():
    return '''{
            "error": "$util.parseJson($input.path(\'$.errorMessage\')).userMessage",
            "time": "$context.requestTimeEpoch",
            "requestId": "$context.requestTimeEpoch $context.requestId"
        }'''


def get_error_catchall_response_template():
    return '''{
            "error": "Bad Gateway",
            "time": "$context.requestTimeEpoch",
            "requestId": "$context.requestId"
        }'''


def get_success_response_template():
    return '$util.parseJson($input.body)'
