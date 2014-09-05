from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt

from services.models import ServiceSubscription, Service
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

