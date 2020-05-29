# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['decorated_registry']

package_data = \
{'': ['*']}

extras_require = \
{':python_version < "3.7"': ['dataclasses>0.1']}

setup_kwargs = {
    'name': 'decorated-registry',
    'version': '0.0.2',
    'description': 'Decorator-based registry for objects with arbitrary payloads',
    'long_description': "decorated_registry\n==================\n\nImplementation of generalised registries for Python.\n\nAllows you to seamlessly create registries of tests, modules, DSLs and RPCs.\n\nSupports arguments and fully typed.\n\nExample\n-------\n\n```python\nfrom typing import List, Type\nfrom dataclasses import dataclass\nfrom decorated_registry import Registry, ConstructorPayloadFactory\n\n# framework/abstract.py\n\n@dataclass\nclass ModuleConfig:\n    init_priority: int = -1\n\n\nclass Module:\n    pass\n\n# framework/registry.py\n\napplication_module: Registry[ModuleConfig, Type[Module]] = Registry(\n    payload_factory=ConstructorPayloadFactory(dict)\n)\n\n# authentication_mod/impl.py\n\n@application_module\nclass AuthenticationModule(Module):\n    pass\n\n\n# database_mod/impl.pu\n\n@application_module(init_priority=2)\nclass DatabaseSessionModule(Module):\n    pass\n\n# framework/app.py\n\ndef load_modules() -> List[Module]:\n    rtn = []\n    # ensure modules are loaded in the order given by `ModuleConfig.priority`\n    modules_priority = sorted(application_module.items, key=lambda x: x.payload.init_priority)\n    for x in modules_priority:\n        module_cls: Type[Module] = x.value\n        module = module_cls()\n        rtn.append(module)\n    return rtn\n\n\n# framework/main.py\n\ndef main():\n    modules = load_modules()\n\n\nif __name__ == '__main__':\n    main()\n```\n",
    'author': 'Andrey Cizov',
    'author_email': 'acizov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/andreycizov/python-decorated_registry',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
