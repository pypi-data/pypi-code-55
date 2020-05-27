import json
import os
import requests
import base64
from datauri import DataURI
from spb.orm.type import Type
from spb.orm import Model
from spb.orm import AttributeModel
from spb.orm.utils import is_data_url, is_url

class Data(Model):
    RESOURCE_NAME = 'asset'

    id = Type(property_name='id', immutable=True, filterable=True)
    file = Type(property_name='file')
    file_name = Type(property_name='fileName')
    file_size = Type(property_name='fileSize')
    dataset = Type(property_name='dataset')
    data_key = Type(property_name='dataKey')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if len(args) == 1 and isinstance(args[0], dict):
            # if args has dict in first row of args -> kwargs
            kwargs = args[0]
        if 'file' in kwargs:
            setattr(self, 'file', kwargs['file'])

    def __setattr__(self, name, value):
        if name is 'file':
            file_contents = None
            file_size = None
            if os.path.exists(value):
                file_size = os.path.getsize(value)
                file_name = os.path.basename(value)
                file_contents = DataURI.from_file(value)
                file_contents = file_contents.replace('\n', '') # I don't know why
                super().__setattr__('file_name', file_name)
            elif is_data_url(value):
                file_contents = DataURI(value)
                file_size = len(file_contents.data)
            elif is_url(value):
                response = requests.get(value)
                content_type = response.headers["content-type"]
                encoded_body = base64.b64encode(response.content)
                file_size = len(response.content.decode('utf-8'))
                file_contents = f"data:{content_type};base64,{encoded_body.decode()}"
            # file size cannot be bigger than 10MB
            assert file_size <= 10*1024*1024
            super().__setattr__('file_size', file_size)
            super().__setattr__('file', file_contents)
        else:
            super().__setattr__(name, value)



