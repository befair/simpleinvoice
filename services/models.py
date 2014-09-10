from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from django.core.exceptions import ValidationError

from invoice.models import Customer
from services.managers import ServiceSubscriptionManager
from services.custom_fields import PercentageDecimalField, CurrencyField

from django.conf import settings
from decimal import Decimal
#import datetime
from functools import partial
import datetime, pytz
from django.utils import timezone


#--------------------------------------------------------------------------------
# Measures units constants.
# note: other UNIT_ could be Gigabytes, Terabytes

UNIT_DAYS = 'days'
UNIT_YEARS = 'years'
UNIT_MONTHS = 'months'
UNIT_HOURS = 'hours'
UNIT_SECONDS = 'seconds'
UNIT_CHOICES = (
    #(UNIT_SECONDS, _('Seconds')),
    (UNIT_MONTHS, _('Months')),
    (UNIT_HOURS, _('Hours')),
    (UNIT_DAYS, _('Days')),
    (UNIT_YEARS, _('Years')),
)

DATE_CHOICES = (
    (datetime.datetime(2010,1,1), '01/01/2010'),
    (datetime.datetime(2011,1,1), '01/01/2011'),
    (datetime.datetime(2012,1,1), '01/01/2012'),
    (datetime.datetime(2013,1,1), '01/01/2013'),
    (datetime.datetime(2014,1,1), '01/01/2014'),
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
    (UNIT_MONTHS, UNIT_SECONDS): partial(lambda x : x*2592000),
    (UNIT_HOURS, UNIT_SECONDS): partial(lambda x : x*3600),
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
        help_text=_('Indicator to modify the periodic payement deadline. This value has to be greater then -(period), and represents the relative numebr of period units (for instance, months) that should be considered to determine the final service payment deadline. So, if the period is of 12 months, and the modifier is set to -2, then the actual service payment deadline is computed as (12 + (-2) = 10) months. In the same way, a modifier of 2 chenges the deadline to (12 + 2 = 14) month. '),
        verbose_name=_("period deadline modifier"), default=0
    ) 
    period_unit_raw = models.CharField(max_length=16, default=UNIT_HOURS, 
        choices=UNIT_CHOICES, verbose_name=_("raw unit")
    )
    period_unit_display = models.CharField(null=False,max_length=16,
        help_text=_('display measure unit for period'),
        choices=UNIT_CHOICES, default=UNIT_MONTHS,verbose_name=_("period measure of unit")
    )
    period_unit_source = models.CharField(max_length=32, default="epoch_now",verbose_name=_("period unit source"))

    amount = CurrencyField(verbose_name=_("amount"))
    default_vat_percent = PercentageDecimalField(
        default=Decimal(str(settings.DEFAULT_VAT_PERCENT)),
        verbose_name=_("default vat percentage")
    )

    class Meta:

        verbose_name = _("Service")
        verbose_name_plural = _("Services")

    def __unicode__(self):
        return self.name

    def clean(self):
        """
        Custom clean method
        """

        self.period_deadline_modifier = self.period_deadline_modifier or 0
        if not (0 <= self.default_vat_percent <= 1):
            raise ValidationError(_('Vat has to be a percentage value'))

    def save(self, *args, **kw):

        self.full_clean()
        super(Service, self).save(*args, **kw)

    @property
    def period_in_base_units(self):

        if self.period_unit_source == SOURCES["TIME"]:
            # base units are seconds
            base_units_kind = UNIT_SECONDS
        else:
            raise NotImplementedError("TBD")

        return CONVERSION_UNIT_MAP[(self.period_unit_raw, base_units_kind)](self.period)

