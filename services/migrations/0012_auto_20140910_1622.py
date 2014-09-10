# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0011_auto_20140910_1453'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicesubscription',
            name='service_details',
            field=models.TextField(null=True, verbose_name='service details', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='servicesubscription',
            name='howmany',
            field=models.IntegerField(default=1, null=True, verbose_name='how many', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='service',
            name='period_deadline_modifier',
            field=models.IntegerField(default=0, help_text='Indicator to modify the periodic payement deadline. This value has to be greater then -(period), and represents the relative numebr of period units (for instance, months) that should be considered to determine the final service payment deadline. So, if the period is of 12 months, and the modifier is set to -2, then the actual service payment deadline is computed as (12 + (-2) = 10) months. In the same way, a modifier of 2 chenges the deadline to (12 + 2 = 14) month. ', verbose_name='period deadline modifier', blank=True),
        ),
    ]
