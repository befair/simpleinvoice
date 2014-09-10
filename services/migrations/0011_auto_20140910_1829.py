# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0010_auto_20140904_1105'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicesubscription',
            name='subscribed_from_value',
            field=models.IntegerField(null=True, verbose_name='subscribed from (value)'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='servicesubscription',
            name='subscribed_from_dt',
            field=models.DateTimeField(null=True, verbose_name='subscribed from (datetime)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='service',
            name='period_unit_display',
            field=models.CharField(default=b'months', help_text='display measure unit for period', max_length=16, verbose_name='period measure of unit', choices=[(b'months', 'Months'), (b'hours', 'Hours'), (b'days', 'Days'), (b'years', 'Years')]),
        ),
        migrations.AlterField(
            model_name='service',
            name='period_unit_raw',
            field=models.CharField(default=b'hours', max_length=16, verbose_name='raw unit', choices=[(b'months', 'Months'), (b'hours', 'Hours'), (b'days', 'Days'), (b'years', 'Years')]),
        ),
        migrations.AlterField(
            model_name='service',
            name='period_deadline_modifier',
            field=models.IntegerField(default=0, help_text='indicator to modify the periodic payement deadline', verbose_name='period deadline modifier', blank=True),
        ),
        migrations.AlterField(
            model_name='servicesubscription',
            name='discount',
            field=models.DecimalField(default=0, verbose_name='discount', max_digits=3, decimal_places=2, blank=True),
        ),
    ]
