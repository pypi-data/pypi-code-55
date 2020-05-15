# Generated by Django 3.0.6 on 2020-05-09 11:33

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.contrib.taggit
import modelcluster.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
    ]

    operations = [
        migrations.CreateModel(
            name='Compte',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('passwd', models.CharField(max_length=40, verbose_name='Password')),
            ],
        ),
        migrations.CreateModel(
            name='RSSEntries',
            fields=[
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('content', models.TextField(verbose_name='Content')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('rssid', models.CharField(max_length=200, verbose_name='ID')),
                ('published', models.DateTimeField(verbose_name='Published')),
                ('update', models.DateTimeField(verbose_name='Updated')),
                ('is_saved', models.BooleanField(default=False)),
                ('is_read', models.BooleanField(default=False)),
                ('url', models.CharField(max_length=200, verbose_name='URL')),
            ],
            options={
                'verbose_name': 'RSS Entry',
                'verbose_name_plural': 'RSS Entries',
            },
        ),
        migrations.CreateModel(
            name='RSSFeeds',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=120, verbose_name='Name')),
                ('url', models.URLField(verbose_name='URL')),
                ('active', models.BooleanField(default=True)),
                ('twit', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'RSS Feed',
                'verbose_name_plural': 'RSS Feeds',
            },
        ),
        migrations.CreateModel(
            name='TwitterConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('consumer_key', models.CharField(max_length=100)),
                ('consumer_secret', models.CharField(max_length=100)),
                ('access_token_key', models.CharField(max_length=100)),
                ('access_token_secret', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Twitter Config',
                'verbose_name_plural': 'Twitter Config',
            },
        ),
        migrations.CreateModel(
            name='RSSEntriesTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='tag', to='snotra_rss.RSSEntries')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='snotra_rss_rssentriestag_items', to='taggit.Tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='rssentries',
            name='feed',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='snotra_rss.RSSFeeds'),
        ),
        migrations.AddField(
            model_name='rssentries',
            name='tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of tags.', through='snotra_rss.RSSEntriesTag', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
