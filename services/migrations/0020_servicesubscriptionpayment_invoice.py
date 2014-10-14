# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0019_auto_20140919_1401'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicesubscriptionpayment',
            name='invoice',
            field=models.ForeignKey(verbose_name='invoice', to_field='id', blank=True, to='invoice.Invoice', null=True),
            preserve_default=True,
        ),
    ]
