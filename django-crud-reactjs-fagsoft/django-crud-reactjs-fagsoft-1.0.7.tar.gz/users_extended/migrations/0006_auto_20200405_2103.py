# Generated by Django 3.0.5 on 2020-04-05 21:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users_extended', '0005_auto_20200405_1132'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='useraditionalpermission',
            options={'managed': False, 'permissions': (('list_user', 'Can list user'), ('change_password_user', 'Can change user password'), ('change_permission_user', 'Can change user permission'), ('make_superuser_user', 'Can make user superuser'), ('make_staff_user', 'Can make user staff'), ('make_active_user', 'Can make user active'))},
        ),
    ]
