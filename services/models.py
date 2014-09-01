from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _

from invoice.models import Customer
from services.managers import ServiceSubscriptionManager

from django.conf import settings
from decimal import Decimal
#import datetime
from functools import partial
import datetime
from django.utils import timezone

#--------------------------------------------------------------------------------
# Measures units constants.
# note: other UNIT_ could be Gigabytes, Terabytes

UNIT_MONTHS = 'months'
UNIT_HOURS = 'hours'
UNIT_SECONDS = 'seconds'
UNIT_CHOICES = (
    #(UNIT_SECONDS, _('Seconds')),
    (UNIT_MONTHS, _('Months')),
    (UNIT_HOURS, _('Hours')),
)

DATE_CHOICES = (
    (datetime.datetime(2015,1,1), '01/01/2015'),
    (datetime.datetime(2016,1,1), '01/01/2016'),
    (datetime.datetime(2017,1,1), '01/01/2017'),
    (datetime.datetime(2018,1,1), '01/01/2018'),
    (datetime.datetime(2019,1,1), '01/01/2019'),
    (datetime.datetime(2020,1,1), '01/01/2020'),
    (datetime.datetime(2021,1,1), '01/01/2021'),
    (datetime.datetime(2022,1,1), '01/01/2022'),
    (datetime.datetime(2023,1,1), '01/01/2023'),
    (datetime.datetime(2024,1,1), '01/01/2024'),
    (datetime.datetime(2025,1,1), '01/01/2025'),
    (datetime.datetime(2026,1,1), '01/01/2026'),
    (datetime.datetime(2027,1,1), '01/01/2027'),
    (datetime.datetime(2028,1,1), '01/01/2028'),
    (datetime.datetime(2029,1,1), '01/01/2029'),
    (datetime.datetime(2030,1,1), '01/01/2030'),
    (datetime.datetime(2031,1,1), '01/01/2031'),
    (datetime.datetime(2032,1,1), '01/01/2032'),
    (datetime.datetime(2033,1,1), '01/01/2033'),
    (datetime.datetime(2034,1,1), '01/01/2034'),
    (datetime.datetime(2035,1,1), '01/01/2035'),
)

# Conversion table map. Use "partial" because we cannot lambda (":") in dict values

CONVERSION_UNIT_MAP = {
    (UNIT_HOURS, UNIT_MONTHS): partial(lambda x : x/720),
    (UNIT_SECONDS, UNIT_MONTHS): partial(lambda x : x/2592000),
}

# A source define the unite of measure chose for a subsription (time, MB, etc. )

SOURCES = {
    'TIME' : 'epoch_now',
}

#--------------------------------------------------------------------------------


class Service(models.Model):
    """
    Kind of periodic service offered. I.e:

    * Quota annuale associativa
    * Quota annuale mailing-list    

    but it could be also:

    * N gigabytes of traffic
    
    """

    abbreviation = models.CharField(max_length=32,verbose_name=_("abbreviation")) 
    name = models.CharField(max_length=256, db_index=True,verbose_name=_("name"))
    description = models.TextField(verbose_name=_("description"))
    period = models.IntegerField(help_text=_('indicator of a period by raw units.'),
        verbose_name=_("period")
    )
    period_deadline_modifier=models.IntegerField(blank=True,
        help_text=_('indicator to modify the periodic payement deadline'),
        verbose_name=_("period deadline modifier")
    ) 
    period_unit_raw = models.CharField(max_length=16, default=UNIT_HOURS, 
        choices=UNIT_CHOICES, verbose_name=_("raw unit")
    )
    period_unit_display = models.CharField(null=False,max_length=16,
        help_text=_('display measure unit for period'),
        choices=UNIT_CHOICES, default=UNIT_MONTHS,verbose_name=_("period measure of unit")
    )
    period_unit_source = models.CharField(max_length=32, default="epoch_now",verbose_name=_("period unit source"))

    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_("amount"))
    default_vat_percent = models.DecimalField(max_digits=3, decimal_places=2, 
        default=Decimal(str(settings.DEFAULT_VAT_PERCENT)), verbose_name=_("default vat percentage")
    )

    def __unicode__(self):
        return self.name

