# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-22 18:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Translations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender_psid', models.IntegerField()),
                ('translation', models.CharField(max_length=500)),
            ],
        ),
    ]