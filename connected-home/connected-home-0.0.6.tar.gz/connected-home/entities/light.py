import time
from .thing import Thing

class Light(Thing):
    """Definition of a Light."""

    def __init__(self, name='Test Light', status=False):
        """
        Light Constructor

        Parameters
        ---------
        name
            A string to assign to the `name` instance attribute.
        status
            A boolean to set the status of the light.
        """
        super().__init__(name)
        self.status = False
        self.controls.extend(["turn_on", "turn_off"])
        self.type = __class__.__name__
        self.update()

    def turn_on(self):
        """
        Turn on the light.
        """
        self.status = True
        print('Light\'s ' + self.text_status() + '!')
        self.update()
        return True

    def turn_off(self):
        """
        Turn off the light.
        """
        self.status = False
        print('Light\'s ' + self.text_status() + '!')
        self.update()
        return True

    def text_status(self):
        if (self.status):
            return 'On'
        return 'Off'

    def to_json(self):
        light_json = super().to_json()
        light_json["status"] = self.status
        print(light_json)
        return light_json