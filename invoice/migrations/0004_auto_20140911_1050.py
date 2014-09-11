# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0003_remove_customer_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoiceentry',
            name='vat_percent',
            field=models.DecimalField(default=Decimal('0.22'), max_digits=3, decimal_places=2),
        ),
    ]
