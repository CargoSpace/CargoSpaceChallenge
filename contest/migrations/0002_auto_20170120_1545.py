# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problemset',
            name='title',
            field=models.TextField(default=None),
        ),
    ]
