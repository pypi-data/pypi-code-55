
class ResultContainer(object):
    def __init__(self, value):
        from datetime import datetime

        self._value = value
        self._created_at = datetime.utcnow()

    def check_if_valid_ttl(self, ttl):
        from datetime import datetime

        if ttl is None:
            return True

        delta = datetime.utcnow() - self._created_at
        return delta < ttl

    def get_value(self):
        return self._value


