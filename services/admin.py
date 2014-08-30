from django.contrib import admin
from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from django.core.mail import send_mail
from services import models as services
from services.models import Service, ServiceSubscription, ServiceSubscriptionPayments, DATE_CHOICES
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

    list_display = ('customer', 'service', 'subscribed_on', 'subscribed_until', 'note','is_deleted')
    search_fields = ['customer']

    actions = ['check_payment']
    
    exclude = ('last_paid_on','last_paid_for')

    def check_payment(self, request, queryset):
        """
        Check if the selected subscriptions fees have already been payed.

        The subscription last payment date (or quantity) is compared with
        the current time (or consumed quantity) and if the difference is 
        higher than the next period (or period quantity) then a remind 
        mail is sent to the corresponding customer 
        
        """

        for obj in queryset:
            if obj.next_payment_due is True:
                subject = 'payment due'
                message = "Hi %s, we inform you that you have not paid the amount of %s euro for the periodic service %s" % (obj.customer.name,obj.service.amount,obj.service.name)
                sender = 'admin@admin.it'
                receivers = [obj.customer.name]
                send_mail(subject, message, sender, receivers, fail_silently=False) 
    check_payment.short_description = _("Check if selected subscription are paid")

    class Media:
        css = {
            'all' : ('adminstyle.css',),
        }

class PaymentForm(forms.ModelForm):
    """
    This customized form values the ServiceSubscriptionPayment 'paid_for'
    field: if this field is not changed with a custom value, the default 
    Service period is used instead.
    """

    fields = forms.models.fields_for_model(ServiceSubscription,
        fields=['customer','service']
    )
    customer = fields.get('customer')
    service = fields.get('service')

    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        self.fields['paid_for'].initial = DATE_CHOICES[0][0]
    #    fields = forms.models.fields_for_model(ServiceSubscription,
    #        fields=['customer','service']
    #    )
    #    self.fields['customer'] = fields.get('customer')
    #    self.fields['service'] = fields.get('service')
    #    self.Meta.fields.append('customer')
    #    self.Meta.fields.append('service')

    def set_paid_for(self,service=None):
        """
        """
        if service:
            if service.period_unit_raw == services.UNIT_MONTHS:
                #instance.paid_for = 1
                paid_for = DATE_CHOICES[service.period/12][0]
            elif service.period_unit_raw == services.UNIT_HOURS:
                #instance.paid_for = 720
                paid_for = DATE_CHOICES[service.period/(360*24)][0]
            elif service.period_unit_raw == services.UNIT_SECONDS:
                #instance.paid_for = 259200
                paid_for = DATE_CHOICES[service.period/(360*24*60*60)][0]

                return paid_for

    def clean(self):
   
        print (self.data['paid_for'])
        if self.data['paid_for'] == "":
            if self.cleaned_data.get('service'):
                service = self.cleaned_data['service']
                #if service.period_unit_raw == services.UNIT_MONTHS:
                #    #instance.paid_for = 1
                #    self.cleaned_data['paid_for'] = DATE_CHOICES[service.period/12][0]
                #elif service.period_unit_raw == services.UNIT_HOURS:
                #    #instance.paid_for = 720
                #    self.cleaned_data['paid_for'] = DATE_CHOICES[service.period/(360*24)][0]
                #elif service.period_unit_raw == services.UNIT_SECONDS:
                #    #instance.paid_for = 259200
                #    self.cleaned_data['paid_for'] = DATE_CHOICES[service.period/(360*24*60*60)][0]
                self.cleaned_data['paid_for'] = self.set_paid_for(service)
        
        cleaned_data=super(PaymentForm, self).clean()

        print "%s" % (cleaned_data)
        return cleaned_data

    def save(self, commit=True):
        instance = super(PaymentForm, self).save(commit=False)
        if instance:

            subscription = ServiceSubscription.objects.get(
                service=self.cleaned_data['service'],
                customer=self.cleaned_data['customer']
            )
            instance.subscription = subscription 
            instance.save()

            subscription.last_paid_on = instance.paid_on
            subscription.last_paid_for = instance.paid_for
            subscription.save()

        return instance


    class Meta:
        model = ServiceSubscriptionPayments
        exclude = ('subscription',)

class ServiceSubscriptionPaymentsAdmin(admin.ModelAdmin): 

    form = PaymentForm
    
    list_display = ('subscription', 'amount', 'paid_on','note')
    search_fields = ['subscription']


    class Media:
        css = {
            'all' : ('adminstyle.css',),
        }

        js = ("admin_customization.js",)

admin.site.register(Service, ServiceAdmin)	
admin.site.register(ServiceSubscription, ServiceSubscriptionAdmin)	
admin.site.register(ServiceSubscriptionPayments, ServiceSubscriptionPaymentsAdmin)	
