# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20150408_1159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repeat',
            name='month',
            field=models.CharField(max_length=200, verbose_name=b'e.g. monthly'),
            preserve_default=True,
        ),
    ]
