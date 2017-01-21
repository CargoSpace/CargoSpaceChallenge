# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0002_auto_20170120_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contestproblem',
            name='problem',
            field=models.ForeignKey(related_name='contest_problems', to='contest.ProblemSet'),
        ),
        migrations.AlterField(
            model_name='problemset',
            name='problem_type',
            field=models.CharField(choices=[('A', 'Problem A'), ('B', 'Problem B'), ('C', 'Problem C'), ('D', 'Problem D')], max_length=30),
        ),
    ]
