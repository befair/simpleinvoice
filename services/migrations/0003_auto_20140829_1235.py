# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0002_auto_20140828_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicesubscription',
            name='last_update_on',
            field=models.DateTimeField(auto_now=True, verbose_name='updated on'),
        ),
        migrations.AlterField(
            model_name='servicesubscription',
            name='note',
            field=models.TextField(verbose_name='note', blank=True),
        ),
        migrations.AlterField(
            model_name='servicesubscriptionpayments',
            name='service',
            field=models.ForeignKey(to='services.Service', to_field='id', verbose_name='service'),
        ),
        migrations.AlterField(
            model_name='servicesubscriptionpayments',
            name='amount',
            field=models.DecimalField(verbose_name='cost', max_digits=12, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='servicesubscription',
            name='vat_percent',
            field=models.DecimalField(default=Decimal('0.21'), verbose_name='VAT percentage', max_digits=3, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='servicesubscription',
            name='last_paid_on',
            field=models.DateTimeField(null=True, verbose_name='paid on', blank=True),
        ),
        migrations.AlterField(
            model_name='servicesubscriptionpayments',
            name='paid_on',
            field=models.DateTimeField(help_text='When has it been paid?', verbose_name='paid on', auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='servicesubscription',
            name='subscribed_on',
            field=models.DateTimeField(null=True, verbose_name='subscribed on'),
        ),
        migrations.AlterField(
            model_name='servicesubscriptionpayments',
            name='paid_for',
            field=models.IntegerField(help_text='For what has he paid? (incremental value). Leave 0 to use default', verbose_name='paid for'),
        ),
        migrations.AlterField(
            model_name='servicesubscription',
            name='last_paid_for',
            field=models.IntegerField(null=True, verbose_name='paid for', blank=True),
        ),
        migrations.AlterField(
            model_name='servicesubscription',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created on'),
        ),
        migrations.AlterField(
            model_name='servicesubscription',
            name='subscribed_until',
            field=models.DateTimeField(null=True, verbose_name='subscribed until', blank=True),
        ),
        migrations.AlterField(
            model_name='servicesubscription',
            name='service',
            field=models.ForeignKey(to='services.Service', to_field='id', verbose_name='service'),
        ),
        migrations.AlterField(
            model_name='servicesubscriptionpayments',
            name='customer',
            field=models.ForeignKey(to='invoice.Customer', to_field='id', verbose_name='customer'),
        ),
        migrations.AlterField(
            model_name='servicesubscription',
            name='invoice_period',
            field=models.IntegerField(default=1, help_text='how many period lasts before creating an invoice?', null=True, verbose_name='period', blank=True),
        ),
        migrations.AlterField(
            model_name='servicesubscription',
            name='customer',
            field=models.ForeignKey(to='invoice.Customer', to_field='id', verbose_name='customer'),
        ),
        migrations.AlterField(
            model_name='servicesubscriptionpayments',
            name='vat_percent',
            field=models.DecimalField(default=Decimal('0.21'), verbose_name='VAT percentage', max_digits=3, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='servicesubscriptionpayments',
            name='note',
            field=models.TextField(verbose_name='note', blank=True),
        ),
    ]
