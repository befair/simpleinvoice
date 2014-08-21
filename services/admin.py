from django.contrib import admin
from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from django.core.mail import send_mail
from services.models import Service, ServiceSubscription
from django.contrib.contenttypes.models import ContentType

class ServiceAdmin(admin.ModelAdmin): 

    list_display = ('name', 'description', 'period_unit_display', 'amount')
    #list_display_links = ('name',)
    #list_filter = []
    search_fields = ['name']

    #inlines = [CustomerContactInline]

    class Media:
        css = {
            'all' : ('adminstyle.css',),
        }

class ServiceSubscriptionAdmin(admin.ModelAdmin): 

    list_display = ('customer', 'service', 'subscribed_on', 'subscribed_until', 'note')
    #list_display_links = ('name',)
    #list_filter = []
    search_fields = ['customer']

    #inlines = [CustomerContactInline]

    actions = ['check_payement']

    def check_payement(self, request, queryset):
        #print queryset
        #selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        #ct = ContentType.objects.get_for_model(queryset.model)
        #print ct
        #query_string = "ct=%s&ids=%s" % (ct.pk, ",".join(selected))
        #print query_string

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

admin.site.register(Service, ServiceAdmin)	
admin.site.register(ServiceSubscription, ServiceSubscriptionAdmin)	
