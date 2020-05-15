# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-18 15:28
from django.db import migrations


"""
Remove testcases.(add|change|delete)_testcasebug and
testcases.(add|change|delete)_testcasebugsystem permissions set to default
groups.

Issue and IssueTracker permissions are set in apps.py migration post handler.

It is a little different for permissions migration than common schema's
migration. Setting permissions to default group happens after all migrations
finish, so add new permissions there.

Note that, there is no easy way to restore original permissions to default
groups. If it is required to migrate back, please add original permissions
back manually.
"""


def forward(apps, schema_editor):
    permission_model = apps.get_model('auth', 'Permission')
    group_model = apps.get_model('auth', 'Group')

    perms_codename = (
        'add_testcasebug',
        'change_testcasebug',
        'delete_testcasebug',
        'add_testcasebugsystem',
        'change_testcasebugsystem',
        'delete_testcasebugsystem',
    )

    for g in group_model.objects.all():
        for codename in perms_codename:
            if not g.permissions.filter(codename=codename).exists():
                continue
            perm = permission_model.objects.get(codename=codename)
            g.permissions.remove(perm)


class Migration(migrations.Migration):

    dependencies = [
        ('issuetracker', '0017_add_default_issues_display_url_fmt'),
    ]

    operations = [
        migrations.RunPython(
            forward, reverse_code=migrations.RunPython.noop)
    ]
