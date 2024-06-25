# Generated by Django 5.0.6 on 2024-06-25 19:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('artist_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Album',
            fields=[
                ('album_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('artwork', models.URLField(blank=True, default='')),
                ('songlist', models.TextField()),
                ('released', models.CharField(max_length=200)),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.artist')),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('song_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='songs', to='home.album')),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.artist')),
            ],
        ),
    ]