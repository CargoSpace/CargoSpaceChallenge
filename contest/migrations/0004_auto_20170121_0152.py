# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0003_auto_20170121_0146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contestproblem',
            name='contest',
            field=models.ForeignKey(to='contest.Contest', related_name='contest_problems'),
        ),
        migrations.AlterField(
            model_name='contestproblem',
            name='problem',
            field=models.ForeignKey(to='contest.ProblemSet'),
        ),
    ]
