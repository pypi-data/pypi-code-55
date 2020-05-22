# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sanic_quill', 'sanic_quill.fields', 'sanic_quill.widgets']

package_data = \
{'': ['*'], 'sanic_quill': ['static/editor/*', 'static/tabs/*', 'templates/*']}

install_requires = \
['Sanic-Jinja2>=0.8.0,<0.9.0', 'wtforms>=2.3.1,<3.0.0']

setup_kwargs = {
    'name': 'sanic-quill',
    'version': '0.0.2',
    'description': 'Sanic-quill is a port of Flask-quill to Sanic ecosystem. (quill.js WYSIWYG editor)',
    'long_description': 'sanic-quill\n-----------\n\nSanic-quill is a port of Flask-quill (https://github.com/drewdru/flask-quill/) to Sanic ecosystem. (wtforms widget for quill.js editor (https://github.com/quilljs/quill))\n\nQuill.js is a modern WYSIWYG editor built for compatibility and extensibility.\n\n\n\nTo add routes with edit form:\n\nfrom sanic_quill import add_editor\n\neditor will be able on the route /edit\n\nHow to use\n----------\n\nCheck sample in \'examples\'.\n\n\nTo add  WYSIWYG editor to edit any data/fields you need to define 2 methods:\n\n- get_data (used by editor to get information for model to edit in form)\n- save_data (used by editor to save changes from the form)\n\nEditor expect 3 fields in data:\n\n    -  \'title\',\n    -  \'body\',\n    -  \'preview\'\n\n.. code-block:: python\n\n\n\n    from sanic_quill import add_editor\n\n    ...\n\n    # your Sanic app code\n    # with defining app = Sanic()\n\n    ...\n\n    def get_data(_id):\n        """ this method defines logic to send to \'edit\' form data of the object """\n        for post in posts:\n            if post[\'id\'] == _id:\n                post[\'title\'] = post[\'title\']\n                post[\'content\'] = post[\'text\']\n                post[\'preview\'] = post[\'preview\']\n                return post\n\n\n    def save_data(_id, data):\n        """\n            this method defines logic to save data from \'edit\' form\n\n            data comes like a dict with: content, content_preview and title fields,\n            you need map it to your structure\n        """\n        for num, post in enumerate(posts):\n            if post[\'id\'] == _id:\n                print(\'Update post\')\n                post[\'title\'] = data[\'title\']\n                post[\'text\'] = data[\'content\']\n                post[\'description\'] = data[\'preview\']\n                break\n\n    add_editor(app, get_data, save_data)\n\nAfter that you will have routes \'/edit?\'id=$id_of_your_data_item_to_edit\n\nAlso you can define a path where to save an images and route that will be used to serve uploaded images by default it is \'/img\':\n\n.. code-block:: python\n\n    add_editor(app, get_data, save_data, img_folder="/path/for/images", route_for_img=\'/custom_route\')\n\n',
    'author': 'xnuinside',
    'author_email': 'xnuinside@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
