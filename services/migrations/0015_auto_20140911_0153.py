# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import services.custom_fields


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0014_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='period_deadline_modifier',
            field=models.IntegerField(default=0, help_text='Indicator to modify the periodic payement deadline. This value has to be greater then -(period), and represents the relative numebr of period units (for instance, months) that should be considered to determine the final service payment deadline. So, if the period is of 12 months, and the modifier is set to -2, then the actual service payment deadline is computed as (12 + (-2) = 10) months. In the same way, a modifier of 2 chenges the deadline to (12 + 2 = 14) month. ', verbose_name='period deadline modifier', blank=True),
        ),
        migrations.AlterField(
            model_name='servicesubscription',
            name='discount',
            field=services.custom_fields.PercentageDecimalField(default=0, verbose_name='discount', max_digits=3, decimal_places=2, blank=True),
        ),
        migrations.AlterField(
            model_name='servicesubscription',
            name='subscribed_from_dt',
            field=models.DateTimeField(null=True, verbose_name='subscribed from (datetime)', blank=True),
        ),
        migrations.AlterField(
            model_name='servicesubscription',
            name='subscribed_from_value',
            field=models.IntegerField(null=True, verbose_name='subscribed from (value)', blank=True),
        ),
    ]
