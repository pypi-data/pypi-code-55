from libvis.modules import BaseModule
import json

class {{cookiecutter.name}}(BaseModule):
    name="{{cookiecutter.name}}"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hello = 'world'

    def serial(self):
        return json.dumps(self)
