# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-25 05:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fbm_dimitrib11', '0005_auto_20171125_0513'),
    ]

    operations = [
        migrations.AddField(
            model_name='audiochunk',
            name='audio_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='fbm_dimitrib11.Audio'),
            preserve_default=False,
        ),
    ]
