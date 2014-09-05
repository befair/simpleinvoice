from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
#from django.core.exceptions import DoesNotExist, IntegrityError
from django.utils.translation import ugettext, ugettext_lazy as _
from django.utils import timezone
from django.db import IntegrityError

from services.models import ServiceSubscriptionPayment, ServiceSubscription, Service
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
        return HttpResponse('{"status": "ERROR"}',content_type="application/json")

    i = 0

    while len(qd) > 0:
        customer_id = int(qd.pop("payments[%s][%s]" % (i,'customer'))[0])
        date = qd.pop("payments[%s][%s]" % (i,'paid_for'))[0]
        try:
            #TODO Matteo: check if date is valid
            paid_for = timezone.datetime(int(date[6:]),int(date[3:5]),int(date[:2]))
        except ValueError as e:
            return HttpResponse('{"status": "ERROR","message": "%(message)s' % {'message':_("Invalid data"),},content_type="application/json")
            
        amount = float(qd.pop("payments[%s][%s]" % (i,'cost'))[0])
        if amount < 0:
            return HttpResponse('{"status": "ERROR","message": "%(message)s' % {'message':_("Invalid data"),},content_type="application/json")

        notes = qd.pop("payments[%s][%s]" % (i,'notes'))[0]

        ss = ServiceSubscriptionPayment()
        try:
            subscription = ServiceSubscription.objects.get(
                service=Service.objects.get(pk=service_id),
                customer=Customer.objects.get(pk=customer_id)
            )
        except DoesNotExist as e:
            return HttpResponse('{"status": "ERROR","message": "%(message)s' % {'message':_("Invalid data"),},content_type="application/json")
         
        ss.subscription = subscription
        ss.amount = amount
        ss.vat_percent = subscription.vat_percent
        ss.discount = subscription.discount
        ss.paid_for = paid_for
        ss.note = notes

        objects.append(ss)

        i += 1

    for obj in objects:
        try:
            obj.save()
        except IntegrityError as e:
            return HttpResponse('{"status": "ERROR","message": "%(message)s' % {'message':_("Invalid data"),},content_type="application/json")

        obj.subscription.last_paid_on = ss.paid_on
        obj.subscription.last_paid_for = ss.paid_for
        obj.subscription.save()

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

