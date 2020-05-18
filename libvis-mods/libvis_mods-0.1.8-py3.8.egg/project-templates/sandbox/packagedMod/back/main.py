from libvis.modules import BaseModule
import json
from .utils import random_quote

class packagedMod(BaseModule):
    name="packagedMod"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.quote = random_quote()

    def vis_get(self, key):
        value = super().vis_get(key) # makes {value:preprocess(value), type:self.name}
        print('sending value to front: ', key, value)
        return value

    def vis_set(self, key, value):
        super().vis_set(key, value) # same as self[key] = value
        print('updated value form front: ', key, value)