class ServiceSubscription(models.Model):
    """
    Map services offered to customers specifying subscription period,
    and some attributes specific to this subscription like discount or
    custom vat_percent.

    It is used by ServiceSubscriptionPayments as template for payment.
    """

    customer = models.ForeignKey(Customer,verbose_name=_("customer"))
    service = models.ForeignKey(Service,verbose_name=_("service"))

    vat_percent = models.DecimalField(max_digits=3, decimal_places=2, 
        default=Decimal(str(settings.DEFAULT_VAT_PERCENT)),verbose_name=_("VAT percentage")
    )

    discount = models.DecimalField(_("discount"), default=0, max_digits=3, decimal_places=2)

    invoice_period = models.IntegerField(null=True, blank=True,
        help_text=_('how many period lasts before creating an invoice?'),
        default=1,verbose_name=_("period")
    )

    subscribed_on = models.DateTimeField(null=True,verbose_name=_("subscribed on"))
    subscribed_until = models.DateTimeField(null=True,blank=True,choices=DATE_CHOICES,verbose_name=_("subscribed until")) 

    note = models.TextField(blank=True,verbose_name=_("note"))

    created_on = models.DateTimeField(auto_now_add=True,verbose_name=_("created on"))
    last_update_on = models.DateTimeField(auto_now=True,verbose_name=_("updated on"))

    # last paid on and last_paid_for
    # could be also properties get by ServiceSubscriptionPayments model
    last_paid_on = models.DateTimeField(null=True,blank=True,verbose_name=_("paid on")) 
    last_paid_for = models.DateTimeField(null=True,blank=True,verbose_name=_("paid for")) 

    #If the subscription is deleted:
    #
    #    * the subscription will not be shown to the users
    #    * it will not be possible to create payements related to the subscription 
    #    service 
    is_deleted = models.BooleanField(default=False,verbose_name=("is deleted"))
    when_deleted = models.DateTimeField(null=True,blank=True,verbose_name=_("when deleted"))


    all_objects = models.Manager()
        print "%s" % (cleaned_data)

    objects = ServiceSubscriptionManager()

    class Meta:
        unique_together = (('customer', 'service', 'subscribed_on'),)

    @property
    def discounted_price(self):
        """
        Compute discounted subscription quote.

        Discount is a percentage.
        """
        
        return self.service.amount * (1 - self.discount)

    @property
    def expired(self):
        """
        Check if the subscription expiration date is prior to 
        the current date
        """
        if self.subscribed_until:
            return self.subscribed_until <= timezone.now

    @property
    def next_payment_due(self):
        """
        Check if a subscription has been regularly payed, basing on the
        last payement registered into the subscription.

        There has not been any payement for the subscription, 
        """

        if self.expired or self.is_deleted:
            return False

        if not self.last_paid_on:
            return False

        if self.service.period_unit_source == SOURCES['TIME']:
            sec_elapsed = (timezone.now() - self.last_paid_on).total_seconds()
            tot_sec = (self.last_paid_for - self.last_paid_on).total_seconds()

            if self.service.period_unit_raw == UNIT_MONTHS:
                return  sec_elapsed > (tot_sec + (self.service.period_deadline_modifier * 30*24*60*60 ))
            elif self.service.period_unit_raw == UNIT_HOURS:
                return  sec_elapsed > (tot_sec + (self.service.period_deadline_modifier * 60*60))
            elif self.service.period_unit_raw == UNIT_SECONDS:
                return  sec_elapsed > (tot_sec + self.service.period_deadline_modifier)
        raise NotImplementedError("TBD")
        

class ServiceSubscriptionPayments(models.Model):
    """
    """

    subscription = models.ForeignKey(ServiceSubscription,verbose_name=_("subscription"))

    amount = models.DecimalField(max_digits=12, decimal_places=2,verbose_name=_("cost"))
    vat_percent = models.DecimalField(max_digits=3, decimal_places=2, 
        default=Decimal(str(settings.DEFAULT_VAT_PERCENT)),verbose_name=_("VAT percentage")
    )

    discount = models.DecimalField(_("discount"), default=0, max_digits=3, decimal_places=2)

    paid_on = models.DateTimeField(auto_now_add=True, help_text=_('When has it been paid?'),verbose_name=_("paid on")) 
    #WAS: paid_for = models.IntegerField(help_text=_("For what has he paid? (incremental value). Leave 0 to use default"),verbose_name=_("paid for"))
    paid_for = models.DateTimeField(choices=DATE_CHOICES,help_text=_("For what has he paid? (incremental value). Leave 0 to use default"),verbose_name=_("paid for")) 

    note = models.TextField(blank=True,verbose_name=_("note"))

    class Meta:
        unique_together = (('subscription', 'paid_for'),)

    @property
    def discounted_price(self):
        """
        Compute discounted subscription quote.

        Discount is a percentage.
        """
        
        return self.amount * (1 - self.discount)

    @property
    def paid_for_display(self):
        unit_raw = self.subscription.service.period_unit_raw
        unit_display = self.subscription.service.period_unit_display
        return CONVERSION_UNIT_MAP[(unit_raw, unit_display)](self.paid_for)
