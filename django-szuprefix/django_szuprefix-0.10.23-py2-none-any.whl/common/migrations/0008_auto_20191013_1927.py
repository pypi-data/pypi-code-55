# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-10-13 19:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0007_auto_20190416_1622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='\u521b\u5efa\u65f6\u95f4'),
        ),
        migrations.AlterField(
            model_name='exceltask',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='\u521b\u5efa\u65f6\u95f4'),
        ),
        migrations.AlterField(
            model_name='image',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='\u521b\u5efa\u65f6\u95f4'),
        ),
        migrations.AlterField(
            model_name='tempfile',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='\u521b\u5efa\u65f6\u95f4'),
        ),
        migrations.AlterField(
            model_name='trash',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='\u5220\u9664\u65f6\u95f4'),
        ),
        migrations.AlterField(
            model_name='versionhistory',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='\u66f4\u65b0\u65f6\u95f4'),
        ),
    ]
