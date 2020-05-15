# Generated by Django 2.1.10 on 2019-07-24 14:35

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('terra_geocrud', '0004_auto_20190724_0906'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crudview',
            name='map_style',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict),
        ),
        migrations.AlterField(
            model_name='crudview',
            name='pictogram',
            field=models.ImageField(blank=True, null=True, upload_to='crud/views/pictograms'),
        ),
    ]
