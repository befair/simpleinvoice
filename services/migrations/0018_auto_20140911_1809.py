# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0017_auto_20140911_1050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='period_deadline_modifier',
            field=models.IntegerField(default=0, help_text='Indicator to modify the periodic payment deadline. This value has to be greater than -(period), and represents the relative number of period units (for instance, months) that should be considered to determine the final service payment deadline. So, if the period is of 12 months, and the modifier is set to -2, then the actual service payment deadline is computed as (12 + (-2) = 10) months. In the same way, a modifier of 2 chenges the deadline to (12 + 2 = 14) month. ', verbose_name='period deadline modifier', blank=True),
        ),
    ]
