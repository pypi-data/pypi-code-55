# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_stripe',
 'django_stripe.db',
 'django_stripe.migrations',
 'django_stripe.models',
 'django_stripe.utils']

package_data = \
{'': ['*']}

install_requires = \
['django>=3.0,<4.0', 'stripe>=2.48.0,<3.0.0']

setup_kwargs = {
    'name': 'django-stripe-lite',
    'version': '0.2.0',
    'description': 'A library to aid Django integration with Stripe.',
    'long_description': '# django-stripe-lite\n\nProvides a light-touch Django integration with Stripe.\n\nWe handle Stripe webhook security & persisting all events, while allowing your project to take care\nof the business logic.\n\nRequires PostgreSQL, Python 3.x & Django 3.x.\n\n## Installation & Usage\n\n```bash\npip install django-stripe-lite\n```\n\n**Include the app in your INSTALLED_APPS setting:**\n\n```python\nINSTALLED_APPS = (\n    ...,\n    "django_stripe",\n)\n```\n\n**Include the URLs in your URL conf:**\n\n```python\nfrom django.urls import include, path\n\nurlpatterns = [\n    # Assuming we\'re at the root, this will make the webhook\n    # available at /stripe/webhook/\n    path("stripe/", include("django_stripe.urls", namespace="stripe"))\n]\n```\n\n**Set the required settings in your settings file:**\n\n```python\nSTRIPE_WEBHOOK_SECRET = "whsec_0DoBceBjS0jjm7aQj459FXiFSluJEBxt"\n```\n\n**Run the migrations:**\n\n```bash\npython manage.py migrate django_stripe\n```\n\n**Set up your event handlers:**\n\nEvent handlers are simply functions in your code base, which are wrapped with a decorator which\nsignifies that they wish to handle a particular event type (or multiple) when it is received via the\nwebhook.\n\nAll event handlers must be imported at application startup, otherwise the decorator wil not be able\nto register them against the event type. An easy way to ensure this in your local project is to\ntrigger the import in one of your Django Apps `apps.py::AppConfig::ready()` method\n([see the docs](https://docs.djangoproject.com/en/3.0/ref/applications/#django.apps.AppConfig.ready)).\n\nWhen a webhook event is received, all processing of it is wrapped in a transaction such that a\nsingle event handler failure will result in an HTTP 500 returned from the endpoint and the\ntransaction will be rolled back resulting in no database changes for that request. This means that\nthe `WebhookEvent` is not persisted unless:\n\n-   it was received successfully and there were no active handlers registered for the event type,\n    or:\n-   it was received successfully and processed successfully by _all_ active handlers registered\n    against the event type.\n\n```python\nfrom django_stripe.models import WebhookEvent\nfrom django_stripe.webhooks import stripe_webhook_handler\n\n# Single event handler\n@stripe_webhook_handler("customer.subscription.deleted")\ndef delete_customer_subscription(event: WebhookEvent) -> Any:\n    # event.data (dict, Stripe Event object.data field, the object which triggered the webhook event)\n    # event.event_type (str, the full event type name e.g customer.subscription.deleted)\n    # event.mode (textchoices, LIVE or TEST)\n    # event.stripe_created_at (datetime, when Stripe created the event)\n    # event.db_created_at (datetime, when the database initially saved the event)\n    # event.db_last_updated_at (datetime, when the database last saved the event)\n    # event.stripe_id (str, Stripe Event ID)\n    # event.api_version (str, Stripe API version)\n    # event.request_id (str, the Stripe ID of the instigating request, if available)\n    # event.request_idempotency_key (str, the idempotency key of the instigating request, if available)\n    # event.is_processed (bool, whether the event was processed by a handler successfully)\n    # event.headers (dict, the headers of the webhook request)\n    # event.remote_ip (str, Remote IP of the webhook request)\n    pass\n\n# Multiple event handler\n@stripe_webhook_handler(\n    "customer.subscription.created",\n    "customer.subscription.deleted",\n    "customer.subscription.updated",\n)\ndef customer_handler(event: WebhookEvent) -> Any:\n    # See notes above for event structure.\n    pass\n```\n\nThat\'s it, you should be able to start receiving webhook events with the Stripe CLI test client.\nThen once you\'re ready, setup the production webhook via the Stripe dashboard.\n\n## Development\n\nCheck out the repo, then get the deps:\n\n```bash\npoetry install\n```\n\n## Tests\n\n#### Running tests\n\nThe tests themselves use `pytest` as the test runner. If you have installed the `poetry` evironment,\nyou can run them:\n\n```bash\n$ poetry run pytest\n```\n\nThe CI suite is controlled by `tox`, which contains a set of environments that will format (`fmt`),\nlint, and test against all supported Python + Django version combinations.\n\n```bash\n$ tox\n```\n\n#### CI\n\nCI is handled by GitHub Actions. See the Actions tab on Github & the `.github/workflows` folder.\n\n## Publish to PyPi\n\nUpdate versions, then:\n\n```bash\npoetry build\npoetry publish\n```\n',
    'author': 'YunoJuno',
    'author_email': 'code@yunojuno.com',
    'maintainer': 'YunoJuno',
    'maintainer_email': 'code@yunojuno.com',
    'url': 'https://github.com/yunojuno/django-stripe-lite',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
