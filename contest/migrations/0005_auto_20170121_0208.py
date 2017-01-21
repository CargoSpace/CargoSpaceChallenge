# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0004_auto_20170121_0152'),
    ]

    operations = [
        migrations.RenameField(
            model_name='problemset',
            old_name='problem',
            new_name='description',
        ),
    ]
