# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contestsetting',
            name='last_read_next_contest',
            field=models.TextField(null=True, blank=True),
        ),
    ]
