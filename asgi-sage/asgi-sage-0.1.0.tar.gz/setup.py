# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asgi_sage']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'asgi-sage',
    'version': '0.1.0',
    'description': 'Security Headers for asgi apps',
    'long_description': '# asgi-sage\n\n[![Package version](https://badge.fury.io/py/asgi-sage.svg)](https://pypi.org/project/asgi-sage)\n\nSecurity Headers Middleware for Asgi App heavily inspired by [flask-talisman](https://github.com/GoogleCloudPlatform/flask-talisman)\n\n## Installation\n\n```\npip install asgi-sage\n```\n\n## Usage\n\n```\nfrom asgi_sage.middleware import SageMiddleware\n\nasync def app(scope, receive, send):\n    assert scope["type"] == "http"\n    headers = [(b"content-type", "text/plain")]\n    await send({"type": "http.response.start", "status": 200, "headers": headers})\n    await send({"type": "http.response.body", "body": b"Hello, world!"})\n\napp = SageMiddleware(app)\n```\n\n## Options\n\n- `feature_policy: dict = {}, force_https: bool = True`\n- `force_https: bool = False`\n- `force_https_permanent: bool = False`\n- `frame_options: Optional[str] = "SAMEORIGIN"`\n- `strict_transport_security: bool = True`\n- `strict_transport_security_preload: bool = False`\n- `strict_transport_security_max_age: int = 60 \\* 60 \\_ 24 \\* 365`\n- `strict_transport_security_include_subdomains: bool = True`\n- `content_security_policy: Optional[dict] = None`\n- `referrer_policy: str = "strict-origin-when-cross-origin"`\n- `session_cookie_secure: bool = True`\n- `session_cookie_http_only: bool = True`\n\n## Road Map\n\n- [ ] Per Request overriding\n- [ ] Add tests for different ASGI frameworks like [Quart](https://pgjones.gitlab.io/quart/) and [Django 3.0+](https://docs.djangoproject.com/en/3.0/topics/async/)\n- [ ] Properly support websockets\n',
    'author': 'Jt Miclat',
    'author_email': 'jtmiclat@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jtmiclat/asgi-sage',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
