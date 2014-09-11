# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256, verbose_name='name', db_index=True)),
                ('address', models.CharField(default=b'', max_length=128, null=True, verbose_name='address', blank=True)),
                ('zipcode', models.CharField(default=b'', max_length=16, null=True, verbose_name='zipcode', blank=True)),
                ('city', models.CharField(default=b'', max_length=64, null=True, verbose_name='city', blank=True)),
                ('state', models.CharField(default=b'', max_length=64, null=True, verbose_name='state', blank=True)),
                ('ssn', models.CharField(default=b'', max_length=50, null=True, verbose_name='social security number', blank=True)),
                ('vat', models.CharField(default=b'', max_length=50, null=True, verbose_name='vat', blank=True)),
                ('notes', models.TextField(default=b'', null=True, verbose_name='notes', blank=True)),
            ],
            options={
                'verbose_name': 'customer',
                'verbose_name_plural': 'customers',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CustomerContact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('flavour', models.CharField(default=b'phone', max_length=32, choices=[(b'phone', 'phone'), (b'fax', 'fax'), (b'email', 'email'), (b'other', 'other')])),
                ('value', models.CharField(max_length=512)),
                ('customer', models.ForeignKey(to='invoice.Customer')),
            ],
            options={
                'verbose_name': 'customer contact',
                'verbose_name_plural': 'customer contacts',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('real_id', models.CharField(default=b'', max_length=16, unique_for_year=b'date', blank=True, help_text='Set this value only if you need a specific invoice number.', verbose_name='invoice number', db_index=True)),
                ('date', models.DateField(default=datetime.date.today, verbose_name='emit date', db_index=True)),
                ('discount', models.DecimalField(default=0, verbose_name='discount', max_digits=3, decimal_places=2)),
                ('is_valid', models.BooleanField(default=True, help_text='You can invalidate this invoice by unchecking this field.', verbose_name='is valid')),
                ('pay_with', models.CharField(default=b'money transfer', max_length=32, verbose_name='pay with', choices=[(b'money transfer', 'money transfer'), (b'cash', 'cash'), (b'credit card', 'credit card')])),
                ('when_paid', models.DateField(default=None, null=True, verbose_name='when paid', db_index=True, blank=True)),
                ('customer', models.ForeignKey(verbose_name='customer', to='invoice.Customer')),
            ],
            options={
                'ordering': ['-date'],
                'get_latest_by': 'date',
                'verbose_name': 'invoice',
                'verbose_name_plural': 'invoices',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InvoiceEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.DecimalField(verbose_name='amount', max_digits=12, decimal_places=2)),
                ('description', models.TextField(verbose_name='description')),
                ('vat_percent', models.DecimalField(default=Decimal('0.21'), max_digits=3, decimal_places=2)),
                ('invoice', models.ForeignKey(related_name=b'entries', to='invoice.Invoice')),
            ],
            options={
                'verbose_name': 'invoice entry',
                'verbose_name_plural': 'invoice entries',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InvoiceSequence',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('next_invoice_id', models.PositiveIntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