class ServiceSubscription(models.Model):
    """
    Map services offered to customers specifying subscription period,
    and some attributes specific to this subscription like discount or
    custom vat_percent.

    It is used by ServiceSubscriptionPayment as template for payment.
    """

    customer = models.ForeignKey(Customer,verbose_name=_("customer"))
    service = models.ForeignKey(Service,verbose_name=_("service"))

    vat_percent = PercentageDecimalField(
        default=Decimal(str(settings.DEFAULT_VAT_PERCENT)),
        verbose_name=_("VAT percentage")
    )

    discount = PercentageDecimalField(_("discount"), default=0, blank=True)

    invoice_period = models.IntegerField(null=True, blank=True,
        help_text=_('how many period lasts before creating an invoice?'),
        default=1,verbose_name=_("period")
    )

    subscribed_on = models.DateTimeField(null=True,verbose_name=_("subscribed on"))
    subscribed_until = models.DateTimeField(null=True,blank=True,choices=DATE_CHOICES,verbose_name=_("subscribed until")) 

    # ---- set starting subscription
    subscribed_from_dt = models.DateTimeField(
        null=True,verbose_name=_("subscribed from (datetime)"), blank=True
    )
    subscribed_from_value = models.IntegerField(
        null=True,verbose_name=_("subscribed from (value)"), blank=True
    )
    # ----

    note = models.TextField(blank=True,verbose_name=_("note"))

    created_on = models.DateTimeField(auto_now_add=True,verbose_name=_("created on"))
    last_update_on = models.DateTimeField(auto_now=True,verbose_name=_("updated on"))

    # last paid on and last_paid_for
    # could be also properties get by ServiceSubscriptionPayment model
    last_paid_on = models.DateTimeField(null=True,blank=True,verbose_name=_("paid on")) 
    last_paid_for = models.DateTimeField(null=True,blank=True,verbose_name=_("paid for")) 

    #If the subscription is deleted:
    #
    #    * the subscription will not be shown to the users
    #    * it will not be possible to create payements related to the subscription 
    #    service 
    is_deleted = models.BooleanField(default=False,verbose_name=("is deleted"))
    when_deleted = models.DateTimeField(null=True,blank=True,verbose_name=_("when deleted"))

    service_details = models.TextField(null=True,blank=True,verbose_name=_('service details'))
    howmany = models.IntegerField(null=True,blank=True,verbose_name=_('how many'),default=1)

    objects = ServiceSubscriptionManager()

    all_objects = models.Manager()

    class Meta:
        unique_together = (('customer', 'service', 'subscribed_on'),)
        verbose_name = _("Service subscription")
        verbose_name_plural = _("Service subscriptions")

    def __unicode__(self):
        return _("Subscription of %(customer)s to service %(service)s") % {
            'customer' : self.customer,
            'service' : self.service
        }

    def clean(self):
        """
        Custom clean method
        """

		# First implementation
        self.subscribed_from_dt = self.subscribed_on

        if not (0 <= self.discount <= 1):
            raise ValidationError(_('Discount has to be a percentage value'))
        if not (0 <= self.vat_percent <= 1):
            raise ValidationError(_('Vat has to be a percentage value'))

    def save(self, *args, **kw):

        self.full_clean()
        super(ServiceSubscription, self).save(*args, **kw)

    @property
    def discounted_price(self):
        """
        Compute discounted subscription quote.

        Discount is a percentage.
        """
        
        return self.service.amount * (1 - self.discount)

    @property
    def subscribed_on_localtime(self):
        return self.subscribed_on.astimezone(self.customer.timezone)

    @property
    def subscribed_from_dt_localtime(self):
        return self.subscribed_from_dt.astimezone(self.customer.timezone)

    @property
    def subscribed_from_display(self):
        if self.subscribed_from_dt:
            rv = self.subscribed_from_dt_localtime
        else:
            raise NotImplementedError("TBD, this could be also an integer...")
        return rv

    @property
    def expired(self):
        """
        Check if the subscription expiration date is prior to 
        the current date
        """
        if self.subscribed_until:
            return self.subscribed_until <= timezone.now()

    @property
    def periods_from_last_payment(self):
        """
        How many periods passed from last payment. If there is not any
        payment yet, subscription is used. 
        """

        if self.service.period_unit_source == SOURCES['TIME']:
            if not self.last_paid_for:
                sec_elapsed = (timezone.now() - self.subscribed_on).total_seconds()
            else:
                sec_elapsed = (timezone.now() - self.last_paid_for).total_seconds()

            if self.service.period_unit_raw == UNIT_MONTHS:
                return  Decimal(CONVERSION_UNIT_MAP[(UNIT_SECONDS, UNIT_MONTHS)](sec_elapsed)) \
                 / (self.service.period + self.service.period_deadline_modifier)
            elif self.service.period_unit_raw == UNIT_HOURS:
                return  Decimal(CONVERSION_UNIT_MAP[(UNIT_HOURS, UNIT_MONTHS)](sec_elapsed)) \
                 / (self.service.period + self.service.period_deadline_modifier)
            elif self.service.period_unit_raw == UNIT_SECONDS:
                return  Decimal(sec_elapsed) \
                 / (self.service.period + self.service.period_deadline_modifier)
        raise NotImplementedError("TBD")

    @property
    def next_payment_due(self):
        """
        Check if a subscription has been regularly payed, basing on the
        last payment expiry date registered into the subscription.
        """

        if self.expired or self.is_deleted:
            return False

        if self.service.period_unit_source == SOURCES['TIME']:
            return self.periods_from_last_payment > 1
        raise NotImplementedError("TBD")

    @property
    def topay_start_display(self):

        if self.last_paid_for:
            # This will be valid even if last_paid_for will be an integer
            rv = self.last_paid_for
        else:
            if self.service.period_unit_source == SOURCES['TIME']:
                rv = self.subscribed_from_display

            else:
                raise NotImplementedError("TBD")

        return rv

    @property
    def topay_end_display(self):
            
        base = self.topay_start_display

        if self.service.period_unit_source == SOURCES['TIME']:
            if self.service.period_unit_raw == UNIT_MONTHS:
                m = base.month + self.service.period
                if m > 12:
                    m = m % 12
                    y = base.year + 1
                d = base.day
                dt = timezone.datetime(y, m, d, tzinfo=base.tzinfo)
                rv = dt.astimezone(self.customer.timezone)
            elif self.service.period_unit_raw == UNIT_YEARS:
                y = base.year + self.service.period
                m = base.month
                d = base.day
                dt = timezone.datetime(y, m, d, tzinfo=base.tzinfo)
                rv = dt.astimezone(self.customer.timezone)
            elif self.service.period_unit_raw == UNIT_DAYS:
                t = datetime.timedelta(self.service.period)
                rv = base + t
        else:
            raise NotImplementedError("TBD")
        
        return rv


