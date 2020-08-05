# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-05-14 06:33
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cron', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='asynccronmail',
            name='log_file',
            field=models.FileField(null=True, upload_to='emails/'),
        ),
        migrations.AlterField(
            model_name='asynccronmail',
            name='csvfile',
            field=models.FileField(upload_to='emails/', validators=[django.core.validators.FileExtensionValidator(['csv'])]),
        ),
    ]
