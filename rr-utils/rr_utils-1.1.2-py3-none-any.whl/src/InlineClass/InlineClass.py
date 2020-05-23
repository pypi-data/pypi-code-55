class InlineClass(object):
    def __init__(self, _dict, deep=False):
        self.__dict__ = _dict
        if deep:
            self._convert_dit_to_class()

    def _convert_dit_to_class(self):
        for k, v in self.__dict__.items():
            if isinstance(v, dict):
                self.__dict__[k] = InlineClass(v, deep=True)
