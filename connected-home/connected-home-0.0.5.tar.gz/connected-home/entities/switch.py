import time
from .thing import Thing

class Switch(Thing):
    """Definition of a Switch."""

    def __init__(self, name='Test Switch', status=False):
        """
        Switch Constructor

        Parameters
        ---------
        name
            A string to assign to the `name` instance attribute.
        status
            A boolean to set the status of the switch.
        """
        super().__init__(name)
        self.status = status
        self.controls.extend(["switch_on", "switch_off", "toggle"])
        self.type = __class__.__name__
        self.update()

    def switch_on(self):
        """
        Switching on the switch.
        """
        self.status = True
        print('Switched ' + self.text_status() + '!')
        self.update()
        return True

    def switch_off(self):
        """
        Switching off the switch.
        """
        self.status = False
        print('Switched ' + self.text_status() + '!')
        self.update()
        return True

    def toggle(self):
        """
        Switching off the switch.
        """
        self.status = not self.status
        print('Toggled, switched ' + self.text_status() + '!')
        self.update()
        return True

    def text_status(self):
        if (self.status):
            return 'On'
        return 'Off'

    def to_json(self):
        switch_json = super().to_json()
        switch_json["status"] = self.status
        print(switch_json)
        return switch_json