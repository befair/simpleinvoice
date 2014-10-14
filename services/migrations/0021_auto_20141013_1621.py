# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0020_servicesubscriptionpayment_invoice'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicesubscriptionpayment',
            name='when_paid',
            field=models.DateField(default=None, null=True, verbose_name='when paid', db_index=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='servicesubscriptionpayment',
            name='pay_with',
            field=models.CharField(default=b'money transfer', choices=[(b'money transfer', 'money transfer'), (b'cash', 'cash'), (b'credit card', 'credit card')], max_length=32, blank=True, null=True, verbose_name='pay with'),
            preserve_default=True,
        ),
    ]
