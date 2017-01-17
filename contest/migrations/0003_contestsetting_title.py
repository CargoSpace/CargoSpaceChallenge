# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0002_auto_20170117_0157'),
    ]

    operations = [
        migrations.AddField(
            model_name='contestsetting',
            name='title',
            field=models.TextField(default='Settings'),
        ),
    ]
