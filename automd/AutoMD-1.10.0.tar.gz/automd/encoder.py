import flask


class AutoMDObjEncoder(flask.json.JSONEncoder):
    """
    Extension of flask.json.JSONEncoder to allow custom "to_dict" methods
    """
    def default(self, obj: object):
        if hasattr(obj, "to_dict") and callable(obj.to_dict):
            return obj.to_dict()

        return super(obj)
