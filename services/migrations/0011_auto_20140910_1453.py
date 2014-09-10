# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal
import services.custom_fields


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0010_auto_20140904_1105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='default_vat_percent',
            field=services.custom_fields.PercentageDecimalField(default=Decimal('0.22'), verbose_name='default vat percentage', max_digits=3, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='servicesubscription',
            name='vat_percent',
            field=services.custom_fields.PercentageDecimalField(default=Decimal('0.22'), verbose_name='VAT percentage', max_digits=3, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='servicesubscriptionpayment',
            name='vat_percent',
            field=services.custom_fields.PercentageDecimalField(default=Decimal('0.22'), verbose_name='VAT percentage', max_digits=3, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='service',
            name='period_deadline_modifier',
            field=models.IntegerField(default=0, help_text='indicator to modify the periodic payement deadline', verbose_name='period deadline modifier', blank=True),
        ),
        migrations.AlterField(
            model_name='servicesubscriptionpayment',
            name='discount',
            field=services.custom_fields.PercentageDecimalField(default=0, verbose_name='discount', max_digits=3, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='servicesubscription',
            name='discount',
            field=services.custom_fields.PercentageDecimalField(default=0, verbose_name='discount', max_digits=3, decimal_places=2, blank=True),
        ),
    ]
