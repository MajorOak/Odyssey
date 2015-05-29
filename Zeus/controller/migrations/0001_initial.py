# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('request_date', models.DateTimeField(verbose_name=b'date when job was requested')),
                ('request_user', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=20)),
                ('who', models.CharField(max_length=200)),
                ('message', models.CharField(max_length=500)),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'log date')),
            ],
        ),
        migrations.CreateModel(
            name='Scheduler',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(max_length=500)),
                ('start_date', models.DateTimeField(null=True, verbose_name=b'start date this run')),
                ('to_be_ended', models.BooleanField(default=False)),
                ('log_file', models.CharField(max_length=2000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(max_length=500)),
                ('run_date', models.DateTimeField(null=True, verbose_name=b'date of expected launch')),
                ('start_date', models.DateTimeField(null=True, verbose_name=b'date of start')),
                ('end_date', models.DateTimeField(null=True, verbose_name=b'date of end')),
                ('run_number', models.IntegerField(default=0)),
                ('command_line', models.CharField(max_length=4000)),
                ('argument_list', models.CharField(max_length=4000, null=True)),
                ('job', models.ForeignKey(to='controller.Job', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TaskDefinition',
            fields=[
                ('name', models.CharField(max_length=200, serialize=False, primary_key=True)),
                ('command_line', models.CharField(max_length=4000)),
                ('default_argument_list', models.CharField(max_length=4000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TaskDependency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dependency_task', models.CharField(max_length=200)),
                ('task', models.ForeignKey(to='controller.TaskDefinition')),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='name',
            field=models.ForeignKey(to='controller.TaskDefinition'),
        ),
    ]
