# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20150409_1344'),
    ]

    operations = [
        migrations.AddField(
            model_name='repeat',
            name='name',
            field=models.CharField(default=b'', max_length=200, verbose_name=b'e.g. monthly'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='repeat',
            name='month',
            field=models.IntegerField(default=-1),
            preserve_default=True,
        ),
    ]
