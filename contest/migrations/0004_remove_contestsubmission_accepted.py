# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0003_contestsubmission_submission_state'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contestsubmission',
            name='accepted',
        ),
    ]
