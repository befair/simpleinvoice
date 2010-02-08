from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
import datetime

from django.conf import settings

class Company(object):

    vat_percent = settings.COMPANY_VAT_PERCENT
    vat_amount = vat_percent*100
    name = settings.COMPANY_NAME
    inet_contacts = settings.COMPANY_INTERNET_CONTACTS
    address = settings.COMPANY_ADDRESS
    contacts = settings.COMPANY_CONTACTS
    vat_number = settings.COMPANY_VAT_NUMBER

company = Company()

class Customer(models.Model):
    """Customer to emit the invoice to"""

    name = models.CharField(_('name'), max_length=256, blank=False)

    address = models.CharField(_('address'), max_length=128, blank=True, null=True, default='')
    zipcode = models.CharField(_('zipcode'), max_length=16, blank=True, null=True, default='')
    city = models.CharField(_('city'), max_length=64, blank=True, null=True, default='')
    state = models.CharField(_('state'), max_length=64, blank=True, null=True, default='')

    ssn = models.CharField(_('social security number'), max_length=50, blank=True, null=True, default='')
    vat = models.CharField(_('vat'), max_length=50, blank=True, null=True, default='')

    notes = models.TextField(_('notes'), blank=True, null=True, default='')

    def __unicode__(self):
        return self.name

    def is_debtor(self):
        return self.invoice_set.filter(when_paid__isnull=True).count()
    is_debtor.boolean = True

    class Meta:
        verbose_name = _('customer')
        verbose_name_plural = _("customers")

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
    
    def __unicode__(self):
        return u"%s %s: %s" % (self.customer, self.flavour, self.value)

    class Meta:
        verbose_name = _('customer contact')
        verbose_name_plural = _('customer contacts')

class InvoiceSequence(models.Model):
    """This is a sequence used simply to provide a right default value
    for new invoice id, avoiding the ugly save-twice algorithm
    used in previous Invoice.save() implementation"""

    # TODO
    pass

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
        ('money transfer', _('money transfer')),
        ('cash', _('cash')),
        ('credit card', _('credit card')),
    )

    real_id = models.CharField(_('invoice number'), max_length=16, default='', null=False, blank=True, help_text=_("Set this value only if you need a specific invoice number. After you save an invoice with a number you cannot modify it. You can always invalidate the invoice though"), unique=True)
    customer = models.ForeignKey(Customer)
    date = models.DateField(_("emit date"), default=datetime.date.today)	
    is_valid = models.BooleanField(_('is valid'), default=True, help_text=_("You can invalidate this invoice by unchecking this field"))
    pay_with = models.CharField(_('pay with'), max_length=32, choices=PAY_CHOICES, default=PAY_CHOICES[0][0])
    # redundant.. is_paid = models.BooleanField(_('is paid'), default=False, help_text=_("Check this whenever an invoice is paid"))
    when_paid = models.DateField(_("when paid"), null=True, default=None, blank=True)	

    def __unicode__(self):
        return u"%s %s %s (%s)" % (self.real_id, _('of'), self.date, self.customer)

    @property
    def amount(self):
        return self.entries.sum('amount') or 0

    @property
    def vat_amount(self):
        return int(self.amount * company.vat_percent)

    @property
    def tot_to_pay(self):
        return self.amount + self.vat_amount

    def is_paid(self):
        return bool(self.when_paid)
    is_paid.boolean = True

    def save(self):
        """Manage real_id:
        * set invoice real_id if not set before
        * set id (autofield) to a negative value if real id was set
        ugly: save the same object twice ! 
        """

        rv = super(Invoice, self).save()
        if not self.real_id:
            self.real_id = str(self.id)
            rv = super(Invoice, self).save()
        elif self.id > 0 and (str(self.id) != self.real_id):
            self.delete()
            if Invoice.objects.filter(id__lt=0).count():
                self.id = Invoice.objects.filter(id__lt=0).order_by('id')[0].id - 1
            else:
                self.id = -1
            rv = super(Invoice, self).save()
        return rv    

    class Meta:
        verbose_name = _("invoice")
        verbose_name_plural = _("invoices")
        ordering = ['date']

class InvoiceEntryManager(models.Manager):

    def sum(self, field_name):
        rv = 0
        for x in self.get_query_set().values_list(field_name):
            rv += x[0]
        return rv

class InvoiceEntry(models.Model):
    """Invoice single entry"""

    invoice = models.ForeignKey(Invoice, related_name="entries")
    amount = models.IntegerField()
    description = models.TextField()

    objects = InvoiceEntryManager()

    def __unicode__(self):
        return u"%5s: %s" % (self.amount, self.description)

    class Meta:
        verbose_name = _("invoice entry")
        verbose_name_plural = _("invoice entries")

