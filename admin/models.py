from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.sites.models import Site
from django.contrib import admin
from django import forms

from invoice.models import CustomerContact, Invoice, InvoiceEntry, Customer

class InvoiceEntryInline(admin.TabularInline):
    model = InvoiceEntry
    extra = 3

class InvoiceForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        """real_id is not editable if set"""
        super(InvoiceForm, self).__init__(*args, **kwargs)
        if kwargs.has_key('instance') and kwargs['instance'].real_id:
            self.fields['real_id'].widget.attrs['readonly'] = "readonly"

    class Meta:
        model = Invoice

class InvoiceAdmin(admin.ModelAdmin):

    form = InvoiceForm

    fieldsets = (
        (None, {
            'fields' : ('real_id', 
                        ('customer','date'),
                        'is_valid', ('pay_with', 'when_paid')
            )
        }),
    )

    list_display = ('id', 'real_id', 'date', 'customer', 'is_paid', 'is_valid', 'amount')
    list_display_links = ('id', 'real_id',)
    list_filter = ['customer','is_valid','when_paid']
    search_fields = ['real_id', 'customer', 'date']

    inlines = [InvoiceEntryInline]
    save_on_top = True

class CustomerContactInline(admin.TabularInline): 
	model = CustomerContact
	extra = 3

class CustomerContactAdmin(admin.ModelAdmin):
    list_display = ('__unicode__',)
    list_display_links = ('__unicode__',)
    search_fields = ('customer__name',)
    ordering = ('customer',)

class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer

    def clean(self):

        if not self.cleaned_data['ssn'] and not self.cleaned_data['vat']:
            raise forms.ValidationError(_("You should write social security or vat number"))
        return self.cleaned_data

class CustomerAdmin(admin.ModelAdmin):

    form = CustomerForm

    fieldsets = (
        (None, {
            'fields' : ('name', 'address',
                        ('zipcode','city','state'),
                        'ssn','vat',
            )
        }), (_('More info...'), { 'fields' : ('notes',), 'classes' : ('collapse',) }
        ),
    )

    list_display = ('name', 'address', 'city', 'notes')
    list_display_links = ('name',)
    list_filter = []
    search_fields = ['name']

    inlines = [CustomerContactInline]

site_admin = admin.AdminSite()
site_admin.register(Customer, CustomerAdmin)	
site_admin.register(Invoice, InvoiceAdmin)	

