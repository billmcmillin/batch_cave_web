# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-04-16 15:10
from __future__ import unicode_literals

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('converter', '0006_auto_20180412_1901'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversion',
            name='MrkIn',
            field=models.FileField(default=None, storage=django.core.files.storage.FileSystemStorage(base_url='/data', location='/home/mcmillwh/BitBucket/batch_mobile/data'), upload_to='infiles/'),
        ),
        migrations.AddField(
            model_name='conversion',
            name='MrkOut',
            field=models.FileField(default=None, storage=django.core.files.storage.FileSystemStorage(base_url='/data', location='/home/mcmillwh/BitBucket/batch_mobile/data'), upload_to='outfiles/'),
        ),
        migrations.AlterField(
            model_name='conversion',
            name='Type',
            field=models.IntegerField(choices=[(0, 'None'), (1, 'ER_EAI_1st'), (2, 'ER_EAI_2nd'), (3, 'ER_OCLC_WCS_SDebk'), (4, '__init__')], default=0),
        ),
    ]
