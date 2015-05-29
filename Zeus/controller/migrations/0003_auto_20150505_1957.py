# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controller', '0002_auto_20150505_1948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskdependency',
            name='task',
            field=models.CharField(max_length=200),
        ),
    ]
