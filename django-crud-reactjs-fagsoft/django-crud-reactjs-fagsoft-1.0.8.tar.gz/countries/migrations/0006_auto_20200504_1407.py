# Generated by Django 3.0.5 on 2020-05-04 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('countries', '0005_auto_20200503_0432'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='phone_code',
            field=models.CharField(max_length=15, null=True),
        ),
    ]
