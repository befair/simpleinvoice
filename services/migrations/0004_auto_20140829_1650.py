# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0003_auto_20140829_1235'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicesubscription',
            name='when_deleted',
            field=models.DateTimeField(null=True, verbose_name='when deleted', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='servicesubscription',
            name='is_deleted',
            field=models.BooleanField(default=False, verbose_name=b'is deleted'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='servicesubscriptionpayments',
            name='subscription',
            field=models.ForeignKey(default=0, verbose_name='subscription', to_field='id', to='services.ServiceSubscription'),
            preserve_default=False,
        ),
        #migrations.RemoveField(
        #    model_name='servicesubscriptionpayments',
        #    name='service',
        #),
        migrations.AlterUniqueTogether(
            name='servicesubscriptionpayments',
            unique_together=set([(b'subscription', b'paid_for')]),
        ),
    ]
    