class ServiceSubscriptionPayment(models.Model):
    """
    """

    subscription = models.ForeignKey(ServiceSubscription,verbose_name=_("subscription"))

    amount = CurrencyField(verbose_name=_("cost"))
    vat_percent = PercentageDecimalField( 
        default=Decimal(str(settings.DEFAULT_VAT_PERCENT)),
        verbose_name=_("VAT percentage")
    )

    discount = PercentageDecimalField(_("discount"), default=0)

    paid_on = models.DateTimeField(auto_now_add=True, help_text=_('When has it been paid?'),verbose_name=_("paid on")) 
    #WAS: paid_for = models.IntegerField(help_text=_("For what has he paid? (incremental value). Leave 0 to use default"),verbose_name=_("paid for"))
    paid_for = models.DateTimeField(choices=DATE_CHOICES,help_text=_("What date has he paid until?"),verbose_name=_("paid for")) 

    note = models.TextField(blank=True,verbose_name=_("note"))

    class Meta:
        unique_together = (('subscription', 'paid_for'),)
        verbose_name = _("Service subscription payment")
        verbose_name_plural = _("Service subscription payments")

    def __unicode__(self):
        return _("Payment of %(customer)s to service %(service)s") % {
            'customer' : self.subscription.customer,
            'service' : self.subscription.service
        }

    def clean(self):
        """
        Custom clean method
        """

        if not (0 <= self.discount <= 1):
            raise ValidationError(_('Discount has to be a percentage value'))
        if not (0 <= self.vat_percent <= 1):
            raise ValidationError(_('Vat has to be a percentage value'))

    def save(self, *args, **kwargs):
        """
        Payment is not saved if corresponding subscription is deleted
        """

        if not self.subscription.is_deleted:
            self.full_clean()
            return super(ServiceSubscriptionPayment, self).save(*args,**kwargs)

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
    
