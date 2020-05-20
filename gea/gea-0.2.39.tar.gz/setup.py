# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gea', 'gea.migrations', 'gea.templatetags']

package_data = \
{'': ['*'],
 'gea': ['fixtures/*',
         'static/css/*',
         'static/fonts/*',
         'static/img/*',
         'static/js/*',
         'templates/*',
         'templates/gea/*',
         'templates/gea/doc/*',
         'templates/gea/search/*',
         'templates/gea/tools/*',
         'templates/registration/*']}

install_requires = \
['django-extensions>=2.2.9,<3.0.0',
 'django-nested-admin>=3.3.0,<4.0.0',
 'django>=3.0.6,<4.0.0']

setup_kwargs = {
    'name': 'gea',
    'version': '0.2.39',
    'description': 'Gestión de Expedientes de Agrimensores para Django.',
    'long_description': '# gea\n\nGestión de Expedientes de Agrimensores.\n\n__gea__ es una aplicación web basada en [Django](https://www.djangoproject.com/) para gestionar expedientes de agrimensores. Hasta ahora sólo fue usada en la provincia de _Santa Fe, Argentina_.\n\n## Requisitos previos\n\n- GNU/Linux\n- Python >= 3.6\n- [Django](https://pypi.python.org/pypi/Django/) 3.0.6\n- [psycopg2](https://pypi.python.org/pypi/psycopg2/) (opcional si utiliza PostgreSQL)\n- [django-nested-admin](https://pypi.python.org/pypi/django-nested-admin/) (para formularios anidados)\n\n## Instalación\n\n```bash\n$ pip install gea\n```\n\nSe instalan también los ```requirements``` como Django y nested-admin. Si además quiere utilizar PostgreSQL para la Base de Datos, deberá instalar manualmente psycopg2.\n\n```bash\n$ pip install psycopg2\n```\n\n## Puesta en marcha\n\n### Crear proyecto Django\n\n```bash\n$ django-admin startproject estudio\n```\n\n### Editar ```settings.py``` del proyecto Django:\n\n```bash\n$ # dentro de "estudio"\n$ vim estudio/settings.py\n```\n\n- Agregar __```gea```__ y ```nested_admin``` a las ```INSTALLED_APPS```:\n\n```python\nINSTALLED_APPS = (\n    ...\n    \'gea.apps.GeaConfig\',\n    \'nested_admin\',\n)\n```\n\n- Se pueden acomodar el Idioma y la TimeZone\n\n```python\nLANGUAGE_CODE = \'es-AR\'\nTIME_ZONE = \'America/Argentina/Buenos_Aires\'\n```\n\n#### Para utilizar PostgreSQL (opcional)\n\n- Opcionalmente, configurar la Base de Datos para utilizar PostgreSQL, de otro modo, Django usa SQLite3 por defecto. Editar ```settings.py```.\n\n```python\nDATABASES = {\n    \'default\': {\n        \'ENGINE\': \'django.db.backends.postgresql_psycopg2\',\n        \'NAME\': \'gea\',\n        \'USER\': \'<postgresql-user>\',\n        \'PASSWORD\': \'<postgresql-password>\', # be creative\n        \'HOST\': \'localhost\',\n    }\n}\n```\n\ncon esta opción se debe crear la BD, con el comando ```createdb``` de PostgreSQL\n\n```bash\n$ createdb gea\n```\n\n### Editar ```urls.py``` del proyecto Django:\n\n```bash\n$ # dentro de "estudio"\n$ vim estudio/urls.py\n```\n\n- Importar las vistas de ```gea``` y agregar las urls de las aplicaciones que instalamos:\n\n```python\nfrom django.conf.urls import include, path\n\n\nurlpatterns = [\n    ...\n    path(\'gea/\', include(\'gea.urls\')),\n    path(\'_nested_admin/\', include(\'nested_admin.urls\')),\n]\n```\n\n### Base de datos y Superusuario\n\n```bash\n$ # dentro de "estudio"\n$ python manage.py makemigrations gea\n$ python manage.py migrate\n$ python manage.py createsuperuser\n```\n\n```makemigrations``` y ```migrate``` ponen a punto la base de datos, ```createsuperuser``` instala el sistema de autenticación de Django, _Django\'s auth system_, con lo cual, pedirá usuario, mail y contraseña, por ejemplo: _admin_ y _Af7Dr2ujW_. Con estos datos ingresaremos después a la interfaz de administración.\n\n## Archivos estáticos (css, img, js)\n\nPor último, algo muy importante: los archivos de estilo, imágenes y scripts que usará nuestra nueva aplicación.\n\nEditar ```settings.py``` agregando la siguiente linea:\n\n```python\nSTATIC_ROOT = \'./static/\'\n```\n\nY ejecutar:\n```bash\n$ # dentro de "estudio"\n$ python manage.py collectstatic\n```\n\n¡**LISTO**... Ahora podemos probar cómo quedó nuestra django-app!\n\n```bash\n$ # dentro de "estudio"\n$ python manage.py runserver\n```\n\ne ingresamos a [http://127.0.0.1:8000/gea/](http://127.0.0.1:8000/gea/)... con los datos del superusuario que creamos antes.\n\n## LICENCIA\n\n[MIT](LICENSE)\n',
    'author': 'Santiago Pestarini',
    'author_email': 'santiagonob@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/quijot/gea-package',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4',
}


setup(**setup_kwargs)
