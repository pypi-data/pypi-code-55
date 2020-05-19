

class Store(dict):
    """
    """

    def __init__(self, id, action=None):
        """
        """
        self.id = id
        self.action = action

    def __setitem__(self, name, value):
        """
        """
        super().__setitem__(name, value)
        if name != 'action' and self.action:
            self.action(self.id, name, value)
