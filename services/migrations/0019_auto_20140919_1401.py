# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal
import services.custom_fields


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0018_auto_20140911_1809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='default_vat_percent',
            field=services.custom_fields.PercentageDecimalField(default=Decimal('0.21'), verbose_name='default vat percentage', max_digits=3, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='servicesubscriptionpayment',
            name='subscription',
            field=models.ForeignKey(verbose_name='subscription', to_field='id', blank=True, to='services.ServiceSubscription'),
        ),
        migrations.AlterField(
            model_name='servicesubscription',
            name='vat_percent',
            field=services.custom_fields.PercentageDecimalField(default=Decimal('0.21'), verbose_name='VAT percentage', max_digits=3, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='servicesubscriptionpayment',
            name='vat_percent',
            field=services.custom_fields.PercentageDecimalField(default=Decimal('0.21'), verbose_name='VAT percentage', max_digits=3, decimal_places=2),
        ),
    ]
