# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-27 02:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('fbm_dimitrib11', '0003_auto_20171127_0208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conversation',
            name='finished_date_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='conversation',
            name='started_date_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
