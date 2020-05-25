import json


class JSONSerializer(object):
    def _json(self, obj):
        return json.dumps(obj)

    def json(self, **kwargs):
        result = self.__call__(**kwargs)
        return self._json(result)


class DataFrameSerializer(JSONSerializer):
    def _json(self, data_frame):
        return data_frame.to_json()


class NumpySerializer(JSONSerializer):
    def _json(self, array):
        return json.dumps({"data": array.tolist()})
