from django.contrib import admin
from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template import loader, Context
from services import models as services
from services.models import Service, ServiceSubscription, ServiceSubscriptionPayment, DATE_CHOICES
from django import forms
from django.conf import settings
from django.contrib.auth.models import Group 
from django.contrib import messages
from django.utils import timezone

from invoice.models import Customer

class ServiceSubscriptionForm(forms.ModelForm):

    #default_vat_percent = PercentageDecimalField()

    class Meta:
        model = Service

class ServiceAdmin(admin.ModelAdmin): 

    list_display = ('name', 'description', 'period_unit_display', 'amount')
    search_fields = ['name']

    exclude = ('period_unit_source',)

    class Media:
        css = {
            'all' : ('adminstyle.css',),
        }

class ServiceSubscriptionForm(forms.ModelForm):

    #discount = PercentageDecimalField(label=_('discount'))
    #vat_percent = PercentageDecimalField(label=_('vat_percent'))

    #def save(self, commit=True):
    #    instance = super(ServiceSubscriptionForm, self).save(commit=False)

    #    if instance:

    #        service = Service.objects.get(pk=1)
    #        instance.service = service
    #        instance.save()

    #    return instance

    class Meta:

        model = ServiceSubscription
        exclude = (
            'invoice_period', 'last_paid_on','last_paid_for', 
            'is_deleted', 'when_deleted',
            'subscribed_from_dt', 'subscribed_from_value',
			'howmany'
        )

        #labels = {
        #    'discount' : _("discount"),
        #    'vat_percent' : _("vat_percent"),
        #}


class ServiceSubscriptionAdmin(admin.ModelAdmin): 

    form = ServiceSubscriptionForm

    #list_display = ('customer', 'service', 'subscribed_on', 'subscribed_until', 'note','is_deleted')
    search_fields = ['customer']

    actions = ['check_payment','delete_subscriptions','restore_subscriptions']

    def has_add_permission(self, request):
        """
        """
        if Customer.objects.count() == 0:
            return False
        return True

    def get_list_display(self, request):
        """
        """
        if request.user.groups.filter(name='referrers'):
            list_display = ('customer', 'service', 'subscribed_on', 'note','is_deleted')
        else:
            list_display = ('customer', 'service', 'subscribed_on', 'note')
        return list_display

    def get_queryset(self, request):
        """
        """
        if request.user.is_superuser:
            qs = self.model.all_objects.get_queryset()
        else:
            qs = self.model.objects.get_queryset()

        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    def check_payment(self, request, queryset):
        """
        Check if the selected subscriptions fees have already been payed.

        The subscription last payment date (or quantity) is compared with
        the current time (or consumed quantity) and if the difference is 
        higher than the next period (or period quantity) then a remind 
        mail is sent to the corresponding customer 
        
        """

        for obj in queryset:

            if obj.next_payment_due:

                if not obj.customer.email:
                    self.message_user(request, _("Customer %s should pay, but is has no email address"), level=messages.WARNING)

                else:
                
                    template_txt = settings.EMAIL_TEMPLATES['INSOLUTE_TXT']
                    template_html = settings.EMAIL_TEMPLATES['INSOLUTE_HTML']
                    n_periods = int(obj.periods_from_last_payment)
                    print type((obj.discounted_price * n_periods))
                    context = {
                       'customer' : obj.customer,
                       'amount' : (obj.discounted_price * n_periods),
                       'service': obj.service,
                       'n_periods' : n_periods,
                       'initial' : obj.topay_start_display,
                       'end' : obj.topay_end_display,
                        #TODO compute
                       'now' : timezone.now().astimezone(obj.customer.timezone).date, 
                    }
                    subject = 'Payment due'
                    sender = settings.EMAIL_SENDER
                    receivers = [obj.customer.email]
                    msg = EmailMultiAlternatives(
                        subject, loader.get_template(template_txt).render(Context(context)), 
                        sender, receivers
                    )
                    msg.attach_alternative(
                        loader.get_template(template_html).render(Context(context)),
                        "text/html"
                    )
                    msg.send()

    check_payment.short_description = _("Send a reminder mail about unsolved subcscpriptions")

    def delete_subscriptions(self, request, queryset):
        """
        Flag selected subscriptions as deleted
        """

        if request.user.is_superuser:
            for obj in queryset:
                obj.is_deleted = True
                obj.when_deleted = timezone.now()
                obj.save()

    delete_subscriptions.short_description = _("Cancel selected service subscription/s ")

    def restore_subscriptions(self, request, queryset):
        """
        Flag selected subscriptions as deleted
        """

        if request.user.is_superuser:
            for obj in queryset:
                obj.is_deleted = False
                obj.when_deleted = None
                obj.save()

    restore_subscriptions.short_description = _("Restore selected service subscription/s ")

    def get_actions(self, request):
        """
        Remove default cancel action behaviour, using custom action
        instead (see delete_subscriptions ) 
        """

        actions = super(ServiceSubscriptionAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        #if request.user.is_superuser:
        #    actions['delete_subscriptions'] = (self.delete_subscriptions,'delete_subscriptions',self.delete_subscriptions.short_description)
        #    actions['restore_subscriptions'] = (self.restore_subscriptions,'restore_subscriptions',self.restore_subscriptions.short_description)
        return actions

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
    #discount = PercentageDecimalField()
    #vat_percent = PercentageDecimalField()

    class Meta:
        model = ServiceSubscriptionPayment
        exclude = ('subscription','vat_percent','discount',)

    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        self.fields['paid_for'].initial = DATE_CHOICES[5][0]

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
   
        if self.data['paid_for'] == "":
            if self.cleaned_data.get('service'):
                service = self.cleaned_data['service']
                self.cleaned_data['paid_for'] = self.set_paid_for(service)
        
        cleaned_data=super(PaymentForm, self).clean()

        return cleaned_data

    def save(self, commit=True):
        instance = super(PaymentForm, self).save(commit=False)
        if instance:

            subscription = ServiceSubscription.objects.get(
                service=self.cleaned_data['service'],
                customer=self.cleaned_data['customer']
            )
            if subscription.is_deleted:
                raise forms.ValidationError("A payment cannot be done for the subscription since it is deleted") 
            instance.subscription = subscription 
            instance.save()

            subscription.last_paid_on = instance.paid_on
            subscription.last_paid_for = instance.paid_for
            subscription.save()

        return instance

class ServiceSubscriptionPaymentAdmin(admin.ModelAdmin): 

    form = PaymentForm

    fieldsets = (
        (None, {
            'fields' : ('customer', 
                        'service','amount', 'vat_percent',
                        'discount', 'paid_for', 'note'
            )
        }),
    )
    
    list_display = ('subscription', 'paid_on', 'amount', 'note')
    search_fields = ['subscription']

    def get_form(self, request, obj=None, **kwargs):
        """
        Form Meta exclude seems to not work
        """
        kwargs['exclude'] = ['discount','vat_percent',]
        return super(ServiceSubscriptionPaymentAdmin, self).get_form(request, obj=obj, **kwargs)

    def has_add_permission(self, request):
        """
        """
        # Checking only not-deleted Subscriptions
        if ServiceSubscription.objects.count() == 0:
            return False
        return True

    class Media:
        css = {
            'all' : ('adminstyle.css',),
        }

        js = ("admin_customization.js",)

admin.site.register(Service, ServiceAdmin)	
admin.site.register(ServiceSubscription, ServiceSubscriptionAdmin)	
admin.site.register(ServiceSubscriptionPayment, ServiceSubscriptionPaymentAdmin)	
