# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_remove_task_date_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name=b'Date created', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='task',
            name='schedules',
            field=models.ManyToManyField(to='main.Schedule'),
            preserve_default=True,
        ),
    ]
