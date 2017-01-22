# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contestsubmission',
            name='accepted',
        ),
        migrations.AddField(
            model_name='contest',
            name='contest_type',
            field=models.CharField(max_length=20, choices=[('Regular', 'Regular'), ('ACM-Style', 'ACM-Style'), ('Code-Jam-Style', 'Code-Jam-Style')], default='Regular'),
        ),
        migrations.AddField(
            model_name='contestsetting',
            name='last_read_next_contest',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestsubmission',
            name='submission_state',
            field=models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')], default='Pending'),
        ),
        migrations.AddField(
            model_name='probleminput',
            name='point',
            field=models.IntegerField(default=10),
        ),
        migrations.AddField(
            model_name='problemset',
            name='example_input',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='problemset',
            name='example_output',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='problemset',
            name='problem_color',
            field=models.TextField(null=True, default='Blue', blank=True),
        ),
        migrations.AddField(
            model_name='problemset',
            name='source_credit',
            field=models.TextField(default=None),
        ),
        migrations.AlterField(
            model_name='problemset',
            name='problem_type',
            field=models.CharField(max_length=30, choices=[('A', 'Problem A'), ('B', 'Problem B'), ('C', 'Problem C'), ('D', 'Problem D')], default='A'),
        ),
    ]
