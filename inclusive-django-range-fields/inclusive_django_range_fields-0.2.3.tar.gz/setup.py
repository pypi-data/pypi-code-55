# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['inclusive_django_range_fields', 'inclusive_django_range_fields.drf']

package_data = \
{'': ['*']}

install_requires = \
['Django>=1.8', 'djangorestframework>=3.0']

setup_kwargs = {
    'name': 'inclusive-django-range-fields',
    'version': '0.2.3',
    'description': "Inclusive Django Range Fields which uses default bounds as '[]'",
    'long_description': '# Inclusive Django Range Fields\n\n![Inclusive](https://media.giphy.com/media/xUOwGdD7RGT4CTnUaY/giphy.gif "Inclusive")\n\nThe default bound of Django range fields is `[)`. This package follows default bounds as `[]`.\n\n## How to use?\n\n```sh\npip install inclusive-django-range-fields\n```\n\n### Django\n\n```python\n# models.py\n\nfrom django.db import models\nfrom inclusive_django_range_fields import InclusiveIntegerRangeField\n\nclass AdCampaign(models.Model):\n    age_target = InclusiveIntegerRangeField()\n```\n\n```\n>> AdCampaign.objects.first().age_target\nNumericRange(18, 30, \'[]\')\n```\n### Django Rest Framework\n\n```python\n# serializers.py\n\nfrom rest_framework import serializers\nfrom inclusive_django_range_fields.drf import InclusiveIntegerRangeField\n\nclass AdCampaignSerializer(serializers.ModelSerializer):\n    age_target = InclusiveIntegerRangeField()\n\n    class Meta:\n        model = AdCampaign\n        fields = (\n            "id",\n            "age_target",\n        )\n```\n\n```json\n{\n  "id": 1993,\n  "age_target": {\n    "lower": 18,\n    "upper": 30\n  }\n}\n```\n\n## Reference\n\n### Model Fields\n\n- `inclusive_django_range_fields.InclusiveIntegerRangeField`\n- `inclusive_django_range_fields.InclusiveBigIntegerRangeField`\n- `inclusive_django_range_fields.InclusiveDateRangeField`\n\n### Ranges\n\n- `inclusive_django_range_fields.InclusiveNumericRange`\n- `inclusive_django_range_fields.InclusiveDateRange`\n- `inclusive_django_range_fields.InclusiveDateTimeTZRange`\n\n\n### Django Rest Framework Serializers\n\n- `inclusive_django_range_fields.drf.InclusiveIntegerRangeField`\n- `inclusive_django_range_fields.drf.InclusiveDateRangeField`\n\n\n### Form Fields\n\n- `inclusive_django_range_fields.InclusiveIntegerRangeFormField`\n- `inclusive_django_range_fields.InclusiveDateRangeFormField`\n\n\n## PyPI\nhttps://pypi.org/project/inclusive-django-range-fields/\n',
    'author': 'Hipo',
    'author_email': 'pypi@hipolabs.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hipo/inclusive-django-range-fields',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7',
}


setup(**setup_kwargs)
