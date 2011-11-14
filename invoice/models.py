from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
import datetime

from django.conf import settings
from decimal import Decimal

class Company(object):

    name = settings.COMPANY_NAME
    inet_contacts = settings.COMPANY_INTERNET_CONTACTS
    address = settings.COMPANY_ADDRESS
    contacts = settings.COMPANY_CONTACTS
    vat_number = settings.COMPANY_VAT_NUMBER
    iban = settings.COMPANY_IBAN

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
    for new invoice id, when an invoice is saved, 
    its real_id is checked and, if its integer part is equal or greater than next_invoice_id
    this value is updated"""

    next_invoice_id = models.PositiveIntegerField()

    @classmethod
    def get(cls, invoice):
        """Get next sequence id and increment.
        When new year comes, cycle id and start by 1 again"""
        date = invoice.date
        seq = cls.objects.get(pk=1)
        
        try:
            last_invoice_date = Invoice.objects.latest().date
        except Invoice.DoesNotExist:
            last_invoice_date = datetime.datetime.today()

        if date.year - last_invoice_date.year >= 1:
            rv = 1
        else:
            rv = seq.next_invoice_id

        seq.next_invoice_id = rv + 1
        seq.save()
        return rv

    @classmethod
    def update(cls, invoice):
        """Update next_invoice_id if necessary"""
        real_id = invoice.real_id
        i = 1
        int_real_id = 0
        while i <= len(real_id):
            try:
                int_real_id = int(real_id[:i])
                i += 1
            except ValueError:
                "Ok int part retrieved"
                break

        if int_real_id >= cls.objects.get(pk=1).next_invoice_id:
            cls.get(invoice)

        return True
            
    def __unicode__(self):
        return _("Next invoice id is %s") % self.next_invoice_id

class Invoice(models.Model):
    """Invoice data:

    real_id is the invoice id given by the user. 
    If blank given, its default value is get from InvoiceSequence
    It can be changed to an older id with /A /B etc. 

    In this way it is possible to fix user mistakes.
    """
    PAY_CHOICES = (
        ('money transfer', _('money transfer')),
        ('cash', _('cash')),
        ('credit card', _('credit card')),
    )

    real_id = models.CharField(_('invoice number'), max_length=16, default='', null=False, blank=True, help_text=_("Set this value only if you need a specific invoice number."), unique_for_year="date")
    customer = models.ForeignKey(Customer)
    date = models.DateField(_("emit date"), default=datetime.date.today)	
    discount = models.FloatField(_("discount"), default=0)
    is_valid = models.BooleanField(_('is valid'), default=True, help_text=_("You can invalidate this invoice by unchecking this field."))
    pay_with = models.CharField(_('pay with'), max_length=32, choices=PAY_CHOICES, default=PAY_CHOICES[0][0])
    # redundant.. is_paid = models.BooleanField(_('is paid'), default=False, help_text=_("Check this whenever an invoice is paid"))
    when_paid = models.DateField(_("when paid"), null=True, default=None, blank=True)	

    class Meta:
        verbose_name = _("invoice")
        verbose_name_plural = _("invoices")
        ordering = ['date']
        get_latest_by = "date"

    def __unicode__(self):
        return u"%s %s %s (%s)" % (self.real_id, _('of'), self.date, self.customer)

    @property
    def pre_amount(self):
        return self.entries.sum('amount') or 0

    @property
    def amount(self):
        return self.pre_amount*(1-self.discount)

    @property
    def vat_amount(self):
        return self.entries.vat_amount()

    @property
    def tot_to_pay(self):
        rv = self.amount + float(self.vat_amount)
        return rv

    def is_paid(self):
        return bool(self.when_paid)
    is_paid.boolean = True

    def save(self):
        """Manage real_id:
        * if not set: get from InvoiceSequence
        * if set: update InvoiceSequence if needed
        """

        if not self.real_id:
           self.real_id = str(InvoiceSequence.get(self))
        else:
           InvoiceSequence.update(self)
        
        return super(Invoice, self).save()

class InvoiceEntryManager(models.Manager):

    def sum(self, field_name):
        rv = 0
        for x in self.get_query_set().values_list(field_name):
            rv += x[0]
        return rv

    def amount(self):
        return self.sum('amount')

    def vat_amount(self):
        rv = 0
        for x in self.get_query_set().values_list('amount', 'vat_percent'):
            rv += x[0]*x[1]
        return rv

class InvoiceEntry(models.Model):
    """Invoice single entry"""

    invoice = models.ForeignKey(Invoice, related_name="entries")
    amount = models.IntegerField()
    description = models.TextField()
    vat_percent = models.DecimalField(max_digits=3, decimal_places=2, 
        default=Decimal(str(settings.DEFAULT_VAT_PERCENT))
    )

    objects = InvoiceEntryManager()

    def __unicode__(self):
        return u"%5s: %s" % (self.amount, self.description)

    class Meta:
        verbose_name = _("invoice entry")
        verbose_name_plural = _("invoice entries")

