# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AutoContestTitle',
            fields=[
                ('id', models.UUIDField(serialize=False, primary_key=True, editable=False, default=uuid.uuid4)),
                ('title', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('id', models.UUIDField(serialize=False, primary_key=True, editable=False, default=uuid.uuid4)),
                ('title', models.TextField()),
                ('description', models.TextField(null=True, blank=True)),
                ('image', models.FileField(null=True, upload_to='', blank=True)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('language', models.CharField(max_length=5, default='en')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ContestProblem',
            fields=[
                ('id', models.UUIDField(serialize=False, primary_key=True, editable=False, default=uuid.uuid4)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('contest', models.ForeignKey(to='contest.Contest')),
            ],
        ),
        migrations.CreateModel(
            name='ContestSetting',
            fields=[
                ('id', models.UUIDField(serialize=False, primary_key=True, editable=False, default=uuid.uuid4)),
                ('title', models.TextField(default='Settings')),
                ('interval', models.IntegerField(default=3)),
                ('duration', models.IntegerField(default=30)),
                ('pauseAutomaticContest', models.BooleanField(default=False)),
                ('useAutoContestTitle', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ContestSubmission',
            fields=[
                ('id', models.UUIDField(serialize=False, primary_key=True, editable=False, default=uuid.uuid4)),
                ('submission', models.FileField(upload_to='')),
                ('accepted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('contest', models.ForeignKey(to='contest.Contest')),
            ],
        ),
        migrations.CreateModel(
            name='ProblemInput',
            fields=[
                ('id', models.UUIDField(serialize=False, primary_key=True, editable=False, default=uuid.uuid4)),
                ('label', models.TextField()),
                ('language', models.CharField(max_length=5, default='en')),
                ('problem_stdin', models.FileField(upload_to='')),
                ('problem_stdout', models.FileField(upload_to='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProblemSet',
            fields=[
                ('id', models.UUIDField(serialize=False, primary_key=True, editable=False, default=uuid.uuid4)),
                ('title', models.TextField(default='')),
                ('problem', models.TextField()),
                ('language', models.CharField(max_length=5, default='en')),
                ('image', models.FileField(null=True, upload_to='', blank=True)),
                ('problem_type', models.CharField(max_length=30, choices=[('A', 'Problem A'), ('B', 'Problem B'), ('C', 'Problem C'), ('D', 'Problem D'), ('E', 'Problem E')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, default=None, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='probleminput',
            name='problem',
            field=models.ForeignKey(to='contest.ProblemSet'),
        ),
        migrations.AddField(
            model_name='contestsubmission',
            name='problem',
            field=models.ForeignKey(to='contest.ProblemSet'),
        ),
        migrations.AddField(
            model_name='contestsubmission',
            name='submitted_by',
            field=models.ForeignKey(blank=True, null=True, default=None, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='contestproblem',
            name='problem',
            field=models.ForeignKey(to='contest.ProblemSet'),
        ),
    ]
