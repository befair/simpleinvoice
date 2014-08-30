# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0007_auto_20140829_2238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicesubscriptionpayments',
            name='paid_for',
            field=models.DateTimeField(help_text='For what has he paid? (incremental value). Leave 0 to use default', verbose_name='paid for', choices=[(datetime.date(2015, 1, 1), b'01/01/2015'), (datetime.date(2016, 1, 1), b'01/01/2016'), (datetime.date(2017, 1, 1), b'01/01/2017'), (datetime.date(2018, 1, 1), b'01/01/2018'), (datetime.date(2019, 1, 1), b'01/01/2019'), (datetime.date(2020, 1, 1), b'01/01/2020'), (datetime.date(2021, 1, 1), b'01/01/2021'), (datetime.date(2022, 1, 1), b'01/01/2022'), (datetime.date(2023, 1, 1), b'01/01/2023'), (datetime.date(2024, 1, 1), b'01/01/2024'), (datetime.date(2025, 1, 1), b'01/01/2025'), (datetime.date(2026, 1, 1), b'01/01/2026'), (datetime.date(2027, 1, 1), b'01/01/2027'), (datetime.date(2028, 1, 1), b'01/01/2028'), (datetime.date(2029, 1, 1), b'01/01/2029'), (datetime.date(2030, 1, 1), b'01/01/2030'), (datetime.date(2031, 1, 1), b'01/01/2031'), (datetime.date(2032, 1, 1), b'01/01/2032'), (datetime.date(2033, 1, 1), b'01/01/2033'), (datetime.date(2034, 1, 1), b'01/01/2034'), (datetime.date(2035, 1, 1), b'01/01/2035')]),
        ),
    ]
