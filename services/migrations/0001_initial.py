# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('abbreviation', models.CharField(max_length=32, verbose_name='abbreviation')),
                ('name', models.CharField(max_length=256, verbose_name='name', db_index=True)),
                ('description', models.TextField(verbose_name='description')),
                ('period', models.IntegerField(help_text='indicator of a period by raw units.', verbose_name='period')),
                ('period_deadline_modifier', models.IntegerField(help_text='indicator to modify the periodic payement deadline', verbose_name='period deadline modifier', blank=True)),
                ('period_unit_raw', models.CharField(default=b'hours', max_length=16, verbose_name='raw unit', choices=[(b'months', 'Months'), (b'hours', 'Hours')])),
                ('period_unit_display', models.CharField(default=b'months', help_text='display measure unit for period', max_length=16, verbose_name='period measure of unit', choices=[(b'months', 'Months'), (b'hours', 'Hours')])),
                ('period_unit_source', models.CharField(default=b'epoch_now', max_length=32, verbose_name='period unit source')),
                ('amount', models.DecimalField(verbose_name='amount', max_digits=12, decimal_places=2)),
                ('default_vat_percent', models.DecimalField(default=Decimal('0.21'), verbose_name='default vat percentage', max_digits=3, decimal_places=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ServiceSubscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('customer', models.ForeignKey(to='invoice.Customer', to_field='id')),
                ('service', models.ForeignKey(to='services.Service', to_field='id')),
                ('vat_percent', models.DecimalField(default=Decimal('0.21'), max_digits=3, decimal_places=2)),
                ('discount', models.DecimalField(default=0, verbose_name='discount', max_digits=3, decimal_places=2)),
                ('invoice_period', models.IntegerField(default=1, help_text='how many period lasts before creating an invoice?', null=True, blank=True)),
                ('subscribed_on', models.DateTimeField(null=True)),
                ('subscribed_until', models.DateTimeField(null=True, blank=True)),
                ('note', models.TextField(blank=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('last_update_on', models.DateTimeField(auto_now=True)),
                ('last_paid_on', models.DateTimeField(null=True, blank=True)),
                ('last_paid_for', models.IntegerField(help_text='For what has he paid? (incremental value)', null=True, blank=True)),
            ],
            options={
                'unique_together': set([(b'customer', b'service', b'subscribed_on')]),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ServiceSubscriptionPayments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('customer', models.ForeignKey(to='invoice.Customer', to_field='id')),
                ('service', models.ForeignKey(to='services.Service', to_field='id')),
                ('amount', models.DecimalField(max_digits=12, decimal_places=2)),
                ('vat_percent', models.DecimalField(default=Decimal('0.21'), max_digits=3, decimal_places=2)),
                ('discount', models.DecimalField(default=0, verbose_name='discount', max_digits=3, decimal_places=2)),
                ('paid_on', models.DateTimeField(help_text='When has it been paid?', auto_now_add=True)),
                ('paid_for', models.IntegerField(help_text='For what has he paid? (incremental value). Leave 0 to use default')),
                ('note', models.TextField(blank=True)),
            ],
            options={
                'unique_together': set([(b'customer', b'service', b'paid_for')]),
            },
            bases=(models.Model,),
        ),
    ]
