# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-25 05:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fbm_dimitrib11', '0004_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transcript',
            old_name='chunk_id',
            new_name='chunk',
        ),
        migrations.RemoveField(
            model_name='audiochunk',
            name='audio_id',
        ),
        migrations.RemoveField(
            model_name='transcript',
            name='sender_psid',
        ),
        migrations.AddField(
            model_name='transcript',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='fbm_dimitrib11.User'),
            preserve_default=False,
        ),
    ]
