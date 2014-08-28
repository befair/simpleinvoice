# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='period_deadline_modifier',
            field=models.IntegerField(help_text='indicator to modify the periodic payement deadline', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='servicesubscriptionpayments',
            name='paid_for',
            field=models.IntegerField(help_text='For what has he paid? (incremental value). Leave 0 to use default'),
        ),
    ]
