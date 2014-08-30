# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0008_auto_20140829_2247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicesubscriptionpayments',
            name='paid_for',
            field=models.DateTimeField(help_text='For what has he paid? (incremental value). Leave 0 to use default', verbose_name='paid for', choices=[(datetime.datetime(2015, 1, 1, 0, 0), b'01/01/2015'), (datetime.datetime(2016, 1, 1, 0, 0), b'01/01/2016'), (datetime.datetime(2017, 1, 1, 0, 0), b'01/01/2017'), (datetime.datetime(2018, 1, 1, 0, 0), b'01/01/2018'), (datetime.datetime(2019, 1, 1, 0, 0), b'01/01/2019'), (datetime.datetime(2020, 1, 1, 0, 0), b'01/01/2020'), (datetime.datetime(2021, 1, 1, 0, 0), b'01/01/2021'), (datetime.datetime(2022, 1, 1, 0, 0), b'01/01/2022'), (datetime.datetime(2023, 1, 1, 0, 0), b'01/01/2023'), (datetime.datetime(2024, 1, 1, 0, 0), b'01/01/2024'), (datetime.datetime(2025, 1, 1, 0, 0), b'01/01/2025'), (datetime.datetime(2026, 1, 1, 0, 0), b'01/01/2026'), (datetime.datetime(2027, 1, 1, 0, 0), b'01/01/2027'), (datetime.datetime(2028, 1, 1, 0, 0), b'01/01/2028'), (datetime.datetime(2029, 1, 1, 0, 0), b'01/01/2029'), (datetime.datetime(2030, 1, 1, 0, 0), b'01/01/2030'), (datetime.datetime(2031, 1, 1, 0, 0), b'01/01/2031'), (datetime.datetime(2032, 1, 1, 0, 0), b'01/01/2032'), (datetime.datetime(2033, 1, 1, 0, 0), b'01/01/2033'), (datetime.datetime(2034, 1, 1, 0, 0), b'01/01/2034'), (datetime.datetime(2035, 1, 1, 0, 0), b'01/01/2035')]),
        ),
        migrations.AlterField(
            model_name='servicesubscription',
            name='last_paid_for',
            field=models.DateTimeField(null=True, verbose_name='paid for', blank=True),
        ),
        migrations.AlterField(
            model_name='servicesubscription',
            name='subscribed_until',
            field=models.DateTimeField(blank=True, null=True, verbose_name='subscribed until', choices=[(datetime.datetime(2015, 1, 1, 0, 0), b'01/01/2015'), (datetime.datetime(2016, 1, 1, 0, 0), b'01/01/2016'), (datetime.datetime(2017, 1, 1, 0, 0), b'01/01/2017'), (datetime.datetime(2018, 1, 1, 0, 0), b'01/01/2018'), (datetime.datetime(2019, 1, 1, 0, 0), b'01/01/2019'), (datetime.datetime(2020, 1, 1, 0, 0), b'01/01/2020'), (datetime.datetime(2021, 1, 1, 0, 0), b'01/01/2021'), (datetime.datetime(2022, 1, 1, 0, 0), b'01/01/2022'), (datetime.datetime(2023, 1, 1, 0, 0), b'01/01/2023'), (datetime.datetime(2024, 1, 1, 0, 0), b'01/01/2024'), (datetime.datetime(2025, 1, 1, 0, 0), b'01/01/2025'), (datetime.datetime(2026, 1, 1, 0, 0), b'01/01/2026'), (datetime.datetime(2027, 1, 1, 0, 0), b'01/01/2027'), (datetime.datetime(2028, 1, 1, 0, 0), b'01/01/2028'), (datetime.datetime(2029, 1, 1, 0, 0), b'01/01/2029'), (datetime.datetime(2030, 1, 1, 0, 0), b'01/01/2030'), (datetime.datetime(2031, 1, 1, 0, 0), b'01/01/2031'), (datetime.datetime(2032, 1, 1, 0, 0), b'01/01/2032'), (datetime.datetime(2033, 1, 1, 0, 0), b'01/01/2033'), (datetime.datetime(2034, 1, 1, 0, 0), b'01/01/2034'), (datetime.datetime(2035, 1, 1, 0, 0), b'01/01/2035')]),
        ),
    ]
