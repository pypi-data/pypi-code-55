def get_rest_id(rest_object_url: str):
    """ 'http://.../api/run/123/' => 123"""
    url = rest_object_url[:-1]
    return int(url[url.rindex('/') + 1:])
