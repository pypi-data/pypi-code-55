def success(body={}):
    import json
    return json.dumps({
        'body': body
    })


def error(error_code, user_message=''):
    import json
    return json.dumps({
        'gatewayResponse': True,
        'status': 'error',
        'type': error_code,
        'userMessage': user_message
    })
