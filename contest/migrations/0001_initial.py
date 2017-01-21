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
                ('id', models.UUIDField(editable=False, default=uuid.uuid4, primary_key=True, serialize=False)),
                ('title', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('id', models.UUIDField(editable=False, default=uuid.uuid4, primary_key=True, serialize=False)),
                ('title', models.TextField()),
                ('description', models.TextField(blank=True, null=True)),
                ('image', models.FileField(blank=True, upload_to='', null=True)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('language', models.CharField(default='en', max_length=5)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ContestProblem',
            fields=[
                ('id', models.UUIDField(editable=False, default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('contest', models.ForeignKey(to='contest.Contest', related_name='contest_problems')),
            ],
        ),
        migrations.CreateModel(
            name='ContestSetting',
            fields=[
                ('id', models.UUIDField(editable=False, default=uuid.uuid4, primary_key=True, serialize=False)),
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
                ('id', models.UUIDField(editable=False, default=uuid.uuid4, primary_key=True, serialize=False)),
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
                ('id', models.UUIDField(editable=False, default=uuid.uuid4, primary_key=True, serialize=False)),
                ('label', models.TextField()),
                ('language', models.CharField(default='en', max_length=5)),
                ('problem_stdin', models.FileField(upload_to='')),
                ('problem_stdout', models.FileField(upload_to='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProblemSet',
            fields=[
                ('id', models.UUIDField(editable=False, default=uuid.uuid4, primary_key=True, serialize=False)),
                ('title', models.TextField(default=None)),
                ('description', models.TextField()),
                ('language', models.CharField(default='en', max_length=5)),
                ('image', models.FileField(blank=True, upload_to='', null=True)),
                ('problem_type', models.CharField(choices=[('A', 'Problem A'), ('B', 'Problem B'), ('C', 'Problem C'), ('D', 'Problem D')], max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='probleminput',
            name='problem',
            field=models.ForeignKey(to='contest.ProblemSet', related_name='problem_input'),
        ),
        migrations.AddField(
            model_name='contestsubmission',
            name='problem',
            field=models.ForeignKey(to='contest.ProblemSet'),
        ),
        migrations.AddField(
            model_name='contestsubmission',
            name='submitted_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='contestproblem',
            name='problem',
            field=models.ForeignKey(to='contest.ProblemSet'),
        ),
    ]
