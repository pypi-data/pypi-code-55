# Generated by Django 2.2.8 on 2019-12-06 01:58
"""
Add a series version as well as a foreign key to the git forge so querying
for a project's merge request is possible.
"""

from django.db import migrations, models
import django.db.models.deletion


def set_git_forge(apps, schema_editor):
    BridgedSubmission = apps.get_model("patchlab", "BridgedSubmission")
    for bridged_submission in BridgedSubmission.objects.all():
        bridged_submission.git_forge = bridged_submission.submission.project.git_forge
        bridged_submission.save()


def reverse_migration(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("patchlab", "0002_drop_unique_commit"),
    ]

    operations = [
        migrations.AddField(
            model_name="bridgedsubmission",
            name="git_forge",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="patchlab.GitForge",
            ),
        ),
        migrations.RunPython(set_git_forge, reverse_migration),
        migrations.AlterField(
            model_name="bridgedsubmission",
            name="git_forge",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="patchlab.GitForge"
            ),
        ),
        migrations.AddField(
            model_name="bridgedsubmission",
            name="series_version",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddIndex(
            model_name="bridgedsubmission",
            index=models.Index(
                fields=["merge_request", "git_forge"],
                name="patchlab_br_merge_r_195b52_idx",
            ),
        ),
    ]
