from django_exportapp.helper import exporter
from django_exportapp.helper import BaseClassExporter

from django.contrib.auth.models import User

from .models import Foo

import random


class UserExportapp(BaseClassExporter):
    export_status = True

    def return_field_value(self, field_name, field_value):
        if field_name == 'password':
            return 'pbkdf2_sha256$150000$tPfHwMvjttU2$P0aEFkSPOTdKge3GA77AdPTpITKuzZ2vrZmTnTl4MlA='
        #
        return field_value


exporter.reg(User, UserExportapp)


class FooExportapp(BaseClassExporter):
    export_status = True
    export_mode = ['private', 'public']

    def return_field_value(self, field_name, field_value):
        if field_name == 'f':
            return field_value[:3]

        if field_name == 'phone':
            if field_value != '9501234567':
                field_value = random.randint(9000000000, 9999999999)

        if field_name == 'anketa':
            return ''

        return field_value


exporter.reg(Foo, FooExportapp)
