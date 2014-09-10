# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
import services.custom_fields


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0012_auto_20140910_1622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicesubscriptionpayment',
            name='amount',
            field=services.custom_fields.CurrencyField(verbose_name='cost', max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='service',
            name='amount',
            field=services.custom_fields.CurrencyField(verbose_name='amount', max_digits=10, decimal_places=4),
        ),
    ]
