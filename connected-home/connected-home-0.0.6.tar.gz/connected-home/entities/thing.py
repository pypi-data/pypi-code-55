import time

class Thing:
    """A Thing represents a physical or virtual entity collecting data and offering services."""

    def __init__(self, name='Test Thing', id=None):
        """
        Thing Constructor

        Parameters
        ---------
        name
            A string to assign to the `name` instance attribute.
        """
        self.name = name
        if (id is None):
            self.id = name.lower().replace(" ", "-")
        else:
            self.id = id
        self.controls = []
        self.type = __class__.__name__
        self.last_update = time.time()

    def to_json(self):
        thing_json = {}
        if self.name is not None:
            thing_json["name"] = self.name
        return thing_json

    def update(self):
        self.last_update = time.time()