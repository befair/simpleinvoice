# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0005_auto_20140829_1659'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='servicesubscriptionpayments',
            name='service',
        ),
    ]
