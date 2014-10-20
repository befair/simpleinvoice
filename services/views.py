from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseServerError
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
#from django.core.exceptions import DoesNotExist, IntegrityError
from django.utils.translation import ugettext, ugettext_lazy as _
from django.utils import timezone
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned, ValidationError

from services.models import ServiceSubscriptionPayment, ServiceSubscription, Service, DATE_CHOICES
from invoice.models import Customer

import json

@staff_member_required
def bulk_service_payment(request):
    
    c = {'services': []}
    for s in Service.objects.all():
        c['services'].append({'id': s.id, 'name': s.name})

    return render_to_response('bulk.html', c)

# API -----

@staff_member_required
@csrf_exempt
def bulk_payments(request):
    """
    API view.
    Create all payments from the in bulk insert.
    """

    qd  = request.POST.copy()
    objects = []

    try:
        service_id = int(qd.pop('service_id')[0])
    except KeyError as e:
        return HttpResponseServerError('{"status": "ERROR", "message" : "Please select a service"}',content_type="application/json")

    i = 0

    while len(qd) > 0:
        subscription_id = None
        try:
            customer_id = int(qd.pop("payments[%s][%s]" % (i,'customer'))[0])
        except KeyError as e:
            subscription_id =  int(qd.pop("payments[%s][%s]" % (i,'subscription'))[0])
        date = qd.pop("payments[%s][%s]" % (i,'paid_for'))[0]
        amount = float(qd.pop("payments[%s][%s]" % (i,'cost'))[0])
        try:
            if check_date(date):
                paid_for = timezone.datetime(int(date[6:]),int(date[3:5]),int(date[:2]),tzinfo=pytz.UTC)
            else:
                raise ValueError
        except ValueError as e:
            return HttpResponseServerError('{"status":"ERROR", "date":"%(date)s","customer":"%(customer_id)s", "message": "Please choose a valid date"}' % {"date" : date, "customer_id" : customer_id},content_type="application/json")
            
        if amount < 0:
            return HttpResponseServerError('{"status": "ERROR","cost":"%(cost)s","customer":"%(customer_id)s", "message": "Please insert a non negative amount"}' % {"cost" : amount, "customer_id" : customer_id},content_type="application/json")

        notes = qd.pop("payments[%s][%s]" % (i,'notes'))[0]

        pay_with = qd.pop("payments[%s][%s]" % (i,'pay_with'))[0]

        date = qd.pop("payments[%s][%s]" % (i,'when_paid'))[0]

        try:
            if check_date(date):
                when_paid = timezone.datetime(int(date[6:]),int(date[3:5]),int(date[:2]),tzinfo=pytz.UTC)
            else:
                raise ValueError
        except ValueError as e:
            return HttpResponseServerError('{"status":"ERROR", "date":"%(date)s","customer":"%(customer_id)s", "message": "Please choose a valid date"}' % {"date" : date, "customer_id" : customer_id},content_type="application/json")


        ss = ServiceSubscriptionPayment()
        try:
            if not subscription_id:
                subscription = ServiceSubscription.objects.get(
                    service=Service.objects.get(pk=service_id),
                    customer=Customer.objects.get(pk=customer_id)
                )
            else:
                subscription = ServiceSubscription.objects.get(
                    pk=subscription_id
                )
        except ObjectDoesNotExist as e:
            return HttpResponseServerError('{"status": "ERROR","cost":"%(cost)s","customer":"%(customer_id)s", "message": "A subscription for service %(service)s  and customer %(customer)s does not exist"}' % {"service" : Service.objects.get(pk=service_id), "customer" : Customer.objects.get(pk=customer_id),"cost" : amount, "customer_id" : customer_id},content_type="application/json")
        except MultipleObjectsReturned as e:
            subscriptions = ServiceSubscription.objects.filter(
                service=Service.objects.get(pk=service_id),
                customer=Customer.objects.get(pk=customer_id)
            )
            sub_list = ""
            for sub in subscriptions:
                sub_list = sub_list + "<option value='%s'>%s</option>" % (sub.pk,sub) 
 
            return HttpResponseServerError('{"status": "ERROR","cost":"%(cost)s","customer":"%(customer_id)s", "sub_list":"%(sub_list)s", "message":"There are multiple subscription for service %(service)s and customer %(customer)s"}' % {"service" : Service.objects.get(pk=service_id), "customer" : Customer.objects.get(pk=customer_id),"cost" : amount, "customer_id" : customer_id, "sub_list" : sub_list},content_type="application/json")
            
        ss.subscription = subscription
        ss.amount = amount
        ss.vat_percent = subscription.vat_percent
        ss.discount = subscription.discount
        ss.paid_for = paid_for
        ss.note = notes
        ss.when_paid = when_paid
        ss.pay_with = pay_with

        objects.append({"saved":False,"obj":ss})

        i += 1

    for pair in objects:
        try:
            obj = pair['obj']
            if not pair['saved']:
                obj.save()
                obj.subscription.last_paid_on = ss.paid_on
                obj.subscription.last_paid_for = ss.paid_for
                obj.subscription.save()
                pair['saved'] = True
        except IntegrityError as e:
            return HttpResponseServerError('{"status": "ERROR","cost":"%(cost)s","customer":"%(customer_id)s","message": "Payment for subscription %(subscription)s has not been created"}' % {"subscription" : ServiceSubscription.objects.get(pk=obj.subscription.pk), "cost" : obj.amount, "customer_id" : obj.subscription.customer.pk},content_type="application/json")
        except ValidationError as e:
            return HttpResponseServerError('{"status": "ERROR","cost":"%(cost)s","customer":"%(customer_id)s","paid_for":"%(paid_for)s","message": "A payment for subscription  %(subscription)s already exists "}' % {"subscription" : ServiceSubscription.objects.get(pk=obj.subscription.pk), "cost" : obj.amount, "customer_id" : obj.subscription.customer.pk, "paid_for" : obj.paid_for} ,content_type="application/json")



    return HttpResponse('a');

@staff_member_required
def get_services(request, customer_id):
    """
    API view.
    Returns all services and subscriptions of a given Customer in JSON.

    """
    
    response = {}

    customer = get_object_or_404(Customer, pk=customer_id)

    for sub in ServiceSubscription.objects.filter(customer=customer):
        response[sub.service.id] = {
            'service_id': sub.service.id,
            'service_name': sub.service.name,
            'amount': str(sub.service.amount),
            'vat': str(sub.vat_percent),
            'discount': str(sub.discount),
        }
    
    return HttpResponse(
        json.dumps(response),
        content_type="application/json"
    )

@staff_member_required
def get_customers(request, service_id):
    """
    API view.
    Returns all customer subscribed to a given Service in JSON.

    """
    
    response = {}

    service = get_object_or_404(Service, pk=service_id)

    response['amount'] = str(service.amount)

    for sub in ServiceSubscription.objects.filter(service=service_id):
        response[sub.customer.id] = {
            'customer_id': sub.customer.id,
            'customer_name': sub.customer.name,
        }
    
    return HttpResponse(
        json.dumps(response),
        content_type="application/json"
    )

def check_date(date):
    """
    Check if date year is between the allowed services.models.DATE_CHOICES.
    Checks on month and day are done from timezone.datetime(), wrong ones raise
    ValueError
    """

    return len(date) == 10 and ( 
        int(DATE_CHOICES[0][1][6:]) <= int(date[6:]) <= int(DATE_CHOICES[-1][1][6:])
        )
