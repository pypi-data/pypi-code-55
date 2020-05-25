# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asgi_sage']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'asgi-sage',
    'version': '0.1.0a1',
    'description': 'Security Headers for asgi apps',
    'long_description': '# asgi-sage\n\nSecurity Headers Middleware for Asgi App heavily inspired by [flask-talisman](https://github.com/GoogleCloudPlatform/flask-talisman)\n\n# TODO\n\n- [ ] feature_policy: dict = {}, force_https: bool = True,\n- [x] force_https: bool = False,\n- [x] force_https_permanent: bool = False,\n- [x] frame_options: Optional[str] = "SAMEORIGIN",\n- [x] strict_transport_security: bool = True,\n- [x] strict_transport_security_preload: bool = False,\n- [x] strict_transport_security_max_age: int = 60 \\* 60 \\_ 24 \\* 365,\n- [ ] strict_transport_security_include_subdomains: bool = True,\n- [ ] content_security_policy: str = "default-src: \'self\'",\n- [ ] content_security_policy_nonce_in: list = [],\n- [ ] content_security_policy_report_only: bool = False,\n- [ ] content_security_policy_report_uri: Optional[str] = None,\n- [x] referrer_policy: str = "strict-origin-when-cross-origin",\n- [ ] session_cookie_secure: bool = True,\n- [ ] session_cookie_http_only: bool = True,\n- [ ] force_file_save: bool = False,\n- [ ] Per View override\n',
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
