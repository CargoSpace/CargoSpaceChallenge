# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0002_auto_20170122_1755'),
    ]

    operations = [
        migrations.AddField(
            model_name='problemset',
            name='constraints',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='problemset',
            name='input_description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='problemset',
            name='output_description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
