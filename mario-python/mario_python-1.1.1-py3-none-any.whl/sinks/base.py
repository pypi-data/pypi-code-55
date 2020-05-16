class Sink:
    def __init__(self, name: str):
        self.name = name

    def write(self, *args, **kwargs):
        raise NotImplementedError
