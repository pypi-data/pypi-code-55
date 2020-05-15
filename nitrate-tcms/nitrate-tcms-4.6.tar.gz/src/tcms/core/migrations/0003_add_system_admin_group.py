# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-02-22 13:55
from django.db import migrations


def add_system_admin_group(app, schema_editor):
    model = app.get_model('auth', 'Group')
    model.objects.create(name='System Admin')


def remove_system_admin_group(app, schema_editor):
    model = app.get_model('auth', 'Group')
    model.objects.filter(name='System Admin').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_add_initial_data'),
    ]

    operations = [
        migrations.RunPython(add_system_admin_group, remove_system_admin_group)
    ]
