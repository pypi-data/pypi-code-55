# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiocrontab']

package_data = \
{'': ['*']}

install_requires = \
['croniter>=0.3.31,<0.4.0']

extras_require = \
{':python_version >= "3.7" and python_version < "3.8"': ['typing_extensions']}

setup_kwargs = {
    'name': 'aiocrontab',
    'version': '0.1.1',
    'description': 'Crontab implementation in asyncio ',
    'long_description': '# AIOCRONTAB\n\nSample project to "flex" my asyncio skills.\n\n\n### Usage\n\n```python\nimport time\n\nimport aiocrontab\n\n\n@aiocrontab.register("*/5 * * * *")\ndef print_every_five_mminutes():\n    print(f"{time.ctime()}: Hello World!!!!!")\n\n@aiocrontab.register("* * * * *")\ndef print_every_mminute():\n    print(f"{time.ctime()}: Hello World!")\n\n\naiocrontab.run()\n```\n\n**TODO**\n\n- [ ] support for diff timezones\n- [ ] support for async task\n- [x] take logger as dependency\n- [ ] Add more meaningful tests\n- [x] fix mypy errors\n- [ ] document the codebase\n- [ ] document usage in readme\n',
    'author': 'Bhavesh Praveen',
    'author_email': 'bhavespraveen.dev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
