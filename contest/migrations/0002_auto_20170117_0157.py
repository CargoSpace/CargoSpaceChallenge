# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AutoContestTitle',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False, default=uuid.uuid4, editable=False)),
                ('title', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ContestSetting',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False, default=uuid.uuid4, editable=False)),
                ('interval', models.IntegerField(default=3)),
                ('duration', models.IntegerField(default=30)),
                ('pauseAutomaticContest', models.BooleanField(default=False)),
                ('useAutoContestTitle', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AlterField(
            model_name='problemset',
            name='problem_type',
            field=models.CharField(choices=[('A', 'Problem A'), ('B', 'Problem B'), ('C', 'Problem C'), ('D', 'Problem D'), ('E', 'Problem E')], max_length=30),
        ),
    ]
