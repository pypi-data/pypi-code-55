# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-18 12:31
from django.db import migrations, models
import django.db.models.deletion

"""
When deleting a plan which is parent of some other plans, set those plan's
parent field NULL instead of deleting those child plans.
"""


class Migration(migrations.Migration):

    dependencies = [
        ('testplans', '0005_add_nonexisting_email_settings_for_existing_plans'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testplan',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='child_set', to='testplans.TestPlan'),
        ),
    ]
