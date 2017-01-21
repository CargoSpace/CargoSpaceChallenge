# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0002_contestsetting_last_read_next_contest'),
    ]

    operations = [
        migrations.AddField(
            model_name='contestsubmission',
            name='submission_state',
            field=models.CharField(default='Pending', choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')], max_length=20),
        ),
    ]
