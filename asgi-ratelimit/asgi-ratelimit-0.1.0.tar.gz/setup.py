# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ratelimit', 'ratelimit.backends']

package_data = \
{'': ['*']}

extras_require = \
{':python_version < "3.8"': ['typing_extensions>=3.7.4,<4.0.0'],
 ':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.6,<0.7'],
 'redis': ['aredis>=1.1.8,<2.0.0']}

setup_kwargs = {
    'name': 'asgi-ratelimit',
    'version': '0.1.0',
    'description': '',
    'long_description': '# ASGI RateLimit\n\nLimit user access frequency to specified URL. Base on ASGI.\n\n## Install\n\n```\n# Only install\npip install asgi-ratelimit\n\n# Use redis\npip install asgi-ratelimit[redis]\n```\n\n## Usage\n\nThe following example will limit users under the `"default"` group to access `/second_limit` at most once per second and `/minute_limit` at most once per minute. And the users in the `"admin"` group have no restrictions.\n\n```python\nfrom typing import Tuple\n\nfrom ratelimit import RateLimitMiddleware, Rule\nfrom ratelimit.backends.redis import RedisBackend\n\ndef auth_function(scope) -> Tuple[str, str]:\n    """\n    Resolve the user\'s unique identifier and the user\'s group from ASGI SCOPE.\n\n    If there is no group information, it should return "default".\n    """\n    return USER_UNIQUE_ID, GROUP_NAME\n\n\nrate_limit = RateLimitMiddleware(\n    ASGI_APP,\n    AUTH_FUNCTION,\n    RedisBackend(),\n    {\n        "/second_limit": [Rule(second=1), Rule(group="admin")],\n        "/minute_limit": [Rule(minute=1), Rule(group="admin")],\n    },\n)\n```\n',
    'author': 'abersheeran',
    'author_email': 'me@abersheeran.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/abersheeran/asgi-ratelimit',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
