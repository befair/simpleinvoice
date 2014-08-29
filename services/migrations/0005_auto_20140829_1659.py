# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0004_auto_20140829_1650'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='servicesubscriptionpayments',
            name='customer',
        ),
        migrations.AlterUniqueTogether(
            name='servicesubscriptionpayments',
            unique_together=set([(b'subscription', b'paid_for')]),
        ),
    ]
