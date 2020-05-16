# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['marshmallow_pynamodb']

package_data = \
{'': ['*']}

install_requires = \
['marshmallow>=3.0.0', 'marshmallow_enum', 'pynamodb>=4.0.0']

setup_kwargs = {
    'name': 'marshmallow-pynamo-db',
    'version': '0.10.3',
    'description': 'PynamoDB integration with the Marshmallow (de)serialization library',
    'long_description': '# Welcome to Marshmallow-Pynamo-DB\n\n[![PyPI](https://img.shields.io/pypi/v/marshmallow-pynamo-db)](https://pypi.org/project/marshmallow-pynamo-db/)\n[![Build](https://github.com/chrismaille/marshmallow-pynamodb/workflows/tests/badge.svg)](https://github.com/chrismaille/marshmallow-pynamodb/actions)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/stela)](https://www.python.org)\n<a href="https://github.com/psf/black"><img alt="Code style: black"\nsrc="https://img.shields.io/badge/code%20style-black-000000.svg"></a>\n\n> Original Project: https://github.com/mathewmarcus/marshmallow-pynamodb\n\n[PynamoDB](https://pynamodb.readthedocs.io/en/latest/) integration with\nthe [Marshmallow](https://marshmallow.readthedocs.io/en/latest/)\n(de)serialization library.\n\n###  Installation\nFrom PyPi:\n```shell\n  $ pip install marshmallow-pynamo-db\n```\n\nFrom GitHub:\n\n```shell\n  $ pip install git+https://github.com/chrismaille/marshmallow-pynamodb#egg=marshmallow_pynamodb\n```\n\n### Declare your models\n\n```python\nfrom pynamodb.models import Model\nfrom pynamodb.attributes import UnicodeAttribute\n\nclass User(Model):\n    class Meta:\n        table_name = "user"\n    email = UnicodeAttribute(null=True)\n    first_name = UnicodeAttribute(range_key=True)\n    last_name = UnicodeAttribute(hash_key=True)\n```\n\n###  Generate marshmallow schemas\n\n```python\nfrom marshmallow_pynamodb import ModelSchema\n\nclass UserSchema(ModelSchema):\n    class Meta:\n        model = User\n\nuser_schema = UserSchema()\n```\n\n### (De)serialize your data\n\n```python\nuser = User(last_name="Smith", first_name="John")\n\nuser_schema.dump(user)\n# {u\'first_name\': u\'John\', u\'last_name\': u\'Smith\', u\'email\': None}\n\nuser_schema.load({"last_name": "Smith", "first_name": "John"})\n# user<Smith>\n```\n\n### pynamodb-attributes support\nCurrently we support the following custom attributes from\n[pynamodb-attributes](https://github.com/lyft/pynamodb-attributes)\nlibrary:\n\n- `IntegerAttribute` – same as `NumberAttribute` but whose value is typed as `int` (rather than `float`)\n- `UUIDAttribute` - serializes a `UUID` Python object as a `S` type attribute (_e.g._ `\'a8098c1a-f86e-11da-bd1a-00112444be1e\'`)\n- `UnicodeEnumAttribute` - serializes a string-valued `Enum` into a Unicode (`S`-typed) attribute\n- `IntegerEnumAttribute` - serializes a integer-valued `Enum` into a\n  Number (`S`-typed) attribute\n\n```python\nimport uuid\nfrom enum import Enum\n\nfrom pynamodb.attributes import UnicodeAttribute\nfrom pynamodb.models import Model\nfrom pynamodb_attributes import IntegerAttribute, UUIDAttribute, UnicodeEnumAttribute\n\nfrom marshmallow_pynamodb import ModelSchema\n\n\nclass Gender(Enum):\n    male = "male"\n    female = "female"\n    not_informed = "not_informed"\n\n\nclass People(Model):\n    class Meta:\n        table_name = "people"\n    uuid = UUIDAttribute(hash_key=True)\n    first_name = UnicodeAttribute()\n    last_name = UnicodeAttribute()\n    gender = UnicodeEnumAttribute(Gender)\n    age = IntegerAttribute()\n\n    \nclass PeopleSchema(ModelSchema):\n    class Meta:\n        model = People\n\n\npeople_schema = PeopleSchema()\npayload = {\n    "uuid": "064245dc0e5f415c95d3ba6b8f728ae4",\n    "first_name": "John",\n    "last_name": "Doe",\n    "gender": Gender.male.value,\n    "age": 43\n}\npeople = people_schema.load(payload)\n# people<064245dc-0e5f-415c-95d3-ba6b8f728ae4>\nassert people.gender == Gender.male\nassert people.uuid == uuid.UUID("064245dc0e5f415c95d3ba6b8f728ae4")\n```\n\nSee more examples in tests.\n\n### Nested models? No problem\n\n```python\nfrom marshmallow_pynamodb.schema import ModelSchema\n\nfrom pynamodb.models import Model\nfrom pynamodb.attributes import (\n    ListAttribute,\n    MapAttribute,\n    NumberAttribute,\n    UnicodeAttribute,\n)\n\nclass Location(MapAttribute):\n    latitude = NumberAttribute()\n    longitude = NumberAttribute()\n    name = UnicodeAttribute()\n\n\nclass Person(MapAttribute):\n    firstName = UnicodeAttribute()\n    lastName = UnicodeAttribute()\n    age = NumberAttribute()\n\n\nclass OfficeEmployeeMap(MapAttribute):\n    office_employee_id = NumberAttribute()\n    person = Person()\n    office_location = Location()\n\n\nclass Office(Model):\n    class Meta:\n        table_name = \'OfficeModel\'\n\n    office_id = NumberAttribute(hash_key=True)\n    address = Location()\n    employees = ListAttribute(of=OfficeEmployeeMap)\n\n\nclass OfficeSchema(ModelSchema):\n    class Meta:\n        model = Office\n\n# noinspection PyTypeChecker\nOfficeSchema().load(\n    {\n        \'office_id\': 789,\n        \'address\': {\n            \'latitude\': 6.98454,\n            \'longitude\': 172.38832,\n            \'name\': \'some_location\'\n        },\n        \'employees\': [\n            {\n                \'office_employee_id\': 123,\n                \'person\': {\n                    \'firstName\': \'John\',\n                    \'lastName\': \'Smith\',\n                    \'age\': 45\n                },\n                \'office_location\': {\n                    \'latitude\': -24.0853,\n                    \'longitude\': 144.87660,\n                    \'name\': \'other_location\'\n                }\n            },\n            {\n                \'office_employee_id\': 456,\n                \'person\': {\n                    \'firstName\': \'Jane\',\n                    \'lastName\': \'Doe\',\n                    \'age\': 33\n                },\n                \'office_location\': {\n                    \'latitude\': -20.57989,\n                    \'longitude\': 92.30463,\n                    \'name\': \'yal\'\n                }\n            }\n        ]\n    }\n)\n# Office<789>\n```\n\n### Using inherited fields\n\nTo use inherited fields from parent classes, use the `inherit_field_models` option. Example:\n\n```python\n# pip install pynamodb_attributes\nimport uuid\nfrom pynamodb_attributes import UnicodeEnumAttribute, UUIDAttribute\nfrom pynamodb.attributes import UnicodeAttribute\nfrom pynamodb.models import Model\nfrom marshmallow_pynamodb import ModelSchema\nfrom enum import Enum\n\nclass MyStatus(Enum):\n   CREATED = "CREATED"\n\nclass BaseDocument(Model):\n  uuid = UUIDAttribute(default=uuid.uuid4)\n\nclass MyDocument(BaseDocument):\n  status = UnicodeEnumAttribute(MyStatus, default=MyStatus.CREATED)\n  content = UnicodeAttribute()\n\nclass MyDocumentSchema(ModelSchema):\n  class Meta:\n    model = MyDocument\n    inherit_field_models = True\n    \nMyDocumentSchema().load({"content": "foo"})\n```\n\n### License\nMIT licensed. See the bundled\n[LICENSE](https://github.com/mathewmarcus/marshmallow-pynamodb/blob/master/LICENSE.txt)\nfile for more details.\n\n### Not working?\n\nDont panic. Get a towel and, please, open a\n[issue](https://github.com/chrismaille/stela/issues).\n',
    'author': 'Mathew Marcus',
    'author_email': 'mathewmarcus456@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/chrismaille/marshmallow-pynamodb',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
