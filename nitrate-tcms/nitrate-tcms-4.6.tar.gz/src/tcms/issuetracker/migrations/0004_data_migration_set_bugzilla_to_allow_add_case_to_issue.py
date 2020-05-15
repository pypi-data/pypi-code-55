# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-01 16:06
from django.db import migrations


def forward(apps, schema_editor):
    IssueTracker = apps.get_model('issuetracker', 'IssueTracker')
    bz = IssueTracker.objects.get(name='Bugzilla')
    bz.allow_add_case_to_issue = True
    bz.save(update_fields=['allow_add_case_to_issue'])


class Migration(migrations.Migration):

    dependencies = [
        ('issuetracker', '0003_migrate_issue_tracker_data'),
    ]

    operations = [
        migrations.RunPython(forward,
                             reverse_code=migrations.RunPython.noop)
    ]
