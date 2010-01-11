from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
import datetime

class Customer(models.Model):
    """Customer to emit the invoice to"""

    name = models.CharField(_('name'), max_length=256, blank=False)

    address = models.CharField(_('address'), max_length=128, blank=True, null=True, default='')
    zipcode = models.CharFiled(_('zipcode'), max_length=16, blank=True, null=True, default='')
    city = models.CharField(_('city'), max_length=64, blank=True, null=True, default='')
    state = models.CharField(_('state'), max_length=64, blank=True, null=True, default='')

    ssn = models.CharField(_('social security number'), max_length=50, blank=True, null=True, default='')
    vat = models.CharField(_('vat'), max_length=50, blank=True, null=True, default='')

    notes = models.TextField(_('notes'), blank=True, null=True, default='')

    def __unicode__(self):
        return self.name

    @property
    def is_debtor(self):
        return self.invoice_set.filter(is_paid=False).count()

    class Meta:
        verbose_name = _('customer')

class CustomerContact(models.Model):
    """Customer contacts: 
    each record holds a contact for a customer,
    along with the corresponding type"""

    FLAVOUR_CHOICES = (
        ('phone', _('phone')),
        ('fax',_('fax')),
        ('email',_('email')),
        ('other',_('other')),
    )

    customer = models.ForeignKey(Customer)
    flavour = models.CharField(max_length=32, choices=FLAVOUR_CHOICES, default=FLAVOUR_CHOICES[0][0])
    value = models.CharField(max_length=512)
    
    class Meta:
        verbose_name = _('customer contact')

class Invoice(models.Model):
    """Invoice data:

    real_id is the invoice id given by the user. 
    If blank given, its default value is the corresponding auto id field. 
    It can be changed to an older id with /A /B etc. 
    If so, corresponding auto_id field is set to a negative value like
    -1000xx for xx/A , -2000xx for xx/B , -3000xx for xx/C and so on.

    In this way it is possible to fix user mistakes.
    """
    PAY_CHOICES = (
        ('aa', _('BONIFICO')),
        ('bb', _('CONTANTI')),
        ('credit card', _('credit card')),
    )

    real_id = models.CharField(_('invoice number'), default='', null=False, blank=True, help_text(_("Set this value only if you need a specific invoice number")), unique=True)
    customer = models.ForeignKey(Customer)
    date = models.DateField(_("emit date"), default=datetime.date.today)	
    is_valid = models.BooleanField(_('is valid'), default=True, help_text=_("You can invalidate this invoice by unchecking this field"))
    is_paid = models.BooleanField(_('is paid'), default=False, help_text=_("Check this whenever an invoice is paid by a customer"))
    pay_with = models.CharField(_('pay with'), choices=PAY_CHOICES, default=PAY_CHOICES[0][0])

    class Meta:
        verbose_name = _("invoice")

class InvoiceEntry(models.Model):
    """Invoice single entry"""

    invoice = models.ForeignKey(Invoice)
    amount = models.IntegerField()
    description = models.TextField()

    class Meta:
        verbose_name = _("invoice entry")

