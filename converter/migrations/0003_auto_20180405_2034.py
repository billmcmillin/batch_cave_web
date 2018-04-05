# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-04-05 20:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('converter', '0002_conversion_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='conversion',
            old_name='name',
            new_name='Name',
        ),
        migrations.AddField(
            model_name='conversion',
            name='Type',
            field=models.IntegerField(choices=[(0, 'None'), (1, 'ER_EAI_1st'), (2, 'ER_EAI_2nd'), (3, 'ER_OECD')], default=0),
        ),
    ]
