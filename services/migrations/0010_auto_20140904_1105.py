# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0009_auto_20140830_1447'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceSubscriptionPayment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subscription', models.ForeignKey(to='services.ServiceSubscription', to_field='id', verbose_name='subscription')),
                ('amount', models.DecimalField(verbose_name='cost', max_digits=12, decimal_places=2)),
                ('vat_percent', models.DecimalField(default=Decimal('0.21'), verbose_name='VAT percentage', max_digits=3, decimal_places=2)),
                ('discount', models.DecimalField(default=0, verbose_name='discount', max_digits=3, decimal_places=2)),
                ('paid_on', models.DateTimeField(help_text='When has it been paid?', verbose_name='paid on', auto_now_add=True)),
                ('paid_for', models.DateTimeField(help_text='What date has he paid until?', verbose_name='paid for', choices=[(datetime.datetime(2010, 1, 1, 0, 0), b'01/01/2010'), (datetime.datetime(2011, 1, 1, 0, 0), b'01/01/2011'), (datetime.datetime(2012, 1, 1, 0, 0), b'01/01/2012'), (datetime.datetime(2013, 1, 1, 0, 0), b'01/01/2013'), (datetime.datetime(2014, 1, 1, 0, 0), b'01/01/2014'), (datetime.datetime(2015, 1, 1, 0, 0), b'01/01/2015'), (datetime.datetime(2016, 1, 1, 0, 0), b'01/01/2016'), (datetime.datetime(2017, 1, 1, 0, 0), b'01/01/2017'), (datetime.datetime(2018, 1, 1, 0, 0), b'01/01/2018'), (datetime.datetime(2019, 1, 1, 0, 0), b'01/01/2019'), (datetime.datetime(2020, 1, 1, 0, 0), b'01/01/2020'), (datetime.datetime(2021, 1, 1, 0, 0), b'01/01/2021'), (datetime.datetime(2022, 1, 1, 0, 0), b'01/01/2022'), (datetime.datetime(2023, 1, 1, 0, 0), b'01/01/2023'), (datetime.datetime(2024, 1, 1, 0, 0), b'01/01/2024'), (datetime.datetime(2025, 1, 1, 0, 0), b'01/01/2025'), (datetime.datetime(2026, 1, 1, 0, 0), b'01/01/2026'), (datetime.datetime(2027, 1, 1, 0, 0), b'01/01/2027'), (datetime.datetime(2028, 1, 1, 0, 0), b'01/01/2028'), (datetime.datetime(2029, 1, 1, 0, 0), b'01/01/2029'), (datetime.datetime(2030, 1, 1, 0, 0), b'01/01/2030'), (datetime.datetime(2031, 1, 1, 0, 0), b'01/01/2031'), (datetime.datetime(2032, 1, 1, 0, 0), b'01/01/2032'), (datetime.datetime(2033, 1, 1, 0, 0), b'01/01/2033'), (datetime.datetime(2034, 1, 1, 0, 0), b'01/01/2034'), (datetime.datetime(2035, 1, 1, 0, 0), b'01/01/2035')])),
                ('note', models.TextField(verbose_name='note', blank=True)),
            ],
            options={
                'unique_together': set([(b'subscription', b'paid_for')]),
                'verbose_name': 'Service subscription payment',
                'verbose_name_plural': 'Service subscription payments',
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='servicesubscription',
            name='subscribed_until',
            field=models.DateTimeField(blank=True, null=True, verbose_name='subscribed until', choices=[(datetime.datetime(2010, 1, 1, 0, 0), b'01/01/2010'), (datetime.datetime(2011, 1, 1, 0, 0), b'01/01/2011'), (datetime.datetime(2012, 1, 1, 0, 0), b'01/01/2012'), (datetime.datetime(2013, 1, 1, 0, 0), b'01/01/2013'), (datetime.datetime(2014, 1, 1, 0, 0), b'01/01/2014'), (datetime.datetime(2015, 1, 1, 0, 0), b'01/01/2015'), (datetime.datetime(2016, 1, 1, 0, 0), b'01/01/2016'), (datetime.datetime(2017, 1, 1, 0, 0), b'01/01/2017'), (datetime.datetime(2018, 1, 1, 0, 0), b'01/01/2018'), (datetime.datetime(2019, 1, 1, 0, 0), b'01/01/2019'), (datetime.datetime(2020, 1, 1, 0, 0), b'01/01/2020'), (datetime.datetime(2021, 1, 1, 0, 0), b'01/01/2021'), (datetime.datetime(2022, 1, 1, 0, 0), b'01/01/2022'), (datetime.datetime(2023, 1, 1, 0, 0), b'01/01/2023'), (datetime.datetime(2024, 1, 1, 0, 0), b'01/01/2024'), (datetime.datetime(2025, 1, 1, 0, 0), b'01/01/2025'), (datetime.datetime(2026, 1, 1, 0, 0), b'01/01/2026'), (datetime.datetime(2027, 1, 1, 0, 0), b'01/01/2027'), (datetime.datetime(2028, 1, 1, 0, 0), b'01/01/2028'), (datetime.datetime(2029, 1, 1, 0, 0), b'01/01/2029'), (datetime.datetime(2030, 1, 1, 0, 0), b'01/01/2030'), (datetime.datetime(2031, 1, 1, 0, 0), b'01/01/2031'), (datetime.datetime(2032, 1, 1, 0, 0), b'01/01/2032'), (datetime.datetime(2033, 1, 1, 0, 0), b'01/01/2033'), (datetime.datetime(2034, 1, 1, 0, 0), b'01/01/2034'), (datetime.datetime(2035, 1, 1, 0, 0), b'01/01/2035')]),
        ),
        migrations.DeleteModel(
            name='ServiceSubscriptionPayments',
        ),
    ]
