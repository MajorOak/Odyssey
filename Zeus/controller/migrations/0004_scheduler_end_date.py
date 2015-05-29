# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controller', '0003_auto_20150505_1957'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheduler',
            name='end_date',
            field=models.DateTimeField(null=True, verbose_name=b'end date this run'),
        ),
    ]
