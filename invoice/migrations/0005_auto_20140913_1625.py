# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0004_auto_20140911_1050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoiceentry',
            name='vat_percent',
            field=models.DecimalField(default=Decimal('0.21'), max_digits=3, decimal_places=2),
        ),
    ]
