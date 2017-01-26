# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0003_auto_20170123_1046'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contestsetting',
            name='last_read_next_contest',
        ),
    ]
