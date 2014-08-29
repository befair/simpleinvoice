# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicesubscription',
            name='last_paid_for',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
