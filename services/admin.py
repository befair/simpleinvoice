from django.contrib import admin
from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from django.core.mail import send_mail
from services import models as services
from services.models import Service, ServiceSubscription, ServiceSubscriptionPayments
from django import forms

class ServiceAdmin(admin.ModelAdmin): 

    list_display = ('name', 'description', 'period_unit_display', 'amount')
    search_fields = ['name']

    exclude = ('period_unit_source',)

    class Media:
        css = {
            'all' : ('adminstyle.css',),
        }

class ServiceSubscriptionAdmin(admin.ModelAdmin): 

    list_display = ('customer', 'service', 'subscribed_on', 'subscribed_until', 'note')
    search_fields = ['customer']

    actions = ['check_payement']

    def check_payement(self, request, queryset):
        """
        Check if the selected subscriptions fees have already been payed.

        The subscription last payement date (or quantity) is compared with
        the current time (or consumed quantity) and if the difference is 
        higher than the next period (or period quantity) then a remind 
        mail is sent to the corresponding customer 
        
        """

        for obj in queryset:
            if obj.next_payment_due is True:
                subject = 'payement due'
                message = "Hi %s, we inform you that you have not paid the amount of %s euro for the periodic service %s" % (obj.customer.name,obj.service.amount,obj.service.name)
                sender = 'admin@admin.it'
                receivers = [obj.customer.name]
                send_mail(subject, message, sender, receivers, fail_silently=False) 
    check_payement.short_description = _("Check if selected subscription are paid")

    class Media:
        css = {
            'all' : ('adminstyle.css',),
        }

class PayementForm(forms.ModelForm):
    """
    This customized form values the ServiceSubscriptionPayement 'paid_for'
    field: if this field is not changed with a custom value, the default 
    Service period is used instead.
    """

    def __init__(self, *args, **kwargs):
        super(PayementForm, self).__init__(*args, **kwargs)
        self.fields['paid_for'].initial = '0'

    def save(self, commit=True):
        instance = super(PayementForm, self).save(commit=False)
        if self.cleaned_data['paid_for'] is 0:
            service = self.cleaned_data['service']
            instance = self.instance
            if service.period_unit_raw == services.UNIT_MONTHS:
                instance.paid_for = 1
            elif service.period_unit_raw == services.UNIT_HOURS:
                instance.paid_for = 720
            elif service.period_unit_raw == services.UNIT_SECONDS:
                instance.paid_for = 2592000
        if commit:
            instance.save()
        return instance


    class Meta:
        model = ServiceSubscriptionPayments

class ServiceSubscriptionPayementsAdmin(admin.ModelAdmin): 

    form = PayementForm
    
    list_display = ('customer', 'service', 'amount', 'paid_on','note')
    search_fields = ['customer','service']


    class Media:
        css = {
            'all' : ('adminstyle.css',),
        }

admin.site.register(Service, ServiceAdmin)	
admin.site.register(ServiceSubscription, ServiceSubscriptionAdmin)	
admin.site.register(ServiceSubscriptionPayments, ServiceSubscriptionPayementsAdmin)	
