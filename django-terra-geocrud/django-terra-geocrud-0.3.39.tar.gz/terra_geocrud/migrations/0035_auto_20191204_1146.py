# Generated by Django 2.2.8 on 2019-12-04 11:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('terra_geocrud', '0034_auto_20191204_1017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extralayerstyle',
            name='layer_extra_geom',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='style', to='geostore.LayerExtraGeom'),
        ),
    ]
