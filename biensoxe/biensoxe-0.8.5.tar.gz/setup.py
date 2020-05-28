# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['biensoxe', 'biensoxe.django']

package_data = \
{'': ['*']}

install_requires = \
['memoprop>=0.2.0,<0.3.0', 'pydantic>=1.0,<2.0']

setup_kwargs = {
    'name': 'biensoxe',
    'version': '0.8.5',
    'description': 'Library to parse and validate Vietnamese vehicle plate',
    'long_description': "========\nBienSoXe\n========\n\n.. image:: https://badgen.net/pypi/v/biensoxe\n   :target: https://pypi.org/project/biensoxe\n\nLibrary to validate and parse Vietnamese vehicle plate.\n\nThis library is not a computer-vision-based license plate recognition software. It instead is used for validating output of such computer vision software. Imagine that you use camera to track all cars coming in and out off your parking lot, but you don't want to save false result (due to wrong angle of camera, for example), you can use this library to check and remove them.\n\nInstall\n-------\n\n.. code-block:: sh\n\n    pip3 install biensoxe\n\n\nUsage\n-----\n\nCall ``VietnamVehiclePlate.from_string``, passing the number string, to create ``VietnamVehiclePlate`` object.\n\n.. code-block:: python\n\n    >>> from biensoxe import VietnamVehiclePlate\n\n    >>> VietnamVehiclePlate.from_string('44A-112.23')\n    VietnamVehiclePlate(compact='44A11223', vehicle_type=<VehicleType.DOMESTIC_AUTOMOBILE: 1>,\n    series='A', order='11223', locality='44', dip_country=None)\n\n    >>> VietnamVehiclePlate.from_string('41-291-NG-01')\n    VietnamVehiclePlate(vehicle_type=<VehicleType.DIPLOMATIC: 9>, series='NG', order='01', locality='41', dip_country='291')\n\n\nThe method raises ``ValueError`` if the string could not be parsed.\n\nTo format the plate number as in daily life, pass ``VietnamVehiclePlate`` to ``str``:\n\n.. code-block:: python\n\n    >>> plate = VietnamVehiclePlate.from_string('72E101130')\n\n    >>> plate\n    VietnamVehiclePlate(compact='72E101130', vehicle_type=<VehicleType.DOMESTIC_MOTORCYCLE_50_TO_175CC: 3>, series='E1', order='01130', locality='72', dip_country=None)\n\n    >>> str(plate)\n    '72-E1 011.30'\n\nDjango\n~~~~~~\n\nThis library provides a field type, ``VietnamVehiclePlateField``, for Django model. The field will return value as ``VietnamVehiclePlate`` object. Here is example:\n\n.. code-block:: python\n\n    from biensoxe.django import VietnamVehiclePlateField\n\n    def default_plate_number():\n        return VietnamVehiclePlate.from_string('10A 00001')\n\n    class Vehicle(models.Model):\n        plate_number = VietnamVehiclePlateField(max_length=20, default=default_plate_number, unique=True)\n\n    def __str__(self):\n        return str(self.plate_number) or self.pk\n\nNote that this field stores value internally as PostgeSQL ``CIText`` data type, so you can only use this field with PostgreSQL.\nYou also need to activate CITextExtension_ yourself.\n\n\nCredit\n------\n\nBrought to you by `Nguyễn Hồng Quân <author_>`_.\n\n\n.. _CITextExtension: https://docs.djangoproject.com/en/2.2/ref/contrib/postgres/operations/#citextextension\n.. _author: https://quan.hoabinh.vn\n",
    'author': 'Nguyễn Hồng Quân',
    'author_email': 'ng.hong.quan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sunshine-tech/BienSoXe',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
