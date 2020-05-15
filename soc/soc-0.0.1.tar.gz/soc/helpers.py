import json


def jsonify(o, **kwargs) -> str:
    return json.dumps(o, **kwargs)
